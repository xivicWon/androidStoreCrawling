import sys, rootpath
from module.EnvManager import EnvManager
from module.OpenDB_v3 import OpenDB
from repository.AppStoreRepository import AppStoreRepository
sys.path.append(rootpath.detect())
from service.MobileIndexService import MobileIndexService
from module.TimeChecker import TimeChecker
    
if __name__  == '__main__' :
    
    envManager = EnvManager.instance()
    openDB: OpenDB = OpenDB(envManager.DB_HOST, envManager.DB_USER ,envManager.DB_PASSWORD ,envManager.DB_DATABASE )
    appStoreRepository:AppStoreRepository = AppStoreRepository(dbManager=openDB)
          
    timeChecker = TimeChecker()
    timeChecker.start(code="main")
    package = "com.kbcard.cxh.appcard"
    mobileIndexService =  MobileIndexService(appStoreRepository=appStoreRepository)
    mobileIndexService.marketInfoSave(package=package)

    timeChecker.stop(code="main")
    timeChecker.display(code="main")