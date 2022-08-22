import sys, rootpath
sys.path.append(rootpath.detect())
import requests, time, json
from typing import  Callable, List
from bs4 import BeautifulSoup as bs
from bs4.element import Tag
from requests import get
from threading import Thread, current_thread 
from multiprocessing import Process, Queue, current_process
from dto.AppleAppDto import AppleAppDto
from dto.AppWithDeveloperWithResourceDto import AppWithDeveloperWithResourceDto
from dto.RequestDto import RequestDto
from entity.AppEntity import AppEntity
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from entity.AppResourceEntity import AppResourceEntity
from module.OpenDB_v3 import OpenDB
from repository.AppStoreRepository import AppStoreRepository
from module.EnvStore import EnvStore 
from module.Curl import Curl



def main() :
    q = Queue()
    appleScrap = AppleScrap()        
    
    crwlingJob = appleScrap.requestWorkListFromDB(appStoreRepository, MARKET_NUM)
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
                processList.append( Process(target=appleScrap.workToProcess , name="[ {}th process ]".format(processNum), args=(processJob, THREAD_COUNT, q ,) ))

    consumer = Process(target=appleScrap.consumerProcess , name="[ consumer process ]", args=(q,))
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