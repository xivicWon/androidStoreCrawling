
import unittest
import sys, rootpath
sys.path.append(rootpath.detect())
from entity.AppEntity import AppEntity
from module.EnvManager import EnvManager

from module.OpenDB_v3 import OpenDB
from repository.AppStoreRepository import AppStoreRepository

class TestRepository(unittest.TestCase):
    appStoreRepository:AppStoreRepository
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        Env = EnvStore()
        appStore = Env.getAppStore
        openDB: OpenDB = OpenDB(appStore["host"], appStore["user_name"]  ,appStore["password"] , appStore["database"] )
        self.appStoreRepository:AppStoreRepository = AppStoreRepository(dbManager=openDB)
        
        
    def test_findAppId(self):
        result = self.appStoreRepository.findAppById(market_num=1, id="com.myung.snsday")
        
        self.assertEqual(AppEntity , type(result))
        
    def test_findAll(self):
        result = self.appStoreRepository.findAppByUndefinedName(market_num=1)
        self.assertEqual(list , type(result))
        self.assertGreaterEqual(a=len(result) ,b=1000 )
        
if __name__ == "__main__":
    unittest.main()