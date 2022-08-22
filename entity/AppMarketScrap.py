
import json
from typing import List
from entity.Entity import Entity

class AppMarketScrap(Entity):
    __num : int
    __market_num : int
    __scrap_name : str 
    __scrap_url : str 
    __scrap_argu : json
    
    def __init__(self) -> None:
        
        pass
    
    def ofDict(self, obj) :
        self.__num = obj["num"]
        self.__market_num = obj["market_num"]
        self.__scrap_name = obj["scrap_name"]
        self.__scrap_url = obj["scrap_url"]
        try : 
            self.__scrap_argu = json.loads(obj["scrap_argu"])
        except Exception : 
            self.__scrap_argu = json.loads("{}")
        return self
    
    def getScrapUrl(self):
        urls:List[str] = [] 
        if self.__market_num == 2 :
            urls.extend(self.getAppleScrapUrl())

        return urls
    
    
    def getAppleScrapUrl(self)->List[str]:    
        url = self.__scrap_url
        urls:List[str] = [] 
        queryStr = []
        if "ageId" in self.__scrap_argu:
           queryStr.append("ageId=" + self.__scrap_argu["ageId"])
           
        if "chart" in self.__scrap_argu and type(self.__scrap_argu["chart"]) == list :
            for chart in self.__scrap_argu["chart"] :
                queryStr.append("chart=" + chart)
                urls.append(url + "?" + "&".join(queryStr))
                queryStr.pop()

        return urls                