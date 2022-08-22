import rootpath
import sys
sys.path.append(rootpath.detect())
from entity.Entity import Entity

class AppEntity(Entity):
    __num : int
    __id : str 
    __market_num : int

    @property
    def getId(self):
        return self.__id
    
    @property
    def getNum(self):
        return self.__num
    
    @property
    def getMarketNum( self):
        return self.__market_num
    
    @getId.setter
    def setId(self, id ):
        self.__id = id
        return self

    @getNum.setter
    def setNum(self, num ):
        self.__num = num
        return self

    @getMarketNum.setter
    def setMarketNum( self, market_num):
        self.__market_num = market_num
        return self
        
    def ofDict(self , obj:dict):
        self.__num = obj["num"] if "num" in obj else 0
        self.__id = obj["id"]
        self.__market_num = obj["market_num"] 
        return self
        
    def of(self , obj:dict):
        print(self.__annotations__)
        fields = vars(self)
        print(fields)
        for key in obj:
            setattr(self,  key , obj[key])
        return self
    
    
appEntity = AppEntity()
obj:dict = {}
obj["id"] = "abc"
obj["num"] = 10
obj["market_num"] = 1

print(appEntity.of(obj).toString())

