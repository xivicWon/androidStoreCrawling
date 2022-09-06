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
    appImageSavaPath:str = "upload"
    appImage : str 
    appIsActive: str
    def __init__(self   ) -> None:
        pass
    
    def ofGoogleInActive(self, data :dict):
        self.appId = data["id"]
        self.appIsActive =  data["is_active"] if "is_active" in data else "N"
        return self 
    
    def ofGoogle(self, data:dict):
        self.appName = parse.unquote(data["name"])
        self.appId = data["id"]
        if "aggregateRating" in data and "ratingValue" in data["aggregateRating"]:
            self.appRating = int(float(data["aggregateRating"]["ratingValue"]) * 10)
        else :
            self.appRating = 0
        
        self.developerId = parse.unquote(data["author"]["id"]) if "author" in data and "id" in data["author"] else ""
        self.developerName = data["author"]["name"] if "author" in data and "name" in data["author"] else ""
        if "image" in data :
            img:str = data["image"]
            self.appImage = img + "=s" + str(self.DEFAULT_IMAGE_WIDTH) + "-rw"
        else :
            self.appImage = ""
            
        self.appIsActive =  data["is_active"] if "is_active" in data else "Y"
        return self 
    
    def ofApple(self, data:dict):
        self.appName = parse.unquote(data["name"])
        self.appId = "id" + data["id"]
        self.appRating = int(data["userRating"]["value"] * 10)
        
        self.developerId = parse.unquote(data["relationships"]["developer"]["data"][0]["id"]) if "relationships" in data and "developer" in data["relationships"] and "data" in data["relationships"]["developer"] and len(data["relationships"]["developer"]["data"]) > 0 and "id" in data["relationships"]["developer"]["data"][0] else ""
        self.developerName = parse.unquote(data["artistName"]) if "artistName" in data else ""
        if "artwork" in data and "url" in data["artwork"] :
            img:str = data["artwork"]["url"]
            self.appImage = "/".join(img.split("/")[:-1]) + "/" + str(self.DEFAULT_IMAGE_WIDTH) + "x0w.webp"
        else :
            self.appImage = ""
            
        return self 
    
    # def fileDownloadPoilcy(self, file:str)->bool:
    #     return not os.path.isfile(file)
        
    # def downloadImg (self , toDir) -> str :
    #     if self.appImage : 
    #         os.makedirs(toDir, exist_ok=True)
    #         # downloadFileToPath = toDir + "/" + uuid.uuid4().hex + ".png"
    #         downloadFileToPath = toDir + "/" + self.appId + ".png"
    #         if self.fileDownloadPoilcy(downloadFileToPath):
    #             request.urlretrieve(self.appImage, downloadFileToPath)
    #         return downloadFileToPath
    #     return ""
    
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
    def downloadImg (downloadLink:str, toDirectory:str, fileName:str) -> str :
        os.makedirs(toDirectory, exist_ok=True)
        downloadFileToPath = "{}/{}.png".format(toDirectory , fileName )
        if not os.path.isfile(downloadFileToPath):
            (fileName , Headers) = request.urlretrieve(downloadLink, downloadFileToPath)
            return fileName 
        else :
            return downloadFileToPath