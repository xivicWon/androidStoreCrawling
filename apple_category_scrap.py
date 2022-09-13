import sys, rootpath

sys.path.append(rootpath.detect())
from repository.AppStoreRepository import AppStoreRepository
from service.AppleScrapService import AppleScrapService 
from module.OpenDB_v3 import OpenDB
from module.EnvManager import EnvManager 
from module.LogManager import LogManager
from module.TimeChecker import TimeChecker
from module.MultiProcessThread import MultiProcessThread

def main() :
    envManager = EnvManager.instance()
    logManager = LogManager.instance()
    openDB: OpenDB = OpenDB(
        host=envManager.DB_HOST, 
        username=envManager.DB_USER , 
        password=envManager.DB_PASSWORD , 
        database=envManager.DB_DATABASE,
        logModule=logManager)
    appStoreRepository:AppStoreRepository = AppStoreRepository(dbManager=openDB, logModule=logManager)
    appScrapService:AppleScrapService = AppleScrapService(repository=appStoreRepository)      
    
    multiProcess = MultiProcessThread( 
        processCount=PROCESS_COUNT ,
        maxThreadCount=MAX_THREAD_COUNT ,
        supplier=appScrapService.threadProductor
    )
    
    logManager.info("마켓정보 Apple / 프로세스 {0:,} / 최대 쓰레드 {0:,}".format( PROCESS_COUNT, MAX_THREAD_COUNT ))
    multiProcess.addThreadJob(appScrapService.requestWorkListFromDB(MARKET_NUM))
    multiProcess.setConsumer(consumer=appScrapService.consumerProcess) 
    multiProcess.run()

if __name__  == '__main__' :
    PROCESS_COUNT = 5
    MAX_THREAD_COUNT = 100
    MARKET_NUM = 2 
    timeChecker = TimeChecker()
    timeChecker.start(code="main")
    main()
    timeChecker.stop(code="main")
    timeChecker.display(code="main")