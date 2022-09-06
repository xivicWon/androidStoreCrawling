import sys, rootpath
import time

sys.path.append(rootpath.detect())
import requests, json
from typing import  Callable, List
from bs4 import BeautifulSoup as bs
from bs4.element import Tag
from multiprocessing import Queue
from dto.Dto import Dto
from dto.AppDto import AppDto
from dto.AppWithDeveloperWithResourceDto import AppWithDeveloperWithResourceDto
from dto.RequestDto import RequestDto
from dto.ErrorDto import ErrorCode, ErrorDto
from repository.Repository import Repository
from service.Service import Service
from entity.AppEntity import AppEntity
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from entity.AppResourceEntity import AppResourceEntity
from module.EnvManager import EnvManager
from module.LogManager import LogManager
from module.Curl import CurlMethod, Curl
from module.TimeChecker import TimeChecker
from urllib import error as UrllibError
from exception.TooManyRequest import TooManyRequest

class AppleScrapService(Service) : 
    __MARKET_NUM:int = 2 
    __MAX_RETRY_COUNT:int = 3
    __repository:Repository
    def __init__(self,repository:Repository) -> None:
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
    
            
    def threadProductor(self, requestUrl : str,  processStack:List[Dto], errorStack:List[ErrorDto] ):
        repeatCount = 0
        try:
            self.requestUrl(requestUrl, processStack, errorStack)
        except requests.exceptions.ReadTimeout: 
            errorStack.append(ErrorDto.build(ErrorCode.REQUEST_READ_TIMEOUT , "repeatCount : {} request URL : {}".format(repeatCount, requestUrl)))
            # repeatCount+= 1 
            # if repeatCount < self.__MAX_RETRY_COUNT :
            #     self.requestUrl(requestUrl, processStack, errorStack)
            # else : 
            #     errorStack.append(ErrorDto.build(ErrorCode.REQUEST_READ_TIMEOUT , "repeatCount : {} request URL : {}".format(repeatCount, requestUrl)))
        except AttributeError:
            errorStack.append(ErrorDto.build(ErrorCode.ATTRIBUTE_ERROR , requestUrl))
        except UrllibError.URLError :
            errorStack.append(ErrorDto.build(ErrorCode.URL_OPRN_ERROR , requestUrl))
        except TooManyRequest:
            errorStack.append(ErrorDto.build(ErrorCode.TOO_MANY_REQUEST , requestUrl))
            
    def requestUrl(self, requestUrl : str,  processStack:List[Dto] , errorStack:List[ErrorDto]):
        try :
            header = {"Accept-Language" : "ko-KR"}
            res:requests.Response = Curl.request(method=CurlMethod.GET, url=requestUrl, headers=header, data=None ,timeout=10)
            data = RequestDto(requestUrl, res)
            
            if res.status_code != 200:
                raise requests.exceptions.ReadTimeout(requestUrl)
            elif res.status_code == 429:
                raise TooManyRequest(requestUrl)
            
            appWithDeveloperEntityList:List[AppWithDeveloperWithResourceDto] = self.domParser(data.getResponse())
            if type(appWithDeveloperEntityList) == list :
                processStack.extend(appWithDeveloperEntityList)
            else :
                errorStack.append(ErrorDto.build(ErrorCode.RESPONSE_FAIL , requestUrl))
                
        except requests.exceptions.ConnectionError: 
            errorStack.append(ErrorDto.build(ErrorCode.REQUEST_CONNECTION_ERROR , requestUrl))
        except requests.exceptions.ChunkedEncodingError:
            errorStack.append(ErrorDto.build(ErrorCode.CHUNKED_ENCODING_ERROR , requestUrl))
        except AttributeError as e : 
            errorStack.append(ErrorDto.build(ErrorCode.ATTRIBUTE_ERROR , e))
        except TypeError as e : 
            errorStack.append(ErrorDto.build(ErrorCode.TYPE_ERROR , e))
            
    def domParser(self, response:requests.Response )->List[AppWithDeveloperWithResourceDto]:
        try : 
            soup = bs(response.text, "html.parser")
            scripts:List[Tag] = soup.findAll('script', type="fastboot/shoebox", id=lambda x : x and x.startswith('shoebox-kr-limit-100-genreId-'))
            try : 
                listData = scripts[0].text
                data = json.loads(listData)
                if( type(data["chartsList"]["data"]) == list and len(data["chartsList"]["data"]) > 0 ):
                    parsingResult = []
                    for data in data["chartsList"]["data"] :
                        parsingResult.append(self.mappingDto(data))
                    return parsingResult
            except Exception as e : 
                raise Exception(e)
        except AttributeError as e : 
            msg = "domParser] data : {} ]".format(e)
            raise AttributeError(msg)
        except TypeError as e : 
            msg = "domParser] data : {} ]".format( e)
            raise TypeError(msg)

    def mappingDto (self, data:dict ):
        appleAppDto = AppDto().ofApple(data)   
        if "relationships" in data \
            and "developer" in data["relationships"] \
            and "data" in data["relationships"]["developer"]\
            and len(data["relationships"]["developer"]["data"]) > 0 \
            and "id" in data["relationships"]["developer"]["data"][0] :
            developerMarketId = "id" + data["relationships"]["developer"]["data"][0]["id"]
        else : 
            developerMarketId = ""
        
        appMarketDeveloperEntity = AppMarketDeveloperEntity()\
            .setDeveloperMarketId(developerMarketId.lower())\
            .setDeveloperName(appleAppDto.getDeveloperName())\
            .setMarketNum(self.__MARKET_NUM)\
            .setCompanyNum(0)
        
        appEntity = AppEntity()\
            .setAppName(appleAppDto.getAppName())\
            .setId(appleAppDto.getAppId())\
            .setDeveloperNum(0)\
            .setMarketNum(self.__MARKET_NUM)\
            .setIsActive("Y")\
            .setRating(appleAppDto.getAppRating())\
            .setLastUpdateCurrent()
            
        appResourceEntity = AppResourceEntity()\
            .setAppNum(0)\
            .setResourceType("icon")\
            .setPath(AppDto.downloadImg(downloadLink=appleAppDto.appImage, toDirectory="./tmp/apple", fileName=appEntity.getId))
            
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
            
    
    def updateResponseToRepository(self, dtos : List[AppWithDeveloperWithResourceDto]):
        timeChecker = TimeChecker()
        envManager = EnvManager.instance()
        logManager = LogManager.instance()
        logManager.init(envManager)
        print("{0:,} 건에 대한 등록을 진행합니다.".format(len(dtos))) 
        
        #1. developer 등록 및 번호조회
        appMarketDeveloperEntities:List[AppMarketDeveloperEntity] = []
        timeChecker.start(code="Repository-Developer")
        for dto in dtos :
            appMarketDeveloperEntities.append(dto.getAppMarketDeveloperEntity)
     
        self.__repository.saveBulkDeveloper(appMarketDeveloperEntities)
        timeChecker.stop(code="Repository-Developer")
        findAllAppMarketDeveloperEntities = self.__repository.findAllDeveloperByDeveloperMarketId(appMarketDeveloperEntities)  
        
        #2. app 등록 및 번호조회
        timeChecker.start(code="Repository-App")
        appEntities:List[AppEntity] = []
        for dto in dtos :
            appEntity = dto.getAppEntity
            appMarketDeveloperEntity = dto.getAppMarketDeveloperEntity
            filterDeveloperEntity:Callable[[AppMarketDeveloperEntity] , bool] = lambda t : t.getDeveloperMarketId == appMarketDeveloperEntity.getDeveloperMarketId
            findOneAppMarketDeveloperEntity:AppMarketDeveloperEntity = next(filter( filterDeveloperEntity, findAllAppMarketDeveloperEntities), None)
            if findOneAppMarketDeveloperEntity == None:
                print("Error [Not Found AppMarketDeveloperEntity] : {}".format(appMarketDeveloperEntity.toString()))
                continue
            appEntity.setDeveloperNum(findOneAppMarketDeveloperEntity.getNum)
            appEntities.append(appEntity)
            
        self.__repository.saveBulkApp(appEntities)
        findAllAppEntities = self.__repository.findAllApp(appEntities)
                
        #3. resource 등록 
        AppResourceEntities:List[AppResourceEntity] = []
        for dto in dtos :
            appEntity = dto.getAppEntity
            filterAppEntity:Callable[[AppEntity] , bool] = lambda t : t.getId == appEntity.getId
            findOneAppEntity:AppEntity = next(filter(filterAppEntity, findAllAppEntities), None)
            if findOneAppEntity == None :
                print("Error [Not Found AppEntity] : {}".format(appEntity.toString()))
                continue
           
            appResourceEntity = dto.getAppResourceEntity
            appResourceEntity.setAppNum(findOneAppEntity.getNum)
            AppResourceEntities.append(appResourceEntity)
            
        timeChecker.stop(code="Repository-App")
        
        timeChecker.start(code="Repository-Resource")
        self.__repository.saveResourceUseBulk(AppResourceEntities)    
        timeChecker.stop(code="Repository-Resource")
        
        timeChecker.display(code="Repository-Developer")
        timeChecker.display(code="Repository-App")
        timeChecker.display(code="Repository-Resource")