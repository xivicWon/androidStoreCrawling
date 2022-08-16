import datetime
import string
from entity.AppEntity import AppEntity

class MobileIndexDto :
    rank : int
    country_name : string
    market_name : string
    rank_type : string
    app_name : string
    publisher_name : string
    icon_url : string
    market_appid : string
    package_name : string
   
    def __init__(self, obj:object) -> None:
        self.of(obj)
 
 
    def of(self, obj :dict):
        self.rank = obj["rank"]
        self.country_name = obj["country_name"]
        self.market_name = obj["market_name"]
        self.rank_type = obj["rank_type"]
        self.app_name = obj["app_name"]
        self.publisher_name = obj["publisher_name"]
        self.icon_url = obj["icon_url"]
        self.market_appid = obj["market_appid"]
        self.package_name = obj["package_name"]
    
    def __str__(self):
        print('{} 예외처리 called'.format(__class__.__name__))
        return self.app_name
    
    def __enter__(self):
        print("enter")
        
        
    def __exit__(self):
        print("exit")
     
    def toAppEntity(self) -> AppEntity:
        appEntity = AppEntity()  
        appEntity.id = self.market_appid
        appEntity.market_num = appEntity.getMarketNumByName(self.market_name)
        appEntity.app_name = self.app_name
        appEntity.developer_num = 0
        appEntity.cate_num = 0
        appEntity.min_use_age = 0
        appEntity.mapping_code = appEntity.generateMappingCode(self.package_name)
        appEntity.is_active = 'Y'
        appEntity.last_update = datetime.datetime.now().strftime("%Y-%m-%d")
        if appEntity.market_num == 2 :
            appEntity.id = "id" + appEntity.id    

        return appEntity