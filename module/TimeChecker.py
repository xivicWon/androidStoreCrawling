from math import ceil
from time import time

class TimeChecker : 
    __timeLine: dict
    __ceilingLevel :int = 1000
    def __init__(self) -> None:
        self.__timeLine = {}
        pass
    
    def start(self, code:str):
        if not code in self.__timeLine :
            self.__timeLine[code] = {}
        self.__timeLine[code]["start"] = time()
        
    def stop(self, code:str):
        if not code in self.__timeLine :
            self.__timeLine[code] = {}
        self.__timeLine[code]["stop"] = time()
        
        
    def display(self, code :str):
        if not code in self.__timeLine \
            or not "start" in  self.__timeLine[code] \
            or not "stop" in  self.__timeLine[code]:
            print( "{} 는 Start와 Stop 되지 않은 코드입니다.".format(code) ) 
        else :
            print("{} Time : {}  ".format(code,ceil(( self.__timeLine[code]["stop"] - self.__timeLine[code]["start"]) * self.__ceilingLevel) / self.__ceilingLevel))
            
            