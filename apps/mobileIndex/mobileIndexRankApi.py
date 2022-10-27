import datetime
import os, sys, rootpath
from threading import Thread
from typing import List
sys.path.append(rootpath.detect())
from dto.mobileIndex.MIRequestDto import MIRequestDto
from entity.AppEntity import AppEntity
from service.MobileIndexService import MobileIndexService
from module.TimeChecker import TimeChecker
from module.EnvManager import EnvManager
from module.OpenDB_v3 import OpenDB
from module.LogManager import LogManager
from repository.AppStoreRepository import AppStoreRepository


if __name__  == '__main__' :
    
    envManager = EnvManager.instance()
    logManager = LogManager.instance()
    logManager.init(envManager)
    
    logManager.info("##################################")
    logManager.info("# Start File : {} ".format(os.path.dirname(__file__) + __file__))
    logManager.info("##################################")

    openDB: OpenDB = OpenDB(
        host=envManager.DB_HOST, 
        username=envManager.DB_USER , 
        password=envManager.DB_PASSWORD , 
        database=envManager.DB_DATABASE,
        logModule=logManager)
    
    appStoreRepository:AppStoreRepository = AppStoreRepository(dbManager=openDB, logModule=logManager)
    mobileIndexService = MobileIndexService(appStoreRepository=appStoreRepository, logModule=logManager)
    timeChecker = TimeChecker()
    timeChecker.start(code="main")
    
    countries = ["kr", "asia", "other"]
    rankTypes = ["gross", "free", "paid"]
    appTypes = ["app", "game" ]
    
    appEntities:List[AppEntity] = []
    threadList:List[Thread] = []
    for country in countries :
        for rankType in rankTypes :
            for appType in appTypes : 
                mIRequestDto = MIRequestDto()
                if country == "kr" :
                    mIRequestDto.setMarket("all")
                else : 
                    mIRequestDto.setMarket("google")
                    
                yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
                mIRequestDto.setDate(yesterday.strftime("%Y%m%d"))
                mIRequestDto.setStartRank(1)
                mIRequestDto.setEndRank(100)
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