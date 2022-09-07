import os
import sys, rootpath
sys.path.append(rootpath.detect())

import requests, json
from dto.ErrorDto import ErrorCode, ErrorDto
from repository.Repository import Repository
from service.Service import Service
from urllib import error as UrllibError
from typing import  Callable, List, Optional
from bs4 import BeautifulSoup as bs
from multiprocessing import Queue
from dto.Dto import Dto
from dto.AppDto import AppDto
from dto.AppWithDeveloperWithResourceDto import AppWithDeveloperWithResourceDto
from dto.RequestDto import RequestDto
from dto.htmlDom.Tag_A import Tag_A
from entity.AppEntity import AppEntity
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from entity.AppResourceEntity import AppResourceEntity
from module.EnvManager import EnvManager
from module.LogManager import LogManager
from module.Curl import Curl, CurlMethod
from module.TimeChecker import TimeChecker
from exception.TooManyRequest import TooManyRequest


class GoogleScrapService(Service) : 
    __MARKET_NUM:int = 1  
    __MAX_RETRY_COUNT:int = 3 
    __repository:Repository
    __UNDEFINED_APP_NAME: str = "undefined-app"
    __PACKAGE_URL:str = "https://play.google.com/store/apps/details?id="
    
    def __init__(self,repository:Repository) -> None:
        super().__init__()
        print("-----GoogleScrapService.__init__")
        self.__repository = repository
        pass
            
    def requestWorkListFromDB( self, marketNum:int, offset:int , limit:int ) :
        appList = self.__repository.findNoNameAppLimitedToRecently(marketNum,offset , limit)
        crwlingJob:List[str] = []
        if type(appList) == list:
            for appEntity in appList :
                url = self.__PACKAGE_URL + appEntity.getId
                crwlingJob.append(url)
        else :
            msg = "조회된 스크랩대상 데이터가 없음 {} ".format(marketNum)
            print(msg)
            exit()
        return crwlingJob
    
    
    def requestWorkListFromDBTest( self, marketNum:int, ids:List[str] ) :
        # appList = [self.__repository.findAppById(marketNum, id)]
        crwlingJob:List[str] = []
        for id in ids:
            url = self.__PACKAGE_URL + id
            crwlingJob.append(url)
        # if type(appList) == list:
        #     for appEntity in appList :
        #         url = self.__PACKAGE_URL + appEntity.getId
        #         crwlingJob.append(url)
        # else :
        #     msg = "조회된 스크랩대상 데이터가 없음 {} ".format(marketNum)
        #     print(msg)
        #     exit()
        return crwlingJob
    
    def threadProductor(self, requestUrl : str, processStack:List[Dto], errorStack:List[Dto]):
        repeatCount = 0
        try:
            self.requestUrl(requestUrl, processStack, errorStack )
        except requests.exceptions.ReadTimeout: 
            repeatCount+= 1 
            if repeatCount < self.__MAX_RETRY_COUNT :
                self.requestUrl(requestUrl, processStack, errorStack)
            else : 
                errorStack.append(ErrorDto.build(ErrorCode.REQUEST_READ_TIMEOUT , requestUrl))
        except requests.exceptions.ConnectionError: 
            errorStack.append(ErrorDto.build(ErrorCode.REQUEST_CONNECTION_ERROR , requestUrl))
        except requests.exceptions.ChunkedEncodingError:
            errorStack.append(ErrorDto.build(ErrorCode.CHUNKED_ENCODING_ERROR , requestUrl))
        except AttributeError:
            errorStack.append(ErrorDto.build(ErrorCode.CHUNKED_ENCODING_ERROR , requestUrl))
        except UrllibError.URLError :
            errorStack.append(ErrorDto.build(ErrorCode.URL_OPRN_ERROR , requestUrl))
        except TooManyRequest : 
            errorStack.append(ErrorDto.build(ErrorCode.TOO_MANY_REQUEST , requestUrl))

    def requestUrl(self, requestUrl : str,  processStack:List[Dto], errorStack:List[Dto]) :
        header = {"Accept-Language" : "ko-KR"}
        res:requests.Response = Curl.request(method=CurlMethod.GET, url=requestUrl, headers=header, data=None)
        data = RequestDto(requestUrl, res)
        if res.status_code == 404 :
            emptyData:dict = {}
            emptyData["id"] =  data.getUrl().split("?id=")[1]
            emptyData["is_active"] = "N"
            processStack.append(self.mappingInactiveDto(emptyData))
        elif res.status_code == 429:
            raise TooManyRequest(requestUrl)
        else :
            try : 
                appWithDeveloperEntityList = self.singleDomParser(data.getResponse())
                if type(appWithDeveloperEntityList) == AppWithDeveloperWithResourceDto :
                    processStack.append(appWithDeveloperEntityList)
                else :
                    msg = "getResponse Fail : {}".format(requestUrl)
                    errorStack.append(ErrorDto.build(ErrorCode.RESPONSE_FAIL , msg))
            except AttributeError   :
                msg =  "getResponse Fail : {}".format(requestUrl)
                errorStack.append(ErrorDto.build(ErrorCode.ATTRIBUTE_ERROR , msg))
            except TypeError  :
                msg = "getResponse Fail : {}".format(requestUrl)
                errorStack.append(ErrorDto.build(ErrorCode.TYPE_ERROR , msg))
                
                
    @staticmethod
    def filterDeveloperId( obj) :
        href = Tag_A.of(obj).getHref
        return href.startswith("/store/apps/dev") or href.startswith("/store/apps/dev")
    
    def singleDomParser(self, response:requests.Response )->AppWithDeveloperWithResourceDto:
        appWithDeveloperWithResourceDto:AppWithDeveloperWithResourceDto
        try : 
            soup = bs(response.text, "html.parser")
            data = json.loads(soup.find('script', type='application/ld+json').text)
        except AttributeError as e : 
            msg = "AttributeError] Response [status code : {} , url : {}, data : {} ]".format(response.status_code , response.url, data )
            raise AttributeError(msg)
        except TypeError as e : 
            msg = "TypeError] Response [status code : {} , url : {}, data : {}  ]".format(response.status_code , response.url, data)
            raise TypeError(msg)
            
        data["id"] = response.url.split("id=").pop()
        try : 
            aTags = soup.find_all("a")
            filteredATag = next(filter( GoogleScrapService.filterDeveloperId , aTags) , None) 
            developerIDUrl = Tag_A().of(filteredATag).getHref
            if type(developerIDUrl) == str : 
                data["author"]["id"] = developerIDUrl.split("?id=")[1]
            else :
                data["author"]["id"] = 0
        except TypeError as e : 
            msg = "TypeError] Response [status code : {} , url : {}, data : {}  ]".format(response.status_code , response.url, data)
            raise TypeError(msg)
        
        appWithDeveloperWithResourceDto = (self.mappingDto(data))
        return appWithDeveloperWithResourceDto
    
    def mappingInactiveDto(self, data:dict ):
        appDto = AppDto().ofGoogleInActive(data)
        
        appMarketDeveloperEntity = None
        
        appEntity = AppEntity()\
            .setAppName(self.__UNDEFINED_APP_NAME)\
            .setId(appDto.getAppId())\
            .setDeveloperNum(0)\
            .setMarketNum(self.__MARKET_NUM)\
            .setIsActive("N")\
            .setRating(0)\
            .setLastUpdateCurrent()
            
        appResourceEntity = None
        
        return AppWithDeveloperWithResourceDto()\
            .setAppEntity(appEntity)\
            .setAppMarketDeveloperEntity(appMarketDeveloperEntity)\
            .setAppResourceEntity(appResourceEntity)
            
    def mappingDto (self, data:dict ):
        appDto = AppDto().ofGoogle(data)
        
        appMarketDeveloperEntity = AppMarketDeveloperEntity()\
            .setDeveloperMarketId(appDto.getDeveloperId())\
            .setDeveloperName(appDto.getDeveloperName())\
            .setMarketNum(self.__MARKET_NUM)\
            .setCompanyNum(0)
            
        appEntity = AppEntity()\
            .setAppName(appDto.getAppName())\
            .setId(appDto.getAppId())\
            .setDeveloperNum(0)\
            .setMarketNum(self.__MARKET_NUM)\
            .setIsActive("Y")\
            .setRating(appDto.getAppRating())\
            .setLastUpdateCurrent()
            
        directory = "./resource/google"
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        appResourceEntity = AppResourceEntity()\
            .setAppNum(0)\
            .setResourceType("icon")\
            .setPath(AppDto.downloadImg(downloadLink=appDto.appImage, toDirectory="./resource/google", fileName=appEntity.getId))
            
        return AppWithDeveloperWithResourceDto()\
            .setAppEntity(appEntity)\
            .setAppMarketDeveloperEntity(appMarketDeveloperEntity)\
            .setAppResourceEntity(appResourceEntity)

    def consumerProcess(self, q: Queue):
        envManager = EnvManager.instance()
        logManager = LogManager.instance()
        logManager.init(envManager)
        responseResults:List[AppWithDeveloperWithResourceDto] = []
        while ( True ):
            resultData = q.get()
            if( resultData == "None"):
                break
            elif type(resultData) == list :
                for value in resultData:
                    if type(value) == ErrorDto:
                        logManager.error(value.toLog())
                    else :        
                        responseResults.append(value)
            else : 
                print(resultData)
        if len(responseResults) > 0 :
            self.updateResponseToRepository(responseResults)
        
    def saveDeveloperInfo(self, dtos : List[AppWithDeveloperWithResourceDto]):
        appMarketDeveloperEntities:List[AppMarketDeveloperEntity] = []
        condition: Callable[[AppWithDeveloperWithResourceDto] , Optional[AppMarketDeveloperEntity]] = lambda dto : dto.getAppMarketDeveloperEntity
        conditionWithoutNone: Callable[[AppMarketDeveloperEntity], AppMarketDeveloperEntity ] = lambda e : type(e) == AppMarketDeveloperEntity
        appMarketDeveloperEntities = list(filter( conditionWithoutNone, map(condition ,dtos)))
       
        if len(appMarketDeveloperEntities) > 0 :
            self.__repository.saveBulkDeveloper(appMarketDeveloperEntities)
        return appMarketDeveloperEntities
    
    def saveAppEntities(self, dtos: List[AppWithDeveloperWithResourceDto], findAllAppMarketDeveloperEntities) :
        envManager = EnvManager.instance()
        logManager = LogManager.instance()
        logManager.init(envManager)
        appEntities:List[AppEntity] = []
        for dto in dtos :
            appEntity = dto.getAppEntity
            if appEntity.getIsActive == 'Y' :
                appMarketDeveloperEntity = dto.getAppMarketDeveloperEntity
                filterDeveloperEntity:Callable[[AppMarketDeveloperEntity] , bool] = lambda t : t.getDeveloperMarketId == appMarketDeveloperEntity.getDeveloperMarketId
                findOneAppMarketDeveloperEntity:AppMarketDeveloperEntity = next(filter( filterDeveloperEntity, findAllAppMarketDeveloperEntities), None)
                if findOneAppMarketDeveloperEntity == None:
                    msg = "Error [Not Found AppMarketDeveloperEntity] : {}".format(appMarketDeveloperEntity.toString())
                    logManager.error(msg)
                    continue
                appEntity.setDeveloperNum(findOneAppMarketDeveloperEntity.getNum)
            appEntities.append(appEntity)
        
        if len(appEntities) == 0 :
            return None
        self.__repository.saveBulkApp(appEntities)
        return appEntities
        
        
    def updateResponseToRepository(self, dtos : List[AppWithDeveloperWithResourceDto]):
        
        timeChecker = TimeChecker()
        envManager = EnvManager.instance()
        logManager = LogManager.instance()
        logManager.init(envManager)
        print("{0:,} 건에 대한 등록을 진행합니다.".format(len(dtos))) 
        
        #1. developer 등록 및 번호조회 saveDeveloperInfo
        timeChecker.start(code="Repository-Developer")
        appMarketDeveloperEntities = self.saveDeveloperInfo(dtos)
        timeChecker.stop(code="Repository-Developer")
        
        #2. app 등록 및 번호조회 
        timeChecker.start(code="Repository-App")
        findAllAppMarketDeveloperEntities = self.__repository.findAllDeveloperByDeveloperMarketId(appMarketDeveloperEntities)  
        appEntities:List[AppEntity] = []
        for dto in dtos :
            appEntity = dto.getAppEntity
            if appEntity.getIsActive == 'Y' :
                appMarketDeveloperEntity = dto.getAppMarketDeveloperEntity
                filterDeveloperEntity:Callable[[AppMarketDeveloperEntity] , bool] = lambda t : t.getDeveloperMarketId == appMarketDeveloperEntity.getDeveloperMarketId
                findOneAppMarketDeveloperEntity:AppMarketDeveloperEntity = next(filter( filterDeveloperEntity, findAllAppMarketDeveloperEntities), None)
                if findOneAppMarketDeveloperEntity == None:
                    msg = "Error [Not Found AppMarketDeveloperEntity] : {}".format(appMarketDeveloperEntity.toString())
                    logManager.error(msg)
                    logManager.error("getDeveloperMarketId %s " % appMarketDeveloperEntity.getDeveloperMarketId)
                    logManager.error("getDeveloperName %s" % appMarketDeveloperEntity.getDeveloperName)
                    continue
                appEntity.setDeveloperNum(findOneAppMarketDeveloperEntity.getNum)
            appEntities.append(appEntity)
        
        if len(appEntities) == 0 :
            return None
        self.__repository.saveBulkApp(appEntities)
        # findAllAppEntities = self.__repository.findAllApp(appEntities)
                
        #3. resource 등록 
        # AppResourceEntities:List[AppResourceEntity] = []
        # for dto in dtos :
        #     appResourceEntity = dto.getAppResourceEntity
        #     if appResourceEntity != None : 
        #         appEntity = dto.getAppEntity
        #         filterAppEntity:Callable[[AppEntity] , bool] = lambda t : t.getId == appEntity.getId
        #         findOneAppEntity:AppEntity = next(filter(filterAppEntity, findAllAppEntities), None)
        #         if findOneAppEntity == None :
        #             msg = "Error [Not Found AppEntity] : {}".format(appEntity.toString())
        #             logManager.error(msg)
        #             continue
        #         appResourceEntity.setAppNum(findOneAppEntity.getNum)
        #         AppResourceEntities.append(appResourceEntity)
            
        timeChecker.stop(code="Repository-App")
        
        timeChecker.start(code="Repository-Resource")
        # self.__repository.saveResourceUseBulk(AppResourceEntities)    
        timeChecker.stop(code="Repository-Resource")
        
        timeChecker.display(code="Repository-Developer")
        timeChecker.display(code="Repository-App")
        timeChecker.display(code="Repository-Resource")
        