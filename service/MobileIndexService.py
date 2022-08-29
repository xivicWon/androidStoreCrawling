import json
from typing import Callable, List
from dto.mobileIndex.MIMarketInfoDto import MIMarketInfoDto
from dto.mobileIndex.MIRequestDto import MIRequestDto
from entity.AppEntity import AppEntity
from repository.AppStoreRepository import AppStoreRepository
from service.Service import Service
from module.Curl import Curl

class MobileIndexService (Service): 
    
    __REFERER:str = "https://www.mobileindex.com"
    __DOMAIN:str =  "https://www.mobileindex.com"
    __global_rank_v2:str =  "/api/chart/global_rank_v2"
    __market_info:str =  "/api/app/market_info"
    __appStoreRepository :AppStoreRepository 
    
    def __init__(self, appStoreRepository):
        self.__appStoreRepository = appStoreRepository
        pass

    def __getJsonToMobileIndex(self, data ) -> dict : 
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'referer':  self.__REFERER
        }
        url = self.__DOMAIN + self.__market_info
        response = Curl.request(
            method="post",
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
        self.__appStoreRepository.insertAppMappingCode(appEntity=mIMarketInfoDto.toAppleAppEntity())
        self.__appStoreRepository.insertAppMappingCode(appEntity=mIMarketInfoDto.toGoogleAppEntity())
    
    def getGlobalRank(self, dto:MIRequestDto, appEntities:List[AppEntity]):
        headers = {
            "referer":  self.__REFERER
        }
        url = self.__DOMAIN + self.__global_rank_v2
        data = Curl.request (
            method="post",
            headers=headers,
            data=json.dumps(dto.toDict()),
            url=url
        )
        responseData = data.json()
        if responseData["status"] :
            ranks = responseData["data"]
            for app in ranks : 
                if  app["market_name"] == "one" \
                    or app["package_name"] == None \
                    or app["package_name"] == app["market_appid"]:
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
        print( "insert Count : {}".format(len(saveAppEntities)))
        self.__appStoreRepository.saveAppMappingUseBulk(saveAppEntities)