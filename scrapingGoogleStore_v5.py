import sys, rootpath

sys.path.append(rootpath.detect())
from repository.AppStoreRepository import AppStoreRepository
from service.GoogleScrapService import GoogleScrapService 
from module.OpenDB_v3 import OpenDB
from module.EnvStore import EnvStore 
from module.TimeChecker import TimeChecker
from module.MultiProcessThread import MultiProcessThread

def main() :
    Env = EnvStore()
    appStore = Env.getAppStore
    openDB: OpenDB = OpenDB(appStore["host"], appStore["user_name"]  ,appStore["password"] , appStore["database"] )
    appStoreRepository:AppStoreRepository = AppStoreRepository(dbManager=openDB)
    appScrapService:GoogleScrapService = GoogleScrapService(repository=appStoreRepository)        
    
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
    MARKET_NUM = 1 
    timeChecker = TimeChecker()
    timeChecker.start(code="main")
    main()
    timeChecker.stop(code="main")
    timeChecker.display(code="main")