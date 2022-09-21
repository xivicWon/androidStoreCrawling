import datetime
import random
import sys, rootpath
sys.path.append(rootpath.detect())
import requests
from module.FileManager import FileManager
from dto.ThreadJobDto import ThreadJobDto
from dto.ErrorDto import ErrorCode, ErrorDto
from repository.Repository import Repository
from service.Service import Service
from urllib import error as UrllibError
from typing import  Callable, List, Optional
from multiprocessing import Queue
from dto.Dto import Dto
from dto.AppWithDeveloperWithResourceDto import AppWithDeveloperWithResourceDto
from dto.RequestDto import RequestDto
from entity.AppEntity import AppEntity
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from entity.AppResourceEntity import AppResourceEntity
from module.EnvManager import EnvManager
from module.LogManager import LogManager
from module.Curl import Curl, CurlMethod
from module.TimeChecker import TimeChecker
from module.DomParser import DomParser
from exception.TooManyRequest import TooManyRequest


class GoogleScrapService(Service) : 
    __MARKET_NUM:int = 1  
    __repository:Repository
    __APP_ID_URL:str = "https://play.google.com/store/apps/details?id="
    __RESOURCE_DIR:str = "/images/google"
        
    def __init__(self,repository:Repository) -> None:
        super().__init__()
        self.__repository = repository
            
    def getThreadJobOfNoNameApps( self, marketNum:int, offset:int , limit:int ) :
        appList = self.__repository.findNoNameAppLimitedTo(marketNum,offset , limit)
        crwlingJob:List[str] = []
        if type(appList) != list:
            msg = "조회된 스크랩대상 데이터가 없음 {} ".format(marketNum)
            print(msg)
            exit()
            
        for dto in appList :
            url = self.__APP_ID_URL + dto.getAppEntity.getId
            resourceDir = self.__RESOURCE_DIR + "/" + FileManager.randomResourceSubDirectory()
            crwlingJob.append(ThreadJobDto(url = url, resourceDir = resourceDir, dto=dto))
            
        return crwlingJob
    
    
    def threadProducer(self, threadJobDto : ThreadJobDto, processStack:List[Dto], errorStack:List[Dto]):
        requestUrl = threadJobDto.getUrl
        data = self.requestUrl(requestUrl, errorStack )
        if data == None:
            return
        res = data.getResponse
        if res.status_code == 404 :
            appId = data.getUrl.split("?id=")[1]
            processStack.append(DomParser.mappingInactiveDto(GoogleScrapService.__MARKET_NUM, appId))
        elif res.status_code == 429:
            errorStack.append(ErrorDto.build(ErrorCode.TOO_MANY_REQUEST , requestUrl))
        else :
            try : 
                FileManager.makeDirs(threadJobDto.getResourceDir)
                appDto = DomParser.parseGoogleApp(res)
                result = DomParser.getAppWithDeveloperWithResourceDto(
                    marketNum=self.__MARKET_NUM , 
                    appDto = appDto, 
                    resourceDirectory= threadJobDto.getResourceDir)
                
                if type(result) == AppWithDeveloperWithResourceDto :
                    processStack.append(result)
                else :
                    msg = "getResponse Fail : {}".format(requestUrl)
                    errorStack.append(ErrorDto.build(ErrorCode.RESPONSE_FAIL , msg))
            except AttributeError  as e  :
                msg = "getResponse Fail : {}".format(requestUrl) + e 
                errorStack.append(ErrorDto.build(ErrorCode.ATTRIBUTE_ERROR , msg))
            except TypeError as e  :
                msg = "getResponse Fail : {} ".format(requestUrl) + e 
                errorStack.append(ErrorDto.build(ErrorCode.TYPE_ERROR , msg))

    def requestUrl(self, url : str,  errorStack:List[ErrorDto]):
        header = {"Accept-Language" : "ko-KR"}
        try :
            res:requests.Response = Curl.request(
                method=CurlMethod.GET, 
                url=url, 
                headers=header, 
                data=None ,
                timeout=10)
            return RequestDto(url, res)
        except requests.exceptions.ConnectionError: 
            errorStack.append(ErrorDto.build(ErrorCode.REQUEST_CONNECTION_ERROR , url))
            
        except UrllibError.URLError :
            errorStack.append(ErrorDto.build(ErrorCode.URL_OPEN_ERROR , url))
        except TooManyRequest:
            errorStack.append(ErrorDto.build(ErrorCode.TOO_MANY_REQUEST , url))
        # except requests.exceptions.ChunkedEncodingError:
        #     errorStack.append(ErrorDto.build(ErrorCode.CHUNKED_ENCODING_ERROR , url))
        # except AttributeError as e : 
        #     errorStack.append(ErrorDto.build(ErrorCode.ATTRIBUTE_ERROR , e))
        # except TypeError as e : 
        #     errorStack.append(ErrorDto.build(ErrorCode.TYPE_ERROR , e))
        return None
                
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
        timeChecker.stop(code="Repository-App")
        
        findAllAppEntities = self.__repository.findAllApp(appEntities)
        
        #3. resource 등록 
        timeChecker.start(code="Repository-Resource")
        AppResourceEntities:List[AppResourceEntity] = []
        for dto in dtos :
            appResourceEntity = dto.getAppResourceEntity
            if appResourceEntity != None : 
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
        