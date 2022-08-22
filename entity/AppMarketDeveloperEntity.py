import json
from typing import Dict
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
    
    def setDeveloperName(self , developer_name  ):
        self.__developer_name = developer_name 
        return self
    
    def setCompanyNum(self , company_num  ):
        self.__company_num = company_num 
        return self
    
    def ofDict(self , obj:Dict):
        self.__num = obj["num"]
        self.__market_num = obj["market_num"]
        self.__company_num = obj["company_num"]
        self.__developer_name = obj["developer_name"]
        self.__developer_market_id = obj["developer_market_id"]
        self.__group_code = obj["group_code"]
        return self