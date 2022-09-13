import json
import requests
from typing import Callable, List
from dto.mobileIndex.MIMarketInfoDto import MIMarketInfoDto
from dto.mobileIndex.MIRequestDto import MIRequestDto
from entity.AppEntity import AppEntity
from repository.AppStoreRepository import AppStoreRepository
from service.Service import Service
from module.Curl import Curl, CurlMethod
from module.LogModule import LogModule

class MobileIndexService (Service): 
    __DOMAIN:str =  "https://www.mobileindex.com"
    __REFERER:str = "https://www.mobileindex.com/mi-chart/daily-rank"
    __CONTENT_TYPE : str = "application/x-www-form-urlencoded"
    __global_rank_v2:str =  "/api/chart/global_rank_v2"
    __market_info:str =  "/api/app/market_info"
    __appStoreRepository :AppStoreRepository 
    __log: LogModule
    def __init__(self, appStoreRepository, logModule:LogModule ):
        self.__appStoreRepository = appStoreRepository
        self.__log = logModule 
        pass

    def __getJsonToMobileIndex(self, data ) -> dict : 
        headers = {
            'Content-Type': self.__CONTENT_TYPE,
            'referer':  self.__REFERER
        }
        url = self.__DOMAIN + self.__market_info
        response = Curl.request(
            method=CurlMethod.POST,
            headers=headers,
            url=url,
            data=data
        )
        if response.status_code == 200 :
            return response.json()        
        else :
            raise Exception("Web Response Status Code : {}".format(response.status_code))    
        
    def __getGoogleMarket(self, package) -> MIMarketInfoDto:
        data = self.__getJsonToMobileIndex({
            "packageName" : package
        })
        return MIMarketInfoDto().ofDict(data)
    
    def marketInfoSave(self, package) : 
        mIMarketInfoDto = self.__getGoogleMarket(package=package)     
        
        print("{} - {} - {}".format(mIMarketInfoDto.getPackageName, mIMarketInfoDto.getAppId , mIMarketInfoDto.getMappingCode))   
        
        self.__appStoreRepository.insertAppMappingCode(appEntity=mIMarketInfoDto.toAppleAppEntity())
        self.__appStoreRepository.insertAppMappingCode(appEntity=mIMarketInfoDto.toGoogleAppEntity())
    
    def getGlobalRank(self, dto:MIRequestDto, appEntities:List[AppEntity]):
        headers = {
            'Content-Type':  self.__CONTENT_TYPE,
            'referer': self.__REFERER,
        }
        url = self.__DOMAIN + self.__global_rank_v2
        response = Curl.request (
            method = CurlMethod.POST,
            headers=headers,
            url=url,
            data=dto.toDict()
        )
        
        if response.status_code == 200 :
            responseData = response.json() 
        elif response.status_code == 403:
            self.__log.error("MobileIndexService - [Forbidden Error] - 403 - {}".format(json.dumps(dto.toDict())))
            return 
        else : 
            self.__log.error("MobileIndexService - [ Error] - {} - {}".format(response.status_code, json.dumps(dto.toDict())))
            return 
        
        ranks = responseData["data"]
        for app in ranks : 
            try :
                if  app["market_name"] == "one" \
                    or app["package_name"] == None \
                    or app["package_name"] == app["market_appid"]:
                    continue
            except TypeError as e :
                print(e)
                continue
            mIMarketInfoDto = MIMarketInfoDto()
            mIMarketInfoDto.setPackageName(app["package_name"])
            mIMarketInfoDto.setAppId("id" + app["market_appid"])
            appEntities.append(mIMarketInfoDto.toAppleAppEntity())
            appEntities.append(mIMarketInfoDto.toGoogleAppEntity())
    
    def saveGlobalRank (self, appEntities:List[AppEntity]):
        AppIds:List[str] = []
        saveAppEntities:List[AppEntity] = []
        condition : Callable[[str], bool]  = lambda id : id == currentId 
        for appEntity in appEntities :
            currentId = appEntity.getId
            filtered = next(filter( condition, AppIds ), None)
            if filtered != None:
                continue
            saveAppEntities.append(appEntity)
            AppIds.append(currentId)
        self.__log.info("insert/update Count : {} / {}".format(len(saveAppEntities), len(AppIds)))
        self.__appStoreRepository.saveAppMappingUseBulk(saveAppEntities)