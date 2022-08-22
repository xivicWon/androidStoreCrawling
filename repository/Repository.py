from typing import List, Optional
from entity.AppMarketScrap import AppMarketScrap
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from entity.AppResourceEntity import AppResourceEntity
from entity.AppEntity import AppEntity

class Repository : 
    
    def __init__(self) -> None:
        pass
    
    def findAppById(self, market_num:int, id:str )->Optional[AppEntity]:
        pass
    
    def findNoNameAppLimitedTo(self , market_num,  offset :int , limit :int ) -> Optional[List[AppEntity]]:  
        pass
    
    def findAppLimitedTo(self , market_num,  offset :int , limit :int ) -> Optional[List[AppEntity]]:  
        pass
        
    def findDeveloperByDeveloperMarketId(self, appMarketDeveloperEntity : AppMarketDeveloperEntity) ->Optional[AppMarketDeveloperEntity]:
        pass
    
    def saveDeveloper(self, appMarketDeveloperEntity : AppMarketDeveloperEntity) -> int:
        pass
    
    def saveResource (self, appResourceEntity : AppResourceEntity): 
        pass
         
    def addApp ( self, appEntity : AppEntity) -> Optional[int] : 
        pass
        
    def updateApp( self, appEntity : AppEntity): 
        pass
    
    def deleteApp( self, appEntity : AppEntity): 
        pass

    def findMarketScrapUrl(self , market_num ) -> Optional[List[AppMarketScrap]]:  
        pass
    
    def saveResourceUseBulk(self, bulkResources: List[AppResourceEntity]):
        pass
        
    def saveAppTmpUseBulk(self, bulkResources: List[AppEntity]):
        pass
        