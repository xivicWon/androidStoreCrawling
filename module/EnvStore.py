import os
from dotenv import load_dotenv

class EnvStore : 
    __appStore :dict  
    
    
    def __init__(self) -> None:
        load_dotenv()
        self.__setAppStore()
        pass
    
    @property
    def getAppStore(self):
        return self.__appStore
    
    def __setAppStore(self):
        self.__appStore  = {}
        self.__appStore["host"] = os.environ.get("APPSTORE.HOST")
        self.__appStore["database"] = os.environ.get("APPSTORE.DATABASE")
        self.__appStore["user_name"] = os.environ.get("APPSTORE.DATABASE_USER")
        self.__appStore["password"] = os.environ.get("APPSTORE.DATABASE_USER_PASS")


