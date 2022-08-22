from dto.Dto import Dto
from entity.AppEntity import AppEntity
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from entity.AppResourceEntity import AppResourceEntity

class AppWithDeveloperWithResourceDto(Dto) :
    
    __appEntity:AppEntity 
    __appMarketDeveloperEntity:AppMarketDeveloperEntity
    __appResourceEntity : AppResourceEntity
    
    @property
    def getAppEntity(self):
        return self.__appEntity
    
    @property
    def getAppMarketDeveloperEntity(self):
        return self.__appMarketDeveloperEntity
    
    @property
    def getAppResourceEntity(self):
        return self.__appResourceEntity
    
    def setAppEntity(self, appEntity):
        self.__appEntity = appEntity 
        return self
        
    def setAppMarketDeveloperEntity(self, appMarketDeveloperEntity):
        self.__appMarketDeveloperEntity = appMarketDeveloperEntity 
        return self

    def setAppResourceEntity(self, appResourceEntity):
        self.__appResourceEntity = appResourceEntity 
        return self
        