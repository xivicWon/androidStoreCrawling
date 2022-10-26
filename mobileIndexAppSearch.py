import random
import sys, rootpath

sys.path.append(rootpath.detect())
from repository.AppStoreRepository import AppStoreRepository
from service.MobileIndexService import MobileIndexService
from module.TimeChecker import TimeChecker
from module.MultiProcessThread import MultiProcessThread
from module.EnvManager import EnvManager
from module.LogManager import LogManager
from module.OpenDB_v3 import OpenDB
    
    
def main() :
    envManager = EnvManager.instance()
    logManager = LogManager.instance()
    logManager.init(envManager)
    openDB: OpenDB = OpenDB(
        host=envManager.DB_HOST, 
        username=envManager.DB_USER , 
        password=envManager.DB_PASSWORD , 
        database=envManager.DB_DATABASE,
        logModule=logManager)
    appStoreRepository:AppStoreRepository = AppStoreRepository(dbManager=openDB, logModule=logManager )
    appStoreRepository.insertAppScanningForMapping()
    
    mobileIndexService = MobileIndexService(appStoreRepository=appStoreRepository, logModule=logManager)
    multiProcess = MultiProcessThread( 
        processCount=PROCESS_COUNT ,
        maxThreadCount=MAX_THREAD_COUNT ,
        supplier=mobileIndexService.threadProducer
    )
    
    offset:int = 0
    limit:int = random.randrange(1,500)
    limit:int = 100
    logManager.info("Market : Google / Process : {0:,} / Maximun Thread : {0:,}".format( PROCESS_COUNT, MAX_THREAD_COUNT ))
    logManager.info("Offset {0:,} / Limit {0:,}".format( offset, limit ))
    multiProcess.addThreadJob(mobileIndexService.getThreadJobOfNoMappingApps(MARKET_NUM , offset=offset, limit=limit))
    multiProcess.setConsumer(consumer=mobileIndexService.consumerProcess) 
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