import sys, rootpath
sys.path.append(rootpath.detect())
import requests, time, json
from typing import  Callable, List
from bs4 import BeautifulSoup as bs
from bs4.element import Tag
from requests import get
from threading import Thread, current_thread 
from multiprocessing import Process, Queue, current_process
from dto.AppDto import AppleAppDto
from dto.AppWithDeveloperWithResourceDto import AppWithDeveloperWithResourceDto
from dto.RequestDto import RequestDto
from entity.AppEntity import AppEntity
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from entity.AppResourceEntity import AppResourceEntity
from module.OpenDB_v3 import OpenDB
from repository.AppStoreRepository import AppStoreRepository
from module.EnvManager import EnvManager 

def curl(url:str)->requests.Response: 
    res = get(url, timeout=10)
    try :
        return res
    except requests.exceptions.ReadTimeout: 
        return None
    except requests.exceptions.ConnectionError: 
        return None
    except requests.exceptions.ChunkedEncodingError:
        return None


def workToThread(requestUrl : str,  obj:List[AppWithDeveloperWithResourceDto]):
    try:
        res:requests.Response = curl(requestUrl)
        data = RequestDto(id, res)
        appWithDeveloperEntityList = domParser(data.getResponse())
        if type(appWithDeveloperEntityList) == list :
            obj.extend(appWithDeveloperEntityList)
        else :
            print(current_thread().getName() + "getResponse Fail : {}".format(requestUrl))
    except requests.exceptions.ReadTimeout: 
        print(current_thread().getName() + "ReadTimeout request Fail : {}".format(requestUrl))
        return 
    except requests.exceptions.ConnectionError: 
        print(current_thread().getName() + "ConnectionError request Fail : {}".format(requestUrl))
        return 
    except requests.exceptions.ChunkedEncodingError:
        print(current_thread().getName() + "ChunkedEncodingError request Fail : {}".format(requestUrl))
        return 

def mappingDto (data:dict ):
    appleAppDto = AppleAppDto().ofDict(data)
    
    appMarketDeveloperEntity = AppMarketDeveloperEntity()\
        .setDeveloperMarketId(0)\
        .setDeveloperName(appleAppDto.getDeveloperName())\
        .setMarketNum(MARKET_NUM)\
        .setCompanyNum(0)
        
    appEntity = AppEntity()\
        .setAppName(appleAppDto.getAppName())\
        .setId(appleAppDto.getAppId())\
        .setDeveloperNum(0)\
        .setMarketNum(2)\
        .setIsActive("Y")\
        .setRating(appleAppDto.getAppRating())\
        .setLastUpdateCurrent()
        
    appResourceEntity = AppResourceEntity()\
        .setAppNum(0)\
        .setResourceType("icon")\
        .setPath(appleAppDto.downloadImg("./tmp/apple"))    
        
    return AppWithDeveloperWithResourceDto()\
        .setAppEntity(appEntity)\
        .setAppMarketDeveloperEntity(appMarketDeveloperEntity)\
        .setAppResourceEntity(appResourceEntity)

def domParser(response:requests.Response )->List[AppWithDeveloperWithResourceDto]:
    try : 
        soup = bs(response.text, "html.parser")
        scripts:List[Tag] = soup.findAll('script', type="fastboot/shoebox", id=lambda x : x and x.startswith('shoebox-kr-limit-100-genreId-'))
        if len(scripts) > 0 :
            listData = scripts[0].text
            data = json.loads(listData)
            parsingResult = []
            try : 
                if( type(data["chartsList"]["data"]) == list and len(data["chartsList"]["data"]) > 0 ):
                    for data in data["chartsList"]["data"] :
                        parsingResult.append(mappingDto(data))
                    return parsingResult
            except Exception as e : 
                print(e) 
        return None
    except AttributeError as e : 
        print(e)
        return None

def filteredAliveThread(t : Thread):
    if t.is_alive() :
        return True
    else :
        t.join()
        return False

def workToProcess(crwlingJob:list , maxThreadCount : int, q : Queue) :
    processName = current_process().name
    threadlist: List[Thread] = []
    allThreadList: List[Thread] = []
    resList:List[AppWithDeveloperWithResourceDto] = [] 
    threadIndex = 0 
    while( len(crwlingJob) >= 1 ):
        if len(threadlist) >= maxThreadCount :
            threadlist = list(filter( filteredAliveThread , threadlist))
        else :
            url = crwlingJob.pop()
            ## 여러개의 작업리스트를 전달하도록.
            threadIndex += 1 
            workThread = Thread(target=workToThread , name="{} [{}th thread ]".format(processName, threadIndex), 
                                args=(url, resList, ))
            threadlist.append(workThread)
            allThreadList.append(workThread)
            workThread.start()
            
    for thread in allThreadList:
        thread.join()
        
    q.put(resList)
        
        
def consumerProcess(q: Queue):
    responseResults:List[AppWithDeveloperWithResourceDto] = []
    while ( True ):
        value = q.get()
        if( value == "None"):
            break
        responseResults.extend(value)
    updateResponseToRepository(responseResults)
    
def updateResponseToRepository(dtos : List[AppWithDeveloperWithResourceDto]):
    ids:List[str] = []
    
    bulkResource:List[AppResourceEntity] = []
    
    for dto in dtos :
        currentId = dto.getAppEntity.getId
        condition : Callable[[str], bool]  = lambda id : id == currentId 
        filtered = next(filter( condition, ids ), None)
        if filtered != None:
            # print("{} 중복로 인한 패스!".format(currentId))
            continue
        
        ids.append(currentId)
        #1. developer 등록 및 번호조회
        result = appStoreRepository.findDeveloperByDeveloperMarketId(dto.getAppMarketDeveloperEntity)
        if( result == None ):
            try :
                developNum = appStoreRepository.saveDeveloper(dto.getAppMarketDeveloperEntity)
            except Exception as e : 
                print(e)
                exit()
        else :
            developNum = result.getNum
            
        #2. app 등록 및 번호조회
        appEntity = dto.getAppEntity
        findAppEntity = appStoreRepository.findAppById(appEntity.getMarketNum,  appEntity.getId)
        if findAppEntity != None :
            appNum = findAppEntity.getNum
        else :
            appEntity.setDeveloperNum(developNum)
            appNum = appStoreRepository.addApp(appEntity)
            
        #3. resource 등록 ( Bulk Insert 가능. )
        appResourceEntity = dto.getAppResourceEntity
        appResourceEntity.setAppNum(appNum)
        bulkResource.append(appResourceEntity)
        # appStoreRepository.saveResource(appResourceEntity)
        # Todo : 이미지는 중복등록을 방지하기 위한 처리가 필요함. 
        
    print("Bulk Insert Total : {}".format( len(bulkResource)))
    appStoreRepository.saveResourceUseBulk(bulkResource)    
        
    
def requestWorkListFromDB(appStoreRepository: AppStoreRepository, marketNum:int  ) :
    appMartetScrapList = appStoreRepository.findMarketScrapUrl(marketNum)
    crwlingJob:List[str] = []
    if type(appMartetScrapList) == list:
        for appMartetScrap in appMartetScrapList :
            urls = appMartetScrap.getScrapUrl()
            crwlingJob.extend(urls)
    else :
        print("조회된 스크랩대상 데이터가 없음 {} {} {} ".format(marketNum))
        exit()
    return crwlingJob[:2]

def main() :
    q = Queue()
    crwlingJob = requestWorkListFromDB(appStoreRepository, MARKET_NUM)
    jobCount = len(crwlingJob)
    jobLengthEachProcess = max( jobCount % MAX_PROCESS_COUNT, int(jobCount / MAX_PROCESS_COUNT))
    processList: List[Process] = []
    
    print("Process : {}  total job length : {} each work : {} ".format(MAX_PROCESS_COUNT, jobCount, jobLengthEachProcess ))
    print("총 {} 건 작업 시작~ ".format(len(crwlingJob)) )
    processNum = 0
    if len(crwlingJob) > 0:
        while len(crwlingJob) > 0:
            if len(processList) + 1 == MAX_PROCESS_COUNT:
                processJob = crwlingJob[:]
                del crwlingJob[:]
            else :
                processJob = crwlingJob[:jobLengthEachProcess]
                del crwlingJob[:jobLengthEachProcess]
                
            if len(processJob) > 0 : 
                processNum += 1 
                processList.append( Process(target=workToProcess , name="[ {}th process ]".format(processNum), args=(processJob, THREAD_COUNT, q ,) ))

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