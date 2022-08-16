import datetime
from functools import reduce
import json
from typing import Dict

class AppEntity:
    num : int
    id : str 
    market_num : int
    developer_num : int
    cate_num : int
    app_name : str
    min_use_age : int
    mapping_code : str
    is_active : str 
    last_update : str
        
    def setId(self, id ):
        self.id = id
        return self

    def setAppName(self, app_name ):
        self.app_name = app_name 
        return self

    def setMarketNum( self, market_num):
        self.market_num = market_num
        return self
        
    def setIsActive( self, is_active):
        self.is_active = is_active
        return self
    
    def setDeveloperNum(self, developer_num): 
        self.developer_num = developer_num 
        return self
    
    def setLastUpdateCurrent(self  ):
        self.last_update = datetime.datetime.now().strftime("%Y%m%d")
        return self
        
    
    def setLastUpdate(self, last_update ):
        self.last_update = last_update 
        return self
    
    def getId(self):
        return self.id
    
    def getAppName(self ):
        return self.app_name 

    def getMarketNum( self):
        return self.market_num
        
    def getIsActive( self):
        return self.is_active
    
    def getDeveloperNum(self): 
        return self.developer_num
        
    def getLastUpdate(self ):
        return self.last_update
    
    
    def toString(self):
        return json.dumps(vars(self))
  
    def ofDict(self , obj:Dict):
        self.id = obj["id"]
        self.app_name = obj["app_name"]
        self.developer_num = obj["developer_num"]
        self.market_num = obj["market_num"]
        self.cate_num = obj["cate_num"]
        self.min_use_age = obj["min_use_age"]
        self.mapping_code = obj["mapping_code"]
        self.is_active = obj["is_active"]
        self.last_update = obj["last_update"]
        return self
    
    def generateMappingCode(self, str ):
        if str == None : 
            return ""
        else :
            return "__{}__".format( str)  
    
    
    def getMarketNumByName(self, str:str):
        if str == "google" :
            return 1 
        elif  str == "apple" :
            return 2 
        elif  str == "one" :
            return 3 

    def getInsertClause(self ):
        localVariable = vars(self)
        return "({})".format(
            ",".join(
                reduce(lambda acc, key : acc+["{}".format(key ) ] ,localVariable.keys(), [])
                )
            )
        
    def getInsertValueClause(self ):
        localVariable = vars(self)
        return "({})".format(
            ",".join(
                reduce(lambda acc, key : acc+["'{}'".format(localVariable[key] ) ] ,localVariable.keys(), [])
                )
            )
    
    