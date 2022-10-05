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
    
    @staticmethod
    def ofMappingDict( obj:dict ) :
        dto = MIMarketInfoDto()
        dto.__package_name = obj["package_name"]
        if "apple_id" in obj and obj["apple_id"] != None and obj["apple_id"] != "":
            dto.__apple_id = "id" + obj["apple_id"] 
        else :
            dto.__apple_id = None
        return dto
    
        
    def generateMappingCode(self):
        if( (self.getPackageName == "" or self.getPackageName == None) and (self.getAppId == "" or self.getAppId == None) ):
            self.__mapping_code = ""
        else : 
            self.__mapping_code = uuid.uuid4()
    
    def toGoogleAppEntity(self) :
        appEntity = AppEntity()
        if( self.getPackageName == "" or self.getPackageName == None ):
            return None
        appEntity.setId(self.getPackageName)
        appEntity.setMarketNum(1)
        appEntity.setMappingCode(self.__mapping_code)
        appEntity.setLastUpdateCurrent()
        appEntity.setIsActive('Y')
        return appEntity
        
    def toAppleAppEntity(self) :
        appEntity = AppEntity()
        if( self.getAppId == "" or self.getAppId == None ):
            return None
        appEntity.setId(self.getAppId)
        appEntity.setMarketNum(2)
        appEntity.setMappingCode(self.__mapping_code)
        appEntity.setLastUpdateCurrent()
        appEntity.setIsActive('Y')
        return appEntity
        