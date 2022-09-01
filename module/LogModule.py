from abc import *
class LogModule(metaclass=ABCMeta) :
    
    def __new__(cls) :
        return super().__new__(cls)
    
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def debug(self, msg) : 
        pass
        
    @abstractmethod
    def info(self, msg) : 
        pass
    
    @abstractmethod
    def warning(self, msg) :
        pass
    
    @abstractmethod
    def error(self, msg) : 
        pass
        
    @abstractmethod
    def critical(self, msg) : 
        pass
    
    