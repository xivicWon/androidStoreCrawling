from dto.Dto import Dto
import uuid

from entity.AppEntity import AppEntity
class MIMarketInfoDto(Dto) : 
    __package_name:str
    __apple_id : str
    __mapping_code :str
    
    def __init__(self) -> None:
        self.__mapping_code = ""
        pass

    @property
    def getPackageName (self):
        return self.__package_name
    
    @property
    def getAppId (self):
        return self.__apple_id
    
    def setPackageName (self, package_name):
        self.__package_name = package_name
    
    def setAppId (self, apple_id):
        self.__apple_id = apple_id 
    
    def ofDict(self , obj:dict ) :
        self.__package_name = obj["package_name"]
        self.__apple_id = obj["apple_id"]
        return self
        
    def generateMappingCode(self):
        self.__mapping_code = uuid.uuid4()
    
    def toGoogleAppEntity(self) :
        appEntity = AppEntity()
        appEntity.setId(self.getPackageName)
        appEntity.setMarketNum(1)
        appEntity.setMappingCode(self.__mapping_code)
        appEntity.setLastUpdateCurrent()
        appEntity.setIsActive('Y')
        return appEntity
        
    def toAppleAppEntity(self) :
        appEntity = AppEntity()
        appEntity.setId(self.getAppId)
        appEntity.setMarketNum(2)
        appEntity.setMappingCode(self.__mapping_code)
        appEntity.setLastUpdateCurrent()
        appEntity.setIsActive('Y')
        return appEntity
        