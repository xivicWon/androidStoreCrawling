import sys, rootpath 
sys.path.append(rootpath.detect())
import requests, time, json
from typing import Callable,  List
from urllib import parse
from bs4 import BeautifulSoup as bs
from requests import post, get
from threading import Thread, current_thread 
from multiprocessing import Process, Queue, current_process
from dotenv import load_dotenv
from dto.DomParsingDto import DomParsingDto
from dto.RequestDto import RequestDto
from entity.AppEntity import AppEntity
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from module.OpenDB_v3 import OpenDB
from repository.AppStoreRepository import AppStoreRepository
from module.EnvManager import EnvManager
    
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
    prefixUrl = "https://apps.apple.com/kr/app/"
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

def domParser(resquest:requests.Response )->DomParsingDto:
    try : 
        soup = bs(resquest.text, "html.parser")
        data = json.loads(soup.find('script', type='application/ld+json').text)
        developerUrl2 = parse.unquote(data['author']['url'])
        developerUrl = developerUrl2.split("/").pop() if len(developerUrl2) else ""
        return DomParsingDto ( 
            data['author']['name'],
            developerUrl,
            data['name']
        )
    except AttributeError as e : 
        print(e)
        return None
    

def parsingToGoogle(dto:RequestDto):
    domParsingDto = domParser(dto.getResponse())
    try : 
        developId = domParsingDto.getUrl()
    except: 
        developId = ""
    appMarketDeveloperEntity = AppMarketDeveloperEntity()
    appMarketDeveloperEntity.setDeveloperMarketId(developId).setDeveloperName(domParsingDto.getAuthor()).setMarketNum(MARKET_NUM).setCompanyNum(0)
    result = appStoreRepository.findDeveloperByDeveloperMarketId(appMarketDeveloperEntity)

    if( result == None ):
        try :
            developNum = appStoreRepository.saveDeveloper(appMarketDeveloperEntity)
            # 멀티쓰레드로 인해 찰나에 이미 등록되었을 경우. 저장이 되지 않기에 0이란 값을 반환함.
            if developNum == 0 :
                result = appStoreRepository.findDeveloperByDeveloperMarketId(appMarketDeveloperEntity)
                developNum = result.getNum
        except Exception as e : 
            print(e)
            exit()
    else :
        developNum = result.getNum   
        
    appEntity = AppEntity()
    appEntity.setId(dto.getUrl()).setAppName(domParsingDto.getAppName()).setMarketNum(MARKET_NUM).setIsActive('Y').setLastUpdateCurrent()
    if developNum : 
        appEntity.setDeveloperNum(developNum)
        
    appStoreRepository.updateApp(appEntity)
    
    
def notFoundGoogleParsing(dto:RequestDto):
    appEntity = AppEntity()
    appEntity.setId(dto.getUrl()).setAppName('').setMarketNum(MARKET_NUM).setIsActive('N').setDeveloperNum(0).setLastUpdateCurrent()
    appStoreRepository.updateApp(appEntity)
        

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
    
    
def requestWorkListFromDB(appStoreRepository: AppStoreRepository, marketNum:int , offset:int , limit : int ) :
    appList = appStoreRepository.findAppLimitedTo(marketNum, offset, limit)
    if type(appList) == list:
        mappingAppEntityId : Callable[[AppEntity], str] = lambda t : t.getId() 
        crwlingJob = list(map( mappingAppEntityId , appList ) )
    else :
        print("조회결과 없음 {} {} {} ".format(marketNum, offset, limit))
        exit()
    return crwlingJob


def main() :

    q = Queue()
    offset = 0
    limit = 1000
    crwlingJob = requestWorkListFromDB(appStoreRepository, MARKET_NUM, offset, limit)
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
    

envManager = EnvManager()
openDB: OpenDB = OpenDB(envManager.DB_HOST, envManager.DB_USER ,envManager.DB_PASSWORD ,envManager.DB_DATABASE )
appStoreRepository:AppStoreRepository = AppStoreRepository(openDB)

MARKET_NUM = 2 


## App 테이블에 등록된 market_num 가 2 인 데이터를 조회하여, app 데이터 갱신 및 developer등록 처리.
#
# how to run ? 
# >> python AppleStore.py

if __name__  == '__main__' :
    MAX_PROCESS_COUNT = 5
    THREAD_COUNT = 100
    start = time.time()
    main()
    print("Time : {}  ".format(time.time() - start  ))