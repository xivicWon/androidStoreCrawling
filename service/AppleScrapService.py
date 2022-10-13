import datetime
import random
import sys, rootpath
import requests
sys.path.append(rootpath.detect())

from dto.ThreadJobDto import ThreadJobDto
from module.FileManager import FileManager
from typing import  Callable, List, Optional
from multiprocessing import Queue
from dto.Dto import Dto
from dto.AppWithDeveloperWithResourceDto import AppWithDeveloperWithResourceDto
from dto.RequestDto import RequestDto
from dto.ErrorDto import ErrorCode, ErrorDto
from entity.AppEntity import AppEntity
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from entity.AppResourceEntity import AppResourceEntity
from module.EnvManager import EnvManager
from module.LogManager import LogManager
from module.Curl import CurlMethod, Curl
from module.TimeChecker import TimeChecker
from module.DomParser import DomParser

from urllib import error as UrllibError
from exception.TooManyRequest import TooManyRequest

from repository.Repository import Repository
from service.Service import Service

class AppleScrapService(Service) : 
    __MARKET_NUM:int = 2 
    __repository:Repository
    __APPStore_URL:str = "https://apps.apple.com"
    __RESOURCE_DIR:str = "/images/apple"
    
    def __init__(self,repository:Repository) -> None:
        super().__init__()
        self.__repository = repository
        pass
        
    def getThreadJobOfAppleCategory( self ) :
        appMartetScrapList = self.__repository.findMarketScrapUrl(self.__MARKET_NUM)
        crwlingJob:List[str] = []
        if type(appMartetScrapList) == list:
            for appMartetScrap in appMartetScrapList :
                urls = appMartetScrap.getScrapUrl()
                crwlingJob.extend(urls)
        else :
            print("조회된 스크랩대상 데이터가 없음 {} {} {} ".format(self.__MARKET_NUM))
            exit()
            
        return list(map( lambda s: ThreadJobDto(url = s) , crwlingJob))
    
    def getScrapUrlLink( self, national,  appid ):
        return "/".join([self.__APPStore_URL, national , "app", appid])
        
    def getNoNameOrNoImageApps(self, offset:int , limit: int ) : 
        appList = self.__repository.findNoNameAppLimitedTo(self.__MARKET_NUM , offset , limit)
        crwlingJob:List[ThreadJobDto] = []
        if type(appList) != list:
            msg = "조회된 스크랩대상 데이터가 없음 {} ".format(self.__MARKET_NUM)
            print(msg)
            exit()
        
        for dto in appList :
            url = self.getScrapUrlLink(
                dto.getISOCountryCodeEntity.getAlpha2, 
                dto.getAppEntity.getId ) 
            resourceDir = self.__RESOURCE_DIR + "/" + FileManager.randomResourceSubDirectory()
            crwlingJob.append(ThreadJobDto(url = url, resourceDir = resourceDir, dto=dto))
        return crwlingJob
            
    def threadProducer(self, threadJobDto : ThreadJobDto,  processStack:List[Dto], errorStack:List[ErrorDto] ):
        url = threadJobDto.getUrl
        data = self.requestUrl(url, errorStack)
        if data == None:
            return
        
        res = data.getResponse
        if res.status_code == 200:
            if self.isCategoryURL(url):
                appWithDeveloperEntityList:List[AppWithDeveloperWithResourceDto] = DomParser.parseAppleCategory(res)
                if type(appWithDeveloperEntityList) == list :
                    processStack.extend(appWithDeveloperEntityList)
                else :
                    errorStack.append(ErrorDto.build(ErrorCode.RESPONSE_FAIL , url))
            else :
                
                FileManager.makeDirs(threadJobDto.getResourceDir)
                appDto = DomParser.parseAppleAppDetail(res)                
                result = DomParser.getAppWithDeveloperWithResourceDto (
                    appDto=appDto,
                    marketNum=self.__MARKET_NUM, 
                    resourceDirectory=threadJobDto.getResourceDir)
                processStack.append(result)
        elif res.status_code == 429:
            errorStack.append(ErrorDto.build(ErrorCode.TOO_MANY_REQUEST , url))
        elif res.status_code == 404:
            appId = url.split("/")[-1]
            processStack.append(DomParser.mappingInactiveDto(AppleScrapService.__MARKET_NUM, appId))
        else:
            raise requests.exceptions.ReadTimeout(url)
        
    def requestUrl(self, url : str,  errorStack:List[ErrorDto]):
        header = {"Accept-Language" : "ko-KR"}
        try :
            res:requests.Response = Curl.request(method=CurlMethod.GET, url=url, headers=header, data=None ,timeout=10)
            return RequestDto(url, res)
        except requests.exceptions.ReadTimeout: 
            errorStack.append(ErrorDto.build(ErrorCode.REQUEST_READ_TIMEOUT , "request URL : {}".format( url)))
        except requests.exceptions.ConnectionError: 
            errorStack.append(ErrorDto.build(ErrorCode.REQUEST_CONNECTION_ERROR , url))
        except requests.exceptions.ChunkedEncodingError:
            errorStack.append(ErrorDto.build(ErrorCode.CHUNKED_ENCODING_ERROR , url))
        except TooManyRequest:
            errorStack.append(ErrorDto.build(ErrorCode.TOO_MANY_REQUEST , url))
        except UrllibError.URLError :
            errorStack.append(ErrorDto.build(ErrorCode.URL_OPEN_ERROR , url))
        return None
    
    def isCategoryURL(self, url:str):
        return url.startswith("https://apps.apple.com/kr/charts")
    
    
    def consumerProcess(self, q: Queue):
        envManager = EnvManager.instance()
        logManager = LogManager.instance()
        logManager.init(envManager)
        responseResults:List[AppWithDeveloperWithResourceDto] = []
        while True:
            resultData = q.get()
            if( resultData == "None"):
                break
            elif type(resultData) == list and len(resultData) > 0:
                for value in resultData:
                    if isinstance( value, ErrorDto):
                        logManager.byErrorDto(value)
                    else :        
                        responseResults.append(value)
            else : 
                # FIXME: 로그로 작성.
                logManager.error("로그작성필요 : {}".format(resultData))
                
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
    
    def updateResponseToRepository(self, dtos : List[AppWithDeveloperWithResourceDto]):
        timeChecker = TimeChecker()
        envManager = EnvManager.instance()
        logManager = LogManager.instance()
        logManager.init(envManager)
        print("{0:,} 건에 대한 등록을 진행합니다.".format(len(dtos))) 
        
        #1. developer 등록 및 번호조회
        appMarketDeveloperEntities:List[AppMarketDeveloperEntity] = []
        timeChecker.start(code="Repository-Developer")
        appMarketDeveloperEntities = self.saveDeveloperInfo(dtos)
        timeChecker.stop(code="Repository-Developer")
        findAllAppMarketDeveloperEntities = self.__repository.findAllDeveloperByDeveloperMarketId(appMarketDeveloperEntities)  
        
        #2. app 등록 및 번호조회
        timeChecker.start(code="Repository-App")
        appEntities:List[AppEntity] = []
        for dto in dtos :
            appEntity = dto.getAppEntity
            appEntities.append(appEntity)
            appMarketDeveloperEntity = dto.getAppMarketDeveloperEntity
            if appEntity.getIsActive == 'Y' and appMarketDeveloperEntity != None :
                filterDeveloperEntity:Callable[[AppMarketDeveloperEntity] , bool] = lambda t : t.getDeveloperMarketId == appMarketDeveloperEntity.getDeveloperMarketId
                findOneAppMarketDeveloperEntity:AppMarketDeveloperEntity = next(filter( filterDeveloperEntity, findAllAppMarketDeveloperEntities), None)
                if findOneAppMarketDeveloperEntity == None:
                    print("Error [Not Found AppMarketDeveloperEntity] : {}".format(appMarketDeveloperEntity.toString()))
                    continue
                appEntity.setDeveloperNum(findOneAppMarketDeveloperEntity.getNum)
        
        self.__repository.saveBulkApp(appEntities)
        timeChecker.stop(code="Repository-App")
        findAllAppEntities = self.__repository.findAllApp(appEntities)
                
        #3. resource 등록 
        timeChecker.start(code="Repository-Resource")
        AppResourceEntities:List[AppResourceEntity] = []
        for dto in dtos :
            appResourceEntity = dto.getAppResourceEntity
            if appResourceEntity == None : 
                continue
            
            appEntity = dto.getAppEntity
            filterAppEntity:Callable[[AppEntity] , bool] = lambda t : t.getId == appEntity.getId
            findOneAppEntity:AppEntity = next(filter(filterAppEntity, findAllAppEntities), None)
            if findOneAppEntity == None :
                msg = "Error [Not Found AppEntity] : {}".format(appEntity.toString())
                logManager.error(msg)
                continue
            appResourceEntity.setAppNum(findOneAppEntity.getNum)
            AppResourceEntities.append(appResourceEntity)
        
        self.__repository.saveResourceUseBulk(AppResourceEntities)    
        timeChecker.stop(code="Repository-Resource")
        
        timeChecker.display(code="Repository-Developer")
        timeChecker.display(code="Repository-App")
        timeChecker.display(code="Repository-Resource")