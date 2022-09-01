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
    openDB: OpenDB = OpenDB(envManager.DB_HOST, envManager.DB_USER ,envManager.DB_PASSWORD ,envManager.DB_DATABASE, logModule=logManager)
    appStoreRepository:AppStoreRepository = AppStoreRepository(dbManager=openDB, logModule=logManager)
    appScrapService:AppleScrapService = AppleScrapService(repository=appStoreRepository, logModule=logManager)      
    
    multiProcess = MultiProcessThread( 
        processCount=PROCESS_COUNT ,
        maxThreadCount=MAX_THREAD_COUNT ,
        supplier=appScrapService.threadProductor
    )
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