import sys, rootpath
from dto.Dto import Dto

from repository.Repository import Repository
sys.path.append(rootpath.detect())
import requests, json
from typing import  Callable, List
from bs4 import BeautifulSoup as bs
from bs4.element import Tag
from threading import Thread, current_thread 
from multiprocessing import Queue, current_process
from dto.AppleAppDto import AppleAppDto
from dto.AppWithDeveloperWithResourceDto import AppWithDeveloperWithResourceDto
from dto.RequestDto import RequestDto
from entity.AppEntity import AppEntity
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from entity.AppResourceEntity import AppResourceEntity
from repository.AppStoreRepository import AppStoreRepository
from module.Curl import Curl
from module.TimeChecker import TimeChecker

class AppleScrapService : 
    __MARKET_NUM:int = 2 
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
        return crwlingJob[:2]
    
    def threadJob(self, requestUrl : str,  obj:List[Dto]):
        curl = Curl()
        try:
            # print("[ Thread Job ] >>>>>> {} ".format(requestUrl))
            res:requests.Response = curl.request(requestUrl)
            data = RequestDto(requestUrl, res)
            appWithDeveloperEntityList = self.domParser(data.getResponse())
            if type(appWithDeveloperEntityList) == list :
                obj.extend(appWithDeveloperEntityList)
            else :
                print(current_thread().getName() + "getResponse Fail : {}".format(requestUrl))
        except requests.exceptions.ReadTimeout: 
            print(current_thread().getName() + "ReadTimeout request Fail : {}".format(requestUrl))
            return 
        except requests.exceptions.ConnectionError: 
            print(current_thread().getName() + "ConnectionError request Fail : {}".format(requestUrl))
            return 
        except requests.exceptions.ChunkedEncodingError:
            print(current_thread().getName() + "ChunkedEncodingError request Fail : {}".format(requestUrl))
            return 

    def domParser(self, response:requests.Response )->List[AppWithDeveloperWithResourceDto]:
        try : 
            soup = bs(response.text, "html.parser")
            scripts:List[Tag] = soup.findAll('script', type="fastboot/shoebox", id=lambda x : x and x.startswith('shoebox-kr-limit-100-genreId-'))
            if len(scripts) > 0 :
                listData = scripts[0].text
                data = json.loads(listData)
                parsingResult = []
                try : 
                    if( type(data["chartsList"]["data"]) == list and len(data["chartsList"]["data"]) > 0 ):
                        for data in data["chartsList"]["data"] :
                            parsingResult.append(self.mappingDto(data))
                        return parsingResult
                except Exception as e : 
                    print(e) 
            return None
        except AttributeError as e : 
            print(e)
            return None

    def mappingDto (self, data:dict ):
        appleAppDto = AppleAppDto().ofDict(data)
        
        appMarketDeveloperEntity = AppMarketDeveloperEntity()\
            .setDeveloperMarketId(0)\
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
            .setPath(appleAppDto.downloadImg("./tmp/apple"))    
            
        return AppWithDeveloperWithResourceDto()\
            .setAppEntity(appEntity)\
            .setAppMarketDeveloperEntity(appMarketDeveloperEntity)\
            .setAppResourceEntity(appResourceEntity)


    def consumerProcess(self, q: Queue):
        responseResults:List[AppWithDeveloperWithResourceDto] = []
        while ( True ):
            value = q.get()
            if( value == "None"):
                break
            responseResults.extend(value)
        self.updateResponseToRepository(responseResults)
        
    def updateResponseToRepository(self, dtos : List[AppWithDeveloperWithResourceDto]):
        timeChecker = TimeChecker()
        timeChecker.start(code="Repository-Work")
        ids:List[str] = []
        bulkResource:List[AppResourceEntity] = []
        
        for dto in dtos :
            currentId = dto.getAppEntity.getId
            condition : Callable[[str], bool]  = lambda id : id == currentId 
            filtered = next(filter( condition, ids ), None)
            if filtered != None:
                # print("{} 중복로 인한 패스!".format(currentId))
                continue
            
            ids.append(currentId)
            #1. developer 등록 및 번호조회
            result = self.__repository.findDeveloperByDeveloperMarketId(dto.getAppMarketDeveloperEntity)
            if( result == None ):
                try :
                    developNum = self.__repository.saveDeveloper(dto.getAppMarketDeveloperEntity)
                except Exception as e : 
                    print(e)
                    exit()
            else :
                developNum = result.getNum
                
            #2. app 등록 및 번호조회
            appEntity = dto.getAppEntity
            findAppEntity:AppEntity = self.__repository.findAppById(appEntity.getMarketNum, appEntity.getId)
            if findAppEntity != None :
                appNum = findAppEntity.getNum
            else :
                appEntity.setDeveloperNum(developNum)
                appNum = self.__repository.addApp(appEntity)
                
            #3. resource 등록 ( Bulk Insert 가능. )
            appResourceEntity = dto.getAppResourceEntity
            appResourceEntity.setAppNum(appNum)
            bulkResource.append(appResourceEntity)
            
            # self.__repository.saveResource(appResourceEntity)
            # Todo : 이미지는 중복등록을 방지하기 위한 처리가 필요함. 
        # print("Bulk Insert Total : {}".format( len(bulkResource)))
        self.__repository.saveResourceUseBulk(bulkResource)    
        timeChecker.stop(code="Repository-Work")
        timeChecker.display(code="Repository-Work")
        