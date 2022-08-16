import requests, time, json
import os
from typing import Callable, List
from urllib import parse
from bs4 import BeautifulSoup as bs
from requests import post, get
from threading import Thread, current_thread 
from multiprocessing import Process, current_process
from dotenv import load_dotenv
from entity.AppEntity import AppEntity
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from module.OpenDB_v3 import OpenDB
from module.AppStoreRepository import AppStoreRepository


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
    
    print( "\tps : {} ".format( current_thread().getName()))

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
    
    result = googleStoreRepository.findDeveloperByDeveloperNum(appMarketDeveloperEntity)

    if( result == None ):
        try :
            developNum = googleStoreRepository.saveDeveloper(appMarketDeveloperEntity)
            if developNum == 0 :
                result = googleStoreRepository.findDeveloperByDeveloperNum(appMarketDeveloperEntity)
                developNum = result.getNum()  
        except Exception as e : 
            print(e )
            exit()
    else :
        developNum = result.getNum()    
        
    # print( "\tps : {} - id : {} - developer - {}".format( current_thread().getName(), id, appMarketDeveloperEntity.developer_name))
    appEntity = AppEntity()
    appEntity.setId(id).setAppName(data['name']).setMarketNum(marketNum).setIsActive('Y').setLastUpdateCurrent()
    if developNum : 
        appEntity.setDeveloperNum(developNum)
        
    googleStoreRepository.updateApp(appEntity)
    

def notFoundGoogleParsing(id : str):
    # print( "\tps : {} - id : {} - developer - {}".format( current_thread().getName(), id, ''))
    marketNum = 1 
    appEntity = AppEntity()
    appEntity.setId(id).setAppName('').setMarketNum(marketNum).setIsActive('N').setDeveloperNum(0).setLastUpdateCurrent()
    googleStoreRepository.updateApp(appEntity)
        

def filteredAliveThread(t):
    if t.is_alive() :
        return True
    else :
        t.join()
        return False


def workToSingleThread(crwlingJob:list ) :
    processName = current_process().name
    print("{} thread working Count : {}".format(processName, len(crwlingJob)))
    while( len(crwlingJob) >= 1 ):
        url = crwlingJob.pop()
        crawlingGoogle(url)

def workToMultiThread(crwlingJob:list , threadCount : int ) :
    processName = current_process().name
    maxThreadCount = threadCount
    print("{} thread working Count : {}".format(processName, len(crwlingJob)))
    threadlist: List[Thread] = []
    allThreadList: List[Thread] = []
    threadIndex = 1 
    while( len(crwlingJob) >= 1 ):
        if len(threadlist) >= maxThreadCount :
            # 전체 내역중에 종료된 내역이 있는지 체크.
            threadlist = list(filter( filteredAliveThread , threadlist))
        else :
            url = crwlingJob.pop()
            workThread = Thread(target=crawlingGoogle , name="{} [{}th thread ]".format(processName, threadIndex), args=(url,))
            threadIndex += 1 
            threadlist.append(workThread)
            allThreadList.append(workThread)
            workThread.start()
            
    for thread in allThreadList:
        thread.join()
            

load_dotenv()
host = os.environ.get("HOST")
database = os.environ.get("DATABASE")
user_name = os.environ.get("DATABASE_USER")
password = os.environ.get("DATABASE_USER_PASS")

openDB: OpenDB = OpenDB(host, user_name ,password, database)
googleStoreRepository:AppStoreRepository = AppStoreRepository(openDB)

if __name__  == '__main__' :
    MAX_PROCESS_COUNT = 6
    THREAD_COUNT = 100
    start = time.time()
    offset = 0
    limit = 4000
    # Google MarketNum
    marketNum = 1 
    appList = googleStoreRepository.findNoNameAppLimitedTo(marketNum, offset, limit)
    if type(appList) == list:
        mappingAppEntityId : Callable[[AppEntity], str] = lambda t : t.getId() 
        crwlingJob = list(map( mappingAppEntityId , appList ) )
    else :
        print("조회결과 없음 {} {} {} ".format(marketNum, offset, limit))
        exit()
    jobCount = len(crwlingJob)
    jobLengthEachProcess = max( jobCount % MAX_PROCESS_COUNT, int(jobCount / MAX_PROCESS_COUNT))
    processList: List[Process] = []
    startPoint = 0 
    print("Process : {}  total job length : {} each work : {} ".format(MAX_PROCESS_COUNT, jobCount, jobLengthEachProcess ))
    print("총 {} 건 작업 시작~ ".format(len(crwlingJob)) )
    if len(crwlingJob) > jobLengthEachProcess :
        processNum = 1
        while len(crwlingJob) > 0 and len(processList) < MAX_PROCESS_COUNT :
            processJob = crwlingJob[:jobLengthEachProcess]
            if len(processJob) > 0 : 
                del crwlingJob[:jobLengthEachProcess]
                print (processJob)
                processList.append( Process(target=workToMultiThread , name="[ {}th process ]".format(processNum), args=(processJob, THREAD_COUNT) ))
                processNum += 1 
    else :
        processList.append( Process(target=workToMultiThread , name="[ 0th process ]", args=(crwlingJob, THREAD_COUNT)))
    
    print("processlist Count {}".format(len(processList)))

    for process in processList:
        process.start()
        print(process.name + " >> {}".format("LIVE" if process.is_alive() else "DIE"))
    
    for process in processList:
        process.join()
        print(process.name + " >> {}".format("LIVE" if process.is_alive() else "DIE"))

    print("Time : {}  ".format(time.time() - start  ))