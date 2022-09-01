import rootpath
import sys
sys.path.append(rootpath.detect())

from entity.AppEntity import AppEntity
from module.EnvManager import EnvManager
from module.OpenDB_v3 import OpenDB
from repository.AppStoreRepository import AppStoreRepository


Env = EnvStore()
appStore = Env.getAppStore
openDB: OpenDB = OpenDB(appStore["host"], appStore["user_name"]  ,appStore["password"] , appStore["database"] )
appStoreRepository:AppStoreRepository = AppStoreRepository(openDB)

MARKET_NUM = 2 
appEntity = AppEntity().setMarketNum(MARKET_NUM).setId("id1436576616")

print(appEntity.toString())
findAppEntity = appStoreRepository.findAppById(appEntity.getMarketNum,  appEntity.getId)
if findAppEntity != None :
    print(findAppEntity.toString())
else :
    print("Not Found")

