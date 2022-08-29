import requests, time, json
import os
from typing import Callable,  List
from urllib import parse
from bs4 import BeautifulSoup as bs
from requests import post, get
from threading import Thread, current_thread 
from multiprocessing import Process, Queue, current_process
from dotenv import load_dotenv
from dto.RequestDto import RequestDto
from entity.AppEntity import AppEntity
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from module.OpenDB_v3 import OpenDB
from repository.AppStoreRepository import AppStoreRepository
from module.EnvStore import EnvStore 


def curl(url:str)->requests.Response: 
    res = get(url, timeout=5)
    try :
        return res
    except requests.exceptions.ReadTimeout: 
        return None
    except requests.exceptions.ConnectionError: 
        return None
    except requests.exceptions.ChunkedEncodingError:
        return None


def workToThread(id : str,  obj:List[RequestDto]):
    prefixUrl = "https://play.google.com/store/apps/details?id="
    requestUrl = prefixUrl + id
    try:
        res:requests.Response = curl(requestUrl)
        obj.append(RequestDto(id, res))

    except requests.exceptions.ReadTimeout: 
        print(current_thread().getName() + "ReadTimeout request Fail : {}".format(requestUrl))
        return 
    except requests.exceptions.ConnectionError: 
        print(current_thread().getName() + "ConnectionError request Fail : {}".format(requestUrl))
        return 
    except requests.exceptions.ChunkedEncodingError:
        print(current_thread().getName() + "ChunkedEncodingError request Fail : {}".format(requestUrl))
        return 

def parsingToGoogle(dto:RequestDto):
    marketNum = 1 
    try : 
        soup = bs(dto.getResponse().text, "html.parser")
        data = json.loads(soup.find('script', type='application/ld+json').text)
        try : 
            encodeDevelopId = soup.find("a", string=data['author']['name'])["href"].replace("/store/apps/developer?id=", "").replace("/store/apps/dev?id=", "")
            developId = parse.unquote(encodeDevelopId)
        except: 
            developId = ""
    except AttributeError as e : 
        print(e)
        return 
    appMarketDeveloperEntity = AppMarketDeveloperEntity()
    appMarketDeveloperEntity.setDeveloperMarketId(developId).setDeveloperName(data['author']['name']).setMarketNum(marketNum).setCompanyNum(0)
    result = googleStoreRepository.findDeveloperByDeveloperMarketId(appMarketDeveloperEntity)

    if( result == None ):
        try :
            developNum = googleStoreRepository.saveDeveloper(appMarketDeveloperEntity)
            if developNum == 0 :
                result = googleStoreRepository.findDeveloperByDeveloperMarketId(appMarketDeveloperEntity)
                developNum = result.getNum  
        except Exception as e : 
            print(e)
            exit()
    else :
        developNum = result.getNum   
        
    appEntity = AppEntity()
    appEntity.setId(dto.getUrl()).setAppName(data['name']).setMarketNum(marketNum).setIsActive('Y').setLastUpdateCurrent()
    if developNum : 
        appEntity.setDeveloperNum(developNum)
        
    googleStoreRepository.updateApp(appEntity)
    
    
def notFoundGoogleParsing(dto:RequestDto):
    marketNum = 1 
    appEntity = AppEntity()
    appEntity.setId(dto.getUrl()).setAppName('').setMarketNum(marketNum).setIsActive('N').setDeveloperNum(0).setLastUpdateCurrent()
    googleStoreRepository.updateApp(appEntity)
        

def filteredAliveThread(t : Thread):
    if t.is_alive() :
        return True
    else :
        t.join()
        return False

def workToProcess(crwlingJob:list , maxThreadCount : int, q : Queue) :
    processName = current_process().name
    print("{} thread working Count : {}".format(processName, len(crwlingJob)))
    threadlist: List[Thread] = []
    allThreadList: List[Thread] = []
    resList:List[RequestDto] = [] 
    threadIndex = 0 
    while( len(crwlingJob) >= 1 ):
        if len(threadlist) >= maxThreadCount :
            threadlist = list(filter( filteredAliveThread , threadlist))
        else :
            url = crwlingJob.pop()
            ## 여러개의 작업리스트를 전달하도록.
            threadIndex += 1 
            workThread = Thread(target=workToThread , name="{} [{}th thread ]".format(processName, threadIndex), args=(url, resList, ))
            threadlist.append(workThread)
            allThreadList.append(workThread)
            workThread.start()
            
    for thread in allThreadList:
        thread.join()
    q.put(resList)
        
def consumerProcess(q: Queue):
    requestResults:List[RequestDto] = []
    while ( True ):
        value = q.get()
        if( value == "None"):
            break
        requestResults.extend(value)
    print("request result : {}".format(len(requestResults)))
    for resultData in requestResults : 
        if resultData.getResponse().status_code == 200 :
            parsingToGoogle(resultData)
        else :
            notFoundGoogleParsing(resultData)
    
    
def requestWorkListFromDB(googleStoreRepository: AppStoreRepository, marketNum:int , offset:int , limit : int ) :
    appList = googleStoreRepository.findNoNameAppLimitedTo(marketNum, offset, limit)
    if type(appList) == list:
        mappingAppEntityId : Callable[[AppEntity], str] = lambda t : t.getId() 
        crwlingJob = list(map( mappingAppEntityId , appList ) )
    else :
        print("조회결과 없음 {} {} {} ".format(marketNum, offset, limit))
        exit()
    return crwlingJob


def main() :

    q = Queue()
    marketNum = 1 
    offset = 0
    limit = 1000
    crwlingJob = requestWorkListFromDB(googleStoreRepository, marketNum, offset, limit)
    jobCount = len(crwlingJob)
    jobLengthEachProcess = max( jobCount % MAX_PROCESS_COUNT, int(jobCount / MAX_PROCESS_COUNT))
    processList: List[Process] = []
    
    print("Process : {}  total job length : {} each work : {} ".format(MAX_PROCESS_COUNT, jobCount, jobLengthEachProcess ))
    print("총 {} 건 작업 시작~ ".format(len(crwlingJob)) )
    processNum = 0
    if len(crwlingJob) > 0:
        while len(crwlingJob) > 0:
            if len(processList) + 1  == MAX_PROCESS_COUNT:
                processJob = crwlingJob[:]
                del crwlingJob[:]
            else :
                processJob = crwlingJob[:jobLengthEachProcess]
                del crwlingJob[:jobLengthEachProcess]
                
            if len(processJob) > 0 : 
                processNum += 1 
                processList.append( Process(target=workToProcess , name="[ {}th process ]".format(processNum), args=(processJob, THREAD_COUNT,q ,) ))

    consumer = Process(target=consumerProcess , name="[ consumer process ]", args=(q,))
    consumer.start()
    for process in processList:
        process.start()
        print(process.name + " >> {}".format("LIVE" if process.is_alive() else "DIE"))
    
    for process in processList:
        process.join()
        print(process.name + " >> {}".format("LIVE" if process.is_alive() else "DIE"))
        
    q.put("None")
    consumer.join()
    q.close()
    
    
Env = EnvStore()
appStore = Env.getAppStore
openDB: OpenDB = OpenDB(appStore["host"], appStore["user_name"]  ,appStore["password"] , appStore["database"] )
googleStoreRepository:AppStoreRepository = AppStoreRepository(openDB)
    
if __name__  == '__main__' :
    MAX_PROCESS_COUNT = 5
    THREAD_COUNT = 100
    start = time.time()
    
    main()
    print("Time : {}  ".format(time.time() - start  ))