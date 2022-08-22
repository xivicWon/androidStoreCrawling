from urllib import parse, request
import os
from dto.Dto import Dto

class AppleAppDto(Dto) : 
    DEFAULT_IMAGE_WIDTH:int = 256
    developerId: str
    developerName : str
    
    appName: str
    appId : str
    appRating : int
    appImageSavaPath:str = "upload"
    appImage : str 
    
    def __init__(self   ) -> None:
        pass
    
    def ofDict(self, data:dict):
        self.appName = parse.unquote(data["name"])
        self.appId = "id" + data["id"]
        self.appRating = int(data["userRating"]["value"] * 10)
        
        self.developerId = data["relationships"]["developer"]["data"][0]["id"] if "relationships" in data and "developer" in data["relationships"] and "data" in data["relationships"]["developer"] and len(data["relationships"]["developer"]["data"]) > 0 and "id" in data["relationships"]["developer"]["data"][0] else ""
        self.developerName = data["artistName"] if "artistName" in data else ""
        if "artwork" in data and "url" in data["artwork"] :
            img:str = data["artwork"]["url"]
            self.appImage = "/".join(img.split("/")[:-1]) + "/" + str(self.DEFAULT_IMAGE_WIDTH) + "x0w.webp"
        else :
            self.appImage = ""
            
        return self 
    
    def fileDownloadPoilcy(self, file:str)->bool:
        return not os.path.isfile(file)
        
    def downloadImg (self , toDir) -> str :
        if self.appImage : 
            os.makedirs(toDir, exist_ok=True)
            downloadFileToPath = toDir + "/" + self.appId + ".png"
            if self.fileDownloadPoilcy(downloadFileToPath):
                request.urlretrieve(self.appImage, downloadFileToPath)
            return downloadFileToPath
        return ""
    
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
    
    