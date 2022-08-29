import datetime
from typing import Callable, List
from entity.Entity import Entity

class AppEntity(Entity):
    __num : int
    __id : str 
    __market_num : int
    __developer_num : int
    __cate_num : int
    __app_name : str
    __min_use_age : int
    __mapping_code : str
    __is_active : str 
    __last_update : str
    __rating : int 
    
    @property
    def getNum(self):
        return self.__num
    
    @property
    def getId(self):
        return self.__id
    
    @property
    def getAppName(self ):
        return self.__app_name 
    
    @property
    def getMarketNum( self):
        return self.__market_num
    
    @property
    def getIsActive( self):
        return self.__is_active
    
    @property
    def getDeveloperNum(self): 
        return self.__developer_num
    
    @property
    def getLastUpdate(self ):
        return self.__last_update
    
    @property
    def getMappingCode(self ):
        return self.__mapping_code
    
    @property
    def getRating(self):
        return self.__rating
    
    
    def setId(self, id ):
        self.__id = id
        return self

    def setNum(self, num ):
        self.__num = num
        return self

    def setAppName(self, app_name ):
        self.__app_name = app_name 
        return self

    def setMarketNum( self, market_num):
        self.__market_num = market_num
        return self
        
    def setIsActive( self, is_active):
        self.__is_active = is_active
        return self
    
    def setDeveloperNum(self, developer_num): 
        self.__developer_num = developer_num 
        return self
    
    def setCateNum(self, cate_num):
        self.__cate_num = cate_num
        return self 
    
    def setMinUseAge(self, min_use_age):
        self.__min_use_age = min_use_age
        return self 
    
    def setLastUpdateCurrent(self):
        self.__last_update = datetime.datetime.now().strftime("%Y%m%d")
        return self
    
    def setRating (self, rating) :
        self.__rating = rating
        return self
    
    def setLastUpdate(self, last_update:datetime.date):
        self.__last_update = last_update.strftime("%Y%m%d") if last_update == datetime.date else None
        return self
    
    def setMappingCode(self, mapping_code) :
        self.__mapping_code = mapping_code
        return self
  
    def ofDict(self , obj:dict):
        self.__num = obj["num"] if "num" in obj else 0
        self.__id = obj["id"]
        self.__app_name = obj["app_name"] 
        self.__developer_num = obj["developer_num"]
        self.__market_num = obj["market_num"] 
        self.__cate_num = obj["cate_num"] 
        self.__min_use_age = obj["min_use_age"] 
        self.__mapping_code = obj["mapping_code"] if 'mapping_code' in obj else ""
        self.__is_active = obj["is_active"]  if 'is_active' in obj else ""
        # self.__last_update = obj["last_update"].strftime("%Y%m%d") if 'last_update' in obj and type(obj["last_update"]) == datetime.date else ""
        self.setLastUpdate(obj["last_update"] if 'last_update' in obj else None)
        self.__rating = obj["rating"] if 'rating' in obj else 0  
        return self
    
    def ofManyDict (self, objs:List[dict]) :
        condition: Callable[[dict] , AppEntity] = lambda o : AppEntity().ofDict(o)
        return list(map(condition, objs))
    
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