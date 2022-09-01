import datetime
import sys, rootpath
from threading import Thread
from typing import List
from dto.mobileIndex.MIRequestDto import MIRequestDto
from entity.AppEntity import AppEntity
sys.path.append(rootpath.detect())
from service.MobileIndexService import MobileIndexService
from module.TimeChecker import TimeChecker
from module.EnvManager import EnvManager
from module.OpenDB_v3 import OpenDB
from repository.AppStoreRepository import AppStoreRepository
if __name__  == '__main__' :
    
    envManager = EnvManager()
    openDB: OpenDB = OpenDB(envManager.DB_HOST, envManager.DB_USER ,envManager.DB_PASSWORD ,envManager.DB_DATABASE )
    appStoreRepository:AppStoreRepository = AppStoreRepository(dbManager=openDB)
    
    
    timeChecker = TimeChecker()
    timeChecker.start(code="main")
    mobileIndexService = MobileIndexService(appStoreRepository=appStoreRepository)
    
    mIRequestDto = MIRequestDto()
    mIRequestDto.setMarket("all")
    mIRequestDto.setDate(datetime.datetime.now().strftime("%Y%m%d"))
    mIRequestDto.setStartRank(1)
    mIRequestDto.setEndRank(100)
    
    countries = ["kr", "asian" , "other"]
    rankTypes = ["gross", "free" , "paid"]
    appTypes = ["app", "game" , "other"]
    
    # countries = ["kr"]
    # rankTypes = ["gross"]
    # appTypes = ["app", "game"]
    appEntities:List[AppEntity] = []
    threadList:List[Thread] = []
    for country in countries :
        for rankType in rankTypes :
            for appType in appTypes : 
                mIRequestDto.setCounty(country)
                mIRequestDto.setRankType(rankType)
                mIRequestDto.setAppType(appType)
                thread = Thread(
                    target=mobileIndexService.getGlobalRank ,
                    args=(mIRequestDto, appEntities, )
                )
                threadList.append(thread)
                
    for t in threadList :
        t.start() 
        
    for t in threadList :
        t.join() 
        
    mobileIndexService.saveGlobalRank(appEntities)
    timeChecker.stop(code="main")
    timeChecker.display(code="main")