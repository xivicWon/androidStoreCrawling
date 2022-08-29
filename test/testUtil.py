
import keyword


class TestDto :
    __a : str
    __b : str
    __c : str
    
    @property
    def get__a(self) :
        return self.__a
    
    @property
    def get__b(self) :
        return self.__b    
    
    
    @property
    def get__c(self) :
        return self.__c 
    
    def setA(self,a):
        self.__a = a 
        return self
        
    def setB(self,b):
        self.__b = b 
        return self
    
    def setC(self,c):
        self.__c = c 
        return self
    
    def var(self):
        return vars(self)

    def name(self):
        return type(self).__name__

class Util :
    @staticmethod
    def toDict(dto:TestDto) :
        className = type(dto).__name__
        keys = dto.var().keys()
        keyFields = map(lambda s : s.replace("_"+ className , "")  , keys)
        values = list(dto.var().values())
        print(values)
        returnDic = {}
        for idx, key in enumerate(keyFields):
            print("{}, {}".format(idx, key ))
            returnDic[key] = values[idx]
        
        print(returnDic)
        
    
    
testDto = TestDto()
testDto.setA("100").setB("200").setC("300")
    
    
Util.toDict(testDto)