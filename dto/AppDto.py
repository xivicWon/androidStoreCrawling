from urllib import parse, request
import os
import uuid
from dto.Dto import Dto

class AppDto(Dto) : 
    DEFAULT_IMAGE_WIDTH:int = 256
    developerId: str
    developerName : str
    
    appName: str
    appId : str
    appRating : int
    appImage : str 
    appIsActive: str
    def __init__(self   ) -> None:
        pass
    
    @staticmethod
    def ofInActive( appId:str):
        appDto = AppDto()
        appDto.appId = appId
        appDto.appIsActive = "N"
        return appDto 
    
    @staticmethod
    def ofGoogle(data:dict):
        appDto = AppDto()
        appDto.appName = parse.unquote(data["name"])
        appDto.appId = data["id"]
        if "aggregateRating" in data and "ratingValue" in data["aggregateRating"]:
            appDto.appRating = int(float(data["aggregateRating"]["ratingValue"]) * 10)
        else :
            appDto.appRating = 0
        
        appDto.developerId = parse.unquote(data["author"]["id"]) if "author" in data and "id" in data["author"] else ""
        appDto.developerName = data["author"]["name"] if "author" in data and "name" in data["author"] else ""
        if "image" in data :
            img:str = data["image"]
            appDto.appImage = img + "=s" + str(appDto.DEFAULT_IMAGE_WIDTH) + "-rw"
        else :
            appDto.appImage = ""
            
        appDto.appIsActive =  data["is_active"] if "is_active" in data else "Y"
        return appDto 
    
    @staticmethod
    def ofAppleCategory(data:dict):
        appDto = AppDto()
        appDto.appName = parse.unquote(data["name"])
        appDto.appId = "id" + data["id"]
        appDto.appRating = int(data["userRating"]["value"] * 10)
        
        appDto.developerId = parse.unquote(data["relationships"]["developer"]["data"][0]["id"]) if "relationships" in data and "developer" in data["relationships"] and "data" in data["relationships"]["developer"] and len(data["relationships"]["developer"]["data"]) > 0 and "id" in data["relationships"]["developer"]["data"][0] else ""
        appDto.developerName = parse.unquote(data["artistName"]) if "artistName" in data else ""
        if "artwork" in data and "url" in data["artwork"] :
            img:str = data["artwork"]["url"]
            appDto.appImage = "/".join(img.split("/")[:-1]) + "/" + str(appDto.DEFAULT_IMAGE_WIDTH) + "x0w.webp"
        else :
            appDto.appImage = ""
            
        return appDto 
    
    @staticmethod
    def ofAppleAppDetail(data:dict):
        appDto = AppDto()
        appDto.appName = parse.unquote(data["name"])
        appDto.appId = "id" + data["id"]
        appDto.appRating = int(data["aggregateRating"]["ratingValue"] * 10) if "aggregateRating" in data and "ratingValue" in data["aggregateRating"] else 0
        developerUrl = data["author"]["url"] if "author" in data and "url" in data["author"] else ""
        appDto.developerId = parse.unquote(developerUrl.split("/")[-1]) 
        appDto.developerName = parse.unquote(data["author"]["name"]) if "author" in data and "name" in data["author"] else ""
        appDto.appImage = data["img"] if "img" in data else ""
      
        return appDto
    
    def getDeveloperId(self)->str : 
        return self.developerId
    
    def getDeveloperName(self)->str : 
        return self.developerName
    
    def getAppName(self)->str : 
        return self.appName
    
    def getAppId( self)->str : 
        return self.appId
    
    def getAppRating( self)->int : 
        return self.appRating
    
    def getAppImage( self ) -> str : 
        return self.appImage
    
    @staticmethod
    def downloadImg (downloadLink:str, toDirectory:str, fileName:str, force:bool = False) -> str :
        os.makedirs(toDirectory, exist_ok=True)
        downloadFileToPath = "{}/{}.png".format(toDirectory , fileName )
        if force : 
            os.remove(downloadFileToPath)
            
        if not os.path.isfile(downloadFileToPath):
            (fileName , Headers) = request.urlretrieve(url=downloadLink, filename=downloadFileToPath)
            return fileName 
        else :
            return downloadFileToPath