from cProfile import label
import json
from multiprocessing import Queue
from typing import Callable, List

from dto.AppWithDeveloperWithResourceDto import AppWithDeveloperWithResourceDto
from dto.Dto import Dto
from dto.ErrorDto import ErrorDto
from dto.ThreadJobDto import ThreadJobDto
from dto.mobileIndex.MIMarketInfoDto import MIMarketInfoDto
from dto.mobileIndex.MIRequestDto import MIRequestDto
from entity.AppEntity import AppEntity
from repository.AppStoreRepository import AppStoreRepository
from service.Service import Service
from module.Curl import Curl, CurlMethod
from module.LogModule import LogModule
from module.EnvManager import EnvManager
from module.LogManager import LogManager
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
            self.__log.error("MobileIndexService - [Forbidden] - 403 - {}".format(json.dumps(dto.toDict())))
            return 
        else : 
            self.__log.error("MobileIndexService - {} - {}".format(response.status_code, json.dumps(dto.toDict())))
            return 
        
        ranks = responseData["data"]
        
        for app in ranks : 
            if "market_name" not in app or self.isOneStoreApp(app["market_name"]):
                continue
            elif self.isAppleStoreApp(app["market_name"]) : 
                mIMarketInfoDto = MIMarketInfoDto()
                mIMarketInfoDto.generateMappingCode()
                mIMarketInfoDto.setPackageName(app["package_name"])
                mIMarketInfoDto.setAppId("id" + app["market_appid"])
                appEntities.append(mIMarketInfoDto.toAppleAppEntity())
                appEntities.append(mIMarketInfoDto.toGoogleAppEntity())
    
    def isOneStoreApp(self, appStoreName:str ):
        return appStoreName == "one"
    
    def isAppleStoreApp(self, appStoreName:str ):
        return appStoreName == "apple"
    
    def isGoogleStoreApp(self, appStoreName:str ):
        return appStoreName == "google"
    
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
        self.__log.info("insert/update Count : {} / {}".format(len(saveAppEntities), len(appEntities)))
        self.__appStoreRepository.saveAppMappingUseBulk(saveAppEntities)
        
    
    def threadProducer(self, threadJobDto : ThreadJobDto, processStack:List[Dto], errorStack:List[Dto]):
        package = threadJobDto.getUrl
        mIMarketInfoDto = self.__getGoogleMarket(package=package)     
        processStack.append(mIMarketInfoDto.toAppleAppEntity())
        processStack.append(mIMarketInfoDto.toGoogleAppEntity())
        
        
    def consumerProcess(self, q: Queue):
        envManager = EnvManager.instance()
        logManager = LogManager.instance()
        logManager.init(envManager)
        responseResults:List[AppWithDeveloperWithResourceDto] = []
        while ( True ):
            try :
                resultData = q.get()
            except ValueError as e :
                logManager.error("ERROR : {} {}".format(e, resultData))
                continue
            if( resultData == "None"):
                break
            elif type(resultData) == list :
                for value in resultData:
                    if type(value) == ErrorDto:
                        logManager.byErrorDto(value)
                    else :        
                        responseResults.append(value)
            else : 
                logManager.error("consumerProcess > check undefined data : {}".format(resultData))
                
        if len(responseResults) > 0 :
            self.updateResponseToRepository(responseResults)
    
    
    def updateResponseToRepository (self, data:List[AppEntity]):
        for d in data :
            print("{} -> {}".format(d.getId, d.getMappingCode))
            
        self.__appStoreRepository.saveAppMappingUseBulk(bulkResources=data)