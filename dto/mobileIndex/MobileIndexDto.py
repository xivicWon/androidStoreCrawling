from dto.Dto import Dto
from entity.AppEntity import AppEntity

class MobileIndexDto(Dto) :
    __rank : int
    __country_name : str
    __market_name : str
    __rank_type : str
    __app_name : str
    __publisher_name : str
    __icon_url : str
    __market_appid : str
    __package_name : str
   
    def __init__(self) -> None: 
        pass
 
    def ofDict(self, obj :dict):
        self.__rank = obj["rank"]
        self.__country_name = obj["country_name"]
        self.__market_name = obj["market_name"]
        self.__rank_type = obj["rank_type"]
        self.__app_name = obj["app_name"]
        self.__publisher_name = obj["publisher_name"]
        self.__icon_url = obj["icon_url"]
        self.__market_appid = obj["market_appid"]
        self.__package_name = obj["package_name"]
    
    def __str__(self):
        print('{} 예외처리 called'.format(__class__.__name__))
        return self.__app_name
    
    def toAppEntity(self) -> AppEntity:
        appEntity = AppEntity()  
        appEntity.setMarketNum(appEntity.getMarketNumByName(self.__market_name))
        appEntity.setMappingCode(appEntity.generateMappingCode(self.__package_name))
        
        if appEntity.getMarketNum == 2 :
            appId = "id" + self.__market_appid
        else :
            appId = self.__market_appid
            
        return appEntity.setId(appId)\
            .setAppName(self.__app_name)\
            .setDeveloperNum(0)\
            .setCateNum(0)\
            .setMinUseAge(0)\
            .setIsActive("Y")\
            .setLastUpdateCurrent()