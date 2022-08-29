import sys, rootpath
from module.EnvStore import EnvStore
from module.OpenDB_v3 import OpenDB
from repository.AppStoreRepository import AppStoreRepository
sys.path.append(rootpath.detect())
from service.MobileIndexService import MobileIndexService
from module.TimeChecker import TimeChecker
    
if __name__  == '__main__' :
    
    Env = EnvStore()
    appStore = Env.getAppStore
    openDB: OpenDB = OpenDB(appStore["host"], appStore["user_name"]  ,appStore["password"] , appStore["database"] )
    appStoreRepository:AppStoreRepository = AppStoreRepository(dbManager=openDB)
          
    timeChecker = TimeChecker()
    timeChecker.start(code="main")
    package = "com.kbcard.cxh.appcard"
    mobileIndexService =  MobileIndexService(appStoreRepository=appStoreRepository)
    mobileIndexService.marketInfoSave(package=package)

    timeChecker.stop(code="main")
    timeChecker.display(code="main")