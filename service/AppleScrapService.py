import os
import sys, rootpath
from unittest import result




sys.path.append(rootpath.detect())
import requests, json
from typing import  Callable, List, Optional
from bs4 import BeautifulSoup as bs
from bs4.element import Tag
from multiprocessing import Queue
from dto.Dto import Dto
from dto.AppDto import AppDto
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
    
    def __init__(self,repository:Repository) -> None:
        super().__init__()
        self.__repository = repository
        pass
        
    def requestWorkListFromDB( self, marketNum:int  ) :
        appMartetScrapList = self.__repository.findMarketScrapUrl(marketNum)
        crwlingJob:List[str] = []
        if type(appMartetScrapList) == list:
            for appMartetScrap in appMartetScrapList :
                urls = appMartetScrap.getScrapUrl()
                crwlingJob.extend(urls)
        else :
            print("조회된 스크랩대상 데이터가 없음 {} {} {} ".format(marketNum))
            exit()
        return crwlingJob
    
            
    def threadProductor(self, url : str,  processStack:List[Dto], errorStack:List[ErrorDto] ):
        repeatCount = 0
        try:
            self.requestUrl(url, processStack, errorStack)
        except requests.exceptions.ReadTimeout: 
            errorStack.append(ErrorDto.build(ErrorCode.REQUEST_READ_TIMEOUT , "repeatCount : {} request URL : {}".format(repeatCount, url)))
        except AttributeError:
            errorStack.append(ErrorDto.build(ErrorCode.ATTRIBUTE_ERROR , url))
        except UrllibError.URLError :
            errorStack.append(ErrorDto.build(ErrorCode.URL_OPEN_ERROR , url))
        except TooManyRequest:
            errorStack.append(ErrorDto.build(ErrorCode.TOO_MANY_REQUEST , url))
            
    def requestUrl(self, url : str, processStack:List[Dto] , errorStack:List[ErrorDto]):
        try :
            header = {"Accept-Language" : "ko-KR"}
            res:requests.Response = Curl.request(method=CurlMethod.GET, url=url, headers=header, data=None ,timeout=10)
            data = RequestDto(url, res)
            print("StatusCode : {}".format(res.status_code))
            if res.status_code == 200:
                if self.isCategoryURL(url):
                    appWithDeveloperEntityList:List[AppWithDeveloperWithResourceDto] = DomParser.parseAppleCategory(data.getResponse())
                    if type(appWithDeveloperEntityList) == list :
                        processStack.extend(appWithDeveloperEntityList)
                    else :
                        errorStack.append(ErrorDto.build(ErrorCode.RESPONSE_FAIL , url))
                else :
                    processStack.append(DomParser.parseAppleAppDetail(data.getResponse()))
            elif res.status_code == 429:
                raise TooManyRequest(url)
            elif res.status_code == 404:
                appId = data.getUrl().split("/")[-1]
                processStack.append(DomParser.mappingInactiveDto(AppleScrapService.__MARKET_NUM, appId))
            else:
                raise requests.exceptions.ReadTimeout(url)
            
        except requests.exceptions.ConnectionError: 
            errorStack.append(ErrorDto.build(ErrorCode.REQUEST_CONNECTION_ERROR , url))
        except requests.exceptions.ChunkedEncodingError:
            errorStack.append(ErrorDto.build(ErrorCode.CHUNKED_ENCODING_ERROR , url))
        except AttributeError as e : 
            errorStack.append(ErrorDto.build(ErrorCode.ATTRIBUTE_ERROR , e))
        except TypeError as e : 
            errorStack.append(ErrorDto.build(ErrorCode.TYPE_ERROR , e))
    
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
                print("로그작성필요 : {}".format(resultData))
                
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
            if appEntity.getIsActive == 'Y' :
                appMarketDeveloperEntity = dto.getAppMarketDeveloperEntity
                filterDeveloperEntity:Callable[[AppMarketDeveloperEntity] , bool] = lambda t : t.getDeveloperMarketId == appMarketDeveloperEntity.getDeveloperMarketId
                findOneAppMarketDeveloperEntity:AppMarketDeveloperEntity = next(filter( filterDeveloperEntity, findAllAppMarketDeveloperEntities), None)
                if findOneAppMarketDeveloperEntity == None:
                    print("Error [Not Found AppMarketDeveloperEntity] : {}".format(appMarketDeveloperEntity.toString()))
                    continue
                appEntity.setDeveloperNum(findOneAppMarketDeveloperEntity.getNum)
            appEntities.append(appEntity)
            print(appEntity.toString())
            
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