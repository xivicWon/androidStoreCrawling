import sys, rootpath
import time
from urllib import parse
from dto.Dto import Dto

from repository.Repository import Repository
from service.Service import Service
sys.path.append(rootpath.detect())
import requests, json
from typing import  Callable, List
from bs4 import BeautifulSoup as bs
from bs4.element import Tag
from threading import Thread, current_thread 
from multiprocessing import Queue, current_process
from dto.AppDto import AppDto
from dto.AppWithDeveloperWithResourceDto import AppWithDeveloperWithResourceDto
from dto.RequestDto import RequestDto
from entity.AppEntity import AppEntity
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from entity.AppResourceEntity import AppResourceEntity
from module.Curl import Curl
from module.TimeChecker import TimeChecker

class GoogleScrapService(Service) : 
    __MARKET_NUM:int = 1  
    __MAX_RETRY_COUNT:int = 3 
    __repository:Repository
    __UNDEFINED_APP_NAME: str = "undefined-app"
    __PACKAGE_URL:str = "https://play.google.com/store/apps/details?id="

    def __init__(self,repository:Repository) -> None:
        self.__repository = repository
        pass
            
    def requestWorkListFromDB( self, marketNum:int, offset:int , limit:int ) :
        appList = self.__repository.findNoNameAppLimitedTo(marketNum,offset , limit)
        crwlingJob:List[str] = []
        if type(appList) == list:
            for appEntity in appList :
                url = self.__PACKAGE_URL + appEntity.getId
                crwlingJob.append(url)
        else :
            print("조회된 스크랩대상 데이터가 없음 {} ".format(marketNum))
            exit()
        return crwlingJob
    
    
    def threadProductor(self, requestUrl : str,  obj:List[Dto]):
        repeatCount = 0
        try:
            self.requestUrl(requestUrl, obj)
        except requests.exceptions.ReadTimeout: 
            repeatCount+= 1 
            if repeatCount < self.__MAX_RETRY_COUNT :
                self.requestUrl(requestUrl, obj)
            else : 
                print(current_thread().getName() + "ReadTimeout request Fail : {}".format(requestUrl))
                return 
        except requests.exceptions.ConnectionError: 
            print(current_thread().getName() + "ConnectionError request Fail : {}".format(requestUrl))
            return 
        except requests.exceptions.ChunkedEncodingError:
            print(current_thread().getName() + "ChunkedEncodingError request Fail : {}".format(requestUrl))
            return 

    def requestUrl(self, requestUrl : str,  obj:List[Dto]) :
        res:requests.Response = Curl.request("get", requestUrl, None, None)
        data = RequestDto(requestUrl, res)
        if res.status_code == 404 :
            emptyData:dict = {}
            emptyData["id"] =  data.getUrl().split("?id=")[1]
            emptyData["is_active"] = "N"
            obj.append(self.mappingInactiveDto(emptyData))
        elif res.status_code == 429:
            print("Too Many Request - Try it Later => {} ]".format(requestUrl))
        else :
            appWithDeveloperEntityList = self.singleDomParser(data.getResponse())
            if type(appWithDeveloperEntityList) == AppWithDeveloperWithResourceDto :
                obj.append(appWithDeveloperEntityList)
            else :
                time.sleep(1)
                print(current_thread().getName() + "getResponse Fail : {}".format(requestUrl))  
                
    def singleDomParser(self, response:requests.Response )->AppWithDeveloperWithResourceDto:
        
        appWithDeveloperWithResourceDto:AppWithDeveloperWithResourceDto
        try : 
            soup = bs(response.text, "html.parser")
            data = json.loads(soup.find('script', type='application/ld+json').text)
            data["id"] = response.url.split("id=").pop()
            data["author"]["id"] = soup.find("a", string=data['author']['name'])["href"]\
                .replace("/store/apps/developer?id=", "")\
                .replace("/store/apps/dev?id=", "")
            appWithDeveloperWithResourceDto = (self.mappingDto(data))
            
        except AttributeError as e : 
            print("Response [status code : {} , url : {} ]".format(response.status_code , response.url))
            return None
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
            .setDeveloperMarketId(parse.unquote(data["author"]["id"]))\
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
            
        appResourceEntity = AppResourceEntity()\
            .setAppNum(0)\
            .setResourceType("icon")\
            .setPath(appDto.downloadImg("./tmp/google"))    
            
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
        
        #1. developer 등록 및 번호조회
        appMarketDeveloperEntities:List[AppMarketDeveloperEntity] = []
        timeChecker.start(code="Repository-Developer")
        for dto in dtos :
            if dto.getAppMarketDeveloperEntity != None :
                appMarketDeveloperEntities.append(dto.getAppMarketDeveloperEntity)
            
        if len(appMarketDeveloperEntities) > 0 :
            self.__repository.saveBulkDeveloper(appMarketDeveloperEntities)
            findAllAppMarketDeveloperEntities = self.__repository.findAllDeveloperByDeveloperMarketId(appMarketDeveloperEntities)  
        else :
            findAllAppMarketDeveloperEntities = []
            
        timeChecker.stop(code="Repository-Developer")
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
            
        self.__repository.saveBulkApp(appEntities)
        findAllAppEntities = self.__repository.findAllApp(appEntities)
                
        #3. resource 등록 
        AppResourceEntities:List[AppResourceEntity] = []
        for dto in dtos :
            appResourceEntity = dto.getAppResourceEntity
            if appResourceEntity != None : 
                appEntity = dto.getAppEntity
                filterAppEntity:Callable[[AppEntity] , bool] = lambda t : t.getId == appEntity.getId
                findOneAppEntity:AppEntity = next(filter(filterAppEntity, findAllAppEntities), None)
                if findOneAppEntity == None :
                    print("Error [Not Found AppEntity] : {}".format(appEntity.toString()))
                    continue
                appResourceEntity.setAppNum(findOneAppEntity.getNum)
                AppResourceEntities.append(appResourceEntity)
            
        timeChecker.stop(code="Repository-App")
        
        timeChecker.start(code="Repository-Resource")
        self.__repository.saveResourceUseBulk(AppResourceEntities)    
        timeChecker.stop(code="Repository-Resource")
        
        timeChecker.display(code="Repository-Developer")
        timeChecker.display(code="Repository-App")
        timeChecker.display(code="Repository-Resource")
        
    def updateResponseToRepository_old(self, dtos : List[AppWithDeveloperWithResourceDto]):
        TimeALL = "TimeALL"
        
        timeChecker = TimeChecker()
        timeChecker.start(code=TimeALL)
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
            if dto.getAppMarketDeveloperEntity != None :
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
            if dto.getAppResourceEntity != None :
                appResourceEntity = dto.getAppResourceEntity
                appResourceEntity.setAppNum(appNum)
                bulkResource.append(appResourceEntity)
            
            # self.__repository.saveResource(appResourceEntity)
            # Todo : 이미지는 중복등록을 방지하기 위한 처리가 필요함. 
        # print("Bulk Insert Total : {}".format( len(bulkResource)))
        if len(bulkResource) >= 0 :
            self.__repository.saveResourceUseBulk(bulkResource)    
            
        timeChecker.stop(code=TimeALL)
        timeChecker.display(code=TimeALL)
        