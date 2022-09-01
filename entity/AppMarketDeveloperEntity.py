from typing import Dict, List
from entity.Entity import Entity
class AppMarketDeveloperEntity(Entity) :
    __num : int 
    __market_num : int 
    __company_num : int 
    __developer_name : str
    __developer_market_id : str
    __group_code : str
    
    @property
    def getNum(self):
        return self.__num
    
    @property
    def getMarketNum(self):
        return self.__market_num
    
    @property
    def getCompanyNum(self):
        return self.__company_num
    
    @property
    def getDeveloperName(self):
        return self.__developer_name

    def getDecodeDeveloperName(self) : 
        # return self.__developer_name.encode("ASCII").decode("unicode-escape")
        return self.__developer_name
    
    @property
    def getDeveloperMarketId(self):
        return self.__developer_market_id
    
    @property
    def getGroupCode(self):
        return self.__group_code
    
    def setDeveloperMarketId( self, developer_market_id):
        self.__developer_market_id = developer_market_id
        return self
    
    def setMarketNum( self , market_num:int):
        self.__market_num = market_num
        return self
    
    def setDeveloperName(self , developer_name: str):
        # self.__developer_name = developer_name.encode("unicode-escape").decode("ASCII")
        self.__developer_name = developer_name
        return self
    
    def setCompanyNum(self , company_num:int  ):
        self.__company_num = company_num 
        return self
    
    def ofDict(self , obj:Dict):
        self.__num = obj["num"]
        self.__market_num = obj["market_num"]
        self.__company_num = obj["company_num"]
        self.__developer_name = obj["developer_name"]
        self.__developer_market_id = obj["developer_market_id"]
        # emoji 방식으로 할 경우 php 에러 load convert 해줄 수 있어야함. 그 외 다른 서비스에서도... 그래서 제외.
        # self.__developer_name = emoji.emojize(obj["developer_name"])
        # self.__developer_market_id = emoji.emojize(obj["developer_market_id"])
        self.__group_code = obj["group_code"]
        return self
    
    def ofManyDict(self , objs:List[Dict])->List:
        appMarketDeveloperEntities:List[AppMarketDeveloperEntity] = []
        for obj in objs :
            appMarketDeveloperEntity = AppMarketDeveloperEntity()
            appMarketDeveloperEntities.append(appMarketDeveloperEntity.ofDict(obj))
        return appMarketDeveloperEntities
    