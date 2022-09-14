import json
import os
import requests
from typing import List
from bs4 import BeautifulSoup as bs
from bs4.element import Tag

from dto.AppDto import AppDto
from dto.AppWithDeveloperWithResourceDto import AppWithDeveloperWithResourceDto
from entity.AppEntity import AppEntity
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from entity.AppResourceEntity import AppResourceEntity

class DomParser :
    __APPLE_MARKET_NUM:int = 2 
    __APPLE_RESOURCE_DIR:str = "./resource/apple"
    __GOOGLE_MARKET_NUM:int = 1
    __GOOGLE_RESOURCE_DIR:str = "./resource/google"
    __UNDEFINED_APP_NAME: str = "undefined-app"
    
    @staticmethod
    def makeResourceDir(directory :str) :
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    @staticmethod
    def parseAppleAppDetail(response:requests.Response) : 
        marketNum = DomParser.__APPLE_MARKET_NUM 
        resourceDirectory = DomParser.__APPLE_RESOURCE_DIR
        DomParser.makeResourceDir(resourceDirectory)
        try : 
            soup = bs(response.text, "html.parser")
            id = soup.select_one('meta[name="apple:content_id"]').get('content')
            appIconSrcSet = soup.select_one('source').get("srcset", default="")
            appIconSrc = appIconSrcSet.split(",")[0].split(" ")[0]
            apiData = soup.find( name='script', type="application/ld+json").text
            try : 
                data = json.loads(apiData)
                data["id"] = id
                data["img"] = appIconSrc
                if( type(data) == dict ):
                    return DomParser.getAppWithDeveloperWithResourceDto(
                        appDto=AppDto.ofAppleAppDetail(data),
                        marketNum=marketNum, 
                        resourceDirectory=resourceDirectory)
                    
            except Exception as e : 
                raise Exception(e)
        except AttributeError as e : 
            msg = "domParser] data : {} ]".format(e)
            raise AttributeError(msg)
        except TypeError as e : 
            msg = "domParser] data : {} ]".format( e)
            raise TypeError(msg)

    @staticmethod
    def parseAppleCategory( response:requests.Response )->List[AppWithDeveloperWithResourceDto]:
        marketNum = DomParser.__APPLE_MARKET_NUM  
        resourceDirectory = DomParser.__APPLE_RESOURCE_DIR
        DomParser.makeResourceDir(resourceDirectory)
        try : 
            soup = bs(response.text, "html.parser")
            scripts:List[Tag] = soup.findAll('script', type="fastboot/shoebox", id=lambda x : x and x.startswith('shoebox-kr-limit-100-genreId-'))
            try : 
                listData = scripts[0].text
                data = json.loads(listData)
                if( type(data["chartsList"]["data"]) == list and len(data["chartsList"]["data"]) > 0 ):
                    parsingResult = []
                    for data in data["chartsList"]["data"] :
                        parsingResult.append(
                            DomParser.getAppWithDeveloperWithResourceDto(
                                appDto=AppDto.ofAppleCategory(data),
                                marketNum=marketNum, 
                                resourceDirectory=resourceDirectory)
                            )
                    return parsingResult
            except Exception as e : 
                raise Exception(e)
        except AttributeError as e : 
            msg = "domParser] data : {} ]".format(e)
            raise AttributeError(msg)
        except TypeError as e : 
            msg = "domParser] data : {} ]".format( e)
            raise TypeError(msg)

    @staticmethod
    def getAppWithDeveloperWithResourceDto(marketNum:int, appDto:AppDto, resourceDirectory:str ):
        
        appMarketDeveloperEntity = AppMarketDeveloperEntity()\
            .setDeveloperMarketId(appDto.getDeveloperId())\
            .setDeveloperName(appDto.getDeveloperName())\
            .setMarketNum(marketNum)\
            .setCompanyNum(0)
        
        appEntity = AppEntity()\
            .setAppName(appDto.getAppName())\
            .setId(appDto.getAppId())\
            .setDeveloperNum(0)\
            .setMarketNum(marketNum)\
            .setIsActive("Y")\
            .setRating(appDto.getAppRating())\
            .setLastUpdateCurrent()
            
        appResourceEntity = AppResourceEntity()\
            .setAppNum(0)\
            .setResourceType("icon")\
            .setPath(
                AppDto.downloadImg(
                    downloadLink=appDto.appImage, 
                    toDirectory=resourceDirectory, 
                    fileName=appEntity.getId)
                )
            
        return AppWithDeveloperWithResourceDto()\
            .setAppEntity(appEntity)\
            .setAppMarketDeveloperEntity(appMarketDeveloperEntity)\
            .setAppResourceEntity(appResourceEntity)
            
    @staticmethod
    def mappingInactiveDto( marketNum:int, appId:str ):
        appEntity = AppEntity()\
            .setAppName(DomParser.__UNDEFINED_APP_NAME)\
            .setId(appId)\
            .setDeveloperNum(0)\
            .setMarketNum(marketNum)\
            .setIsActive("N")\
            .setRating(0)\
            .setLastUpdateCurrent()
            
        appMarketDeveloperEntity = None
        appResourceEntity = None
        
        return AppWithDeveloperWithResourceDto()\
            .setAppEntity(appEntity)\
            .setAppMarketDeveloperEntity(appMarketDeveloperEntity)\
            .setAppResourceEntity(appResourceEntity)