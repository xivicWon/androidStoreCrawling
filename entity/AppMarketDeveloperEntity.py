import json
from typing import Dict


class AppMarketDeveloperEntity :
    num : int 
    market_num : int 
    company_num : int 
    developer_name : str
    developer_market_id : str
    group_code : str
    
    def setDeveloperMarketId( self, developer_market_id):
        self.developer_market_id =developer_market_id 
        return self
    
    def setMarketNum( self , market_num):
        self.market_num = market_num
        return self
    
    def setDeveloperName(self , developer_name  ):
        self.developer_name = developer_name 
        return self
    
    def setCompanyNum(self , company_num  ):
        self.company_num = company_num 
        return self
    
    def getNum (self): 
        return self.num
    
    def toString(self):
        return json.dumps(vars(self))
    
    def ofDict(self , obj:Dict):
        self.num = obj["num"]
        self.market_num = obj["market_num"]
        self.company_num = obj["company_num"]
        self.developer_name = obj["developer_name"]
        self.developer_market_id = obj["developer_market_id"]
        self.group_code = obj["group_code"]
        return self