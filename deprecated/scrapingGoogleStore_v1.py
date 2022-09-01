
import sys, rootpath 
sys.path.append(rootpath.detect())
import requests, time, json
from typing import Callable, List
from urllib import parse
from bs4 import BeautifulSoup as bs
from requests import post, get
from threading import Thread, current_thread 
from multiprocessing import Process, current_process
from entity.AppEntity import AppEntity
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from module.OpenDB_v3 import OpenDB
from repository.AppStoreRepository import AppStoreRepository
from module.EnvManager import EnvManager

def curl(url:str)->requests.Response: 
    res = get(url, timeout=3)
    try :
        return res
    except requests.exceptions.ReadTimeout: 
        return None
    except requests.exceptions.ConnectionError: 
        return None
    except requests.exceptions.ChunkedEncodingError:
        return None


def crawlingGoogle(id : str):
    # processName = current_process().name
    # print( "\tps : {} - id : {}".format( processName, id))
    prefixUrl = "https://play.google.com/store/apps/details?id="
    requestUrl = prefixUrl + id
    try:
        res:requests.Response = curl(requestUrl)
        if res.status_code == 200 :
            parsingToGoogle(id, res)
        elif res.status_code == 404 :
            notFoundGoogleParsing(id)
 
    except requests.exceptions.ReadTimeout: 
        return 
        # print(current_thread().getName() + " request Fail : {}".format(requestUrl))
    except requests.exceptions.ConnectionError: 
        return 
        # print(current_thread().getName() + "request Fail : {}".format(requestUrl))
    except requests.exceptions.ChunkedEncodingError:
        return 
    

def parsingToGoogle(id : str, res :requests.Response ):
    
    soup = bs(res.text, "html.parser")
    data = json.loads(soup.find('script', type='application/ld+json').text)
    try : 
        encodeDevelopId = soup.find("a", string=data['author']['name'])["href"].replace("/store/apps/developer?id=", "").replace("/store/apps/dev?id=", "")
        developId = parse.unquote(encodeDevelopId)
    except: 
        developId = ""
    
    marketNum = 1 
    
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
            print(e )
            exit()
    else :
        developNum = result.getNum   
        
    print( "\tps : {} - th : {} - id : {} - developer - {}".format( current_process().name, current_thread().getName(), id, appMarketDeveloperEntity.developer_name))
    appEntity = AppEntity()
    appEntity.setId(id).setAppName(data['name']).setMarketNum(marketNum).setIsActive('Y').setLastUpdateCurrent()
    if developNum : 
        appEntity.setDeveloperNum(developNum)
        
    googleStoreRepository.updateApp(appEntity)
    

def notFoundGoogleParsing(id : str):
    print( "\tps : {} - th : {} - id : {} - developer - {}".format( current_process().name, current_thread().getName(), id, ''))
    marketNum = 1 
    appEntity = AppEntity()
    appEntity.setId(id).setAppName('').setMarketNum(marketNum).setIsActive('N').setDeveloperNum(0).setLastUpdateCurrent()
    googleStoreRepository.updateApp(appEntity)
        

def filteredAliveThread(t:Thread):
    if t.is_alive() :
        return True
    else :
        t.join()
        return False


def workToThread(crwlingJob:list ) :
    processName = current_process().name
    maxThreadCount = 100
    print("{} thread working Count : {}".format(processName, len(crwlingJob)))
    threadlist: List[Thread] = []
    
    while( len(crwlingJob) >= 1 ):
        if len(threadlist) >= maxThreadCount :
            # 전체 내역중에 종료된 내역이 있는지 체크.
            threadlist = list(filter( filteredAliveThread , threadlist))
        else :
            url = crwlingJob.pop()
            workThread = Thread(target=crawlingGoogle , name="{} [{}th thread ]".format(processName, len(threadlist)), args=(url,))
            threadlist.append(workThread)
            workThread.start()
            
        for thread in threadlist:
            thread.join()
            

    for thread in threadlist:
        thread.join()


Env = EnvStore()
appStore = Env.getAppStore
openDB: OpenDB = OpenDB(appStore["host"], appStore["user_name"]  ,appStore["password"] , appStore["database"] )
googleStoreRepository:AppStoreRepository = AppStoreRepository(openDB)

if __name__  == '__main__' :
    start = time.time()
    offset = 0
    limit = 100
    # Google MarketNum
    marketNum = 1 
    appList = googleStoreRepository.findNoNameAppLimitedTo(marketNum, offset,limit)
    if type(appList) == list:
        mappingAppEntityId : Callable[[AppEntity], str] = lambda t : t.getId() 
        crwlingJob = list(map( mappingAppEntityId , appList ) )
    else :
        print("조회결과 없음 {} {} {} ".format(marketNum, offset, limit))
        exit()
    jobCount = len(crwlingJob)
    MAX_PROCESS_COUNT = 4
    jobLengthEachProcess = max( jobCount % MAX_PROCESS_COUNT, int(jobCount / MAX_PROCESS_COUNT))
    processList: List[Process] = []
    startPoint = 0 
    print(" process : {}  total job length : {} each work : {} ".format(MAX_PROCESS_COUNT, jobCount, jobLengthEachProcess ))
    print("총 {} 건 작업 시작~ ".format(len(crwlingJob)) )
    if len(crwlingJob) > jobLengthEachProcess :
        processNum = 1
        while len(crwlingJob) > 0 and len(processList) < MAX_PROCESS_COUNT :
            processJob = crwlingJob[:jobLengthEachProcess]
            if len(processJob) > 0 : 
                del crwlingJob[:jobLengthEachProcess]
                print (processJob)
                processList.append( Process(target=workToThread , name="[ {}th process ]".format(processNum), args=(processJob,) ))
                processNum += 1 
    else :
        processList.append( Process(target=workToThread , name="[ 0th process ]", args=(crwlingJob,)))
    
    print("processlist Count {}".format(len(processList)))

    for process in processList:
        process.start()
        print(process.name + " >> {}".format("LIVE" if process.is_alive() else "DIE"))
    
    for process in processList:
        process.join()
        print(process.name + " >> {}".format("LIVE" if process.is_alive() else "DIE"))

    print(" time : {}  ".format(time.time() - start  ))