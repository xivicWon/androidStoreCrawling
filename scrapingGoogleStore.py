# -*- coding: utf-8 -*-
import sys, rootpath
sys.path.append(rootpath.detect())
from repository.AppStoreRepository import AppStoreRepository
from service.GoogleScrapService import GoogleScrapService 
from module.OpenDB_v3 import OpenDB
from module.EnvManager import EnvManager 
from module.TimeChecker import TimeChecker
from module.MultiProcessThread import MultiProcessThread
from module.LogManager import LogManager
def main() :
    
    envManager = EnvManager()
    openDB: OpenDB = OpenDB(envManager.DB_HOST, envManager.DB_USER ,envManager.DB_PASSWORD ,envManager.DB_DATABASE )
    appStoreRepository:AppStoreRepository = AppStoreRepository(dbManager=openDB)
    appScrapService:GoogleScrapService = GoogleScrapService(repository=appStoreRepository)        
    
    multiProcess = MultiProcessThread( 
        processCount=PROCESS_COUNT ,
        maxThreadCount=MAX_THREAD_COUNT ,
        supplier=appScrapService.threadProductor
    )
    
    offset:int = 0
    limit:int = 100
    LogManager.info("마켓정보 Google / 프로세스 {} / 최대 쓰레드 {}".format( PROCESS_COUNT, MAX_THREAD_COUNT ))
    LogManager.info("전체 정보 조외 / Offset {} / Limit {}".format( offset, limit ))
    multiProcess.addThreadJob(appScrapService.requestWorkListFromDB(MARKET_NUM , offset=offset, limit=limit))
    # multiProcess.addThreadJob(appScrapService.requestWorkListFromDBTest(MARKET_NUM , "com.myung.snsday"))
    multiProcess.setConsumer(consumer=appScrapService.consumerProcess) 
    multiProcess.run()

if __name__  == '__main__' :
    PROCESS_COUNT = 5
    MAX_THREAD_COUNT = 100
    MARKET_NUM = 1 
    
    timeChecker = TimeChecker()
    timeChecker.start(code="main")
    main()
    timeChecker.stop(code="main")
    timeChecker.display(code="main")