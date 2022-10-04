from entity.Entity import Entity

class ISOCountryCode(Entity):
    
    __num : int
    __name : str
    __alpha2 : str
    __alpha3 : str
    
    @property
    def getNum(self):
        return self.__num
    
    @property
    def getName(self):
        return self.__name
    
    @property
    def getAlpha2(self):
        return self.__alpha2
    
    @property
    def getAlpha3(self):
        return self.__alpha3
    
    def setNum(self, num ):
        self.__num = num
        return self
    
    def setName(self, name ):
        self.__name = name
        return self
    
    def setAlpha2(self, alpha2 ):
        self.__alpha2 = alpha2
        return self
    
    def setAlpha3(self, alpha3 ):
        self.__alpha3 = alpha3
        return self
    
    @staticmethod
    def ofDict(obj):
        iSOCountryCode = ISOCountryCode()
        iSOCountryCode.setNum(obj["num"])
        iSOCountryCode.setName(obj["name"])
        iSOCountryCode.setAlpha2(obj["alpha2"])
        iSOCountryCode.setAlpha3(obj["alpha3"])
        return iSOCountryCode