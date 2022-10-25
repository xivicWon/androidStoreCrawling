
import sys, rootpath
sys.path.append(rootpath.detect())
from dto.Dto import Dto
import datetime as dt
from module.playwright.MobileIndexCookie import MobileIndexCookie
class MIRequestDto(Dto) :
    __market : str
    __country : str
    __rankType : str
    __appType : str
    __date : str
    __startRank : int 
    __endRank : int
   
    def __init__(self) -> None: 
        pass
 
    @property
    def getMarket(self):
        return self.__market
    @property
    def getCounty(self):
        return self.__country
    @property
    def getRankType(self):
        return self.__rankType
    @property
    def getAppType(self):
        return self.__appType
    @property
    def getDate(self):
        return self.__date
    @property
    def getStartRank(self):
        return self.__startRank
    @property
    def getEndRank(self):
        return self.__endRank
    
    def setMarket(self, market):
         self.__market = market
    
    def setCounty(self, country):
         self.__country = country
    
    def setRankType(self,rankType):
         self.__rankType= rankType
    
    def setAppType(self,appType):
         self.__appType = appType
    
    def setDate(self, date):
         self.__date = date
    
    def setStartRank(self, startRank):
         self.__startRank = startRank
    
    def setEndRank(self, endRank):
         self.__endRank = endRank
    
    def toDict(self):
        return {
            "market" : self.__market,
            "country" : self.__country,
            "rankType" : self.__rankType,
            "appType" : self.__appType,
            "date" : self.__date,
            "startRank" : self.__startRank,
            "endRank" : self.__endRank,
        }
        
    @staticmethod   
    def generateSecretKey():
        secret = MobileIndexCookie.getMobileIndexSecretCode()
        secretWord = "ihateyousomuch"
        key = list(secretWord)
        secretCode = "983272129"
        splitCode = secret.split(secretCode)
        today = dt.datetime.utcnow() + dt.timedelta(hours=9)
        today.replace(hour=int(splitCode[0]),minute=int(splitCode[1]), second=0)
        secretDate = today - dt.timedelta(hours=9)
        mappingCode = "{}{}{}".format(secretDate.year, secretDate.month -1 , secretDate.day  ) 
        return "".join(map(lambda t : key[int(t)] , list(str(int(mappingCode)>>1))))