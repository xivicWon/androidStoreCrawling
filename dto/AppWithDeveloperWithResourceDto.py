from dto.Dto import Dto
from entity.AppEntity import AppEntity
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from entity.AppResourceEntity import AppResourceEntity
from entity.ISOCountryCode import ISOCountryCode

class AppWithDeveloperWithResourceDto(Dto) :
    
    __appEntity:AppEntity 
    __appMarketDeveloperEntity:AppMarketDeveloperEntity
    __appResourceEntity : AppResourceEntity
    __isoCountryCodeEntity : ISOCountryCode
    
    @property
    def getAppEntity(self):
        return self.__appEntity
    
    @property
    def getAppMarketDeveloperEntity(self):
        return self.__appMarketDeveloperEntity
    
    @property
    def getAppResourceEntity(self):
        return self.__appResourceEntity
    
    @property
    def getISOCountryCodeEntity(self):
        return self.__isoCountryCodeEntity
    
    def setAppEntity(self, appEntity):
        self.__appEntity = appEntity 
        return self
        
    def setAppMarketDeveloperEntity(self, appMarketDeveloperEntity):
        self.__appMarketDeveloperEntity = appMarketDeveloperEntity 
        return self

    def setAppResourceEntity(self, appResourceEntity):
        self.__appResourceEntity = appResourceEntity 
        return self
        
    def setISOCountryCodeEntity(self, isoCountryCode):
        self.__isoCountryCodeEntity = isoCountryCode
        return self
    