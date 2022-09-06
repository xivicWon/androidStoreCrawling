import os
from dotenv import load_dotenv
from module.SingletonInstance import SingletonInstance

class EnvManager(SingletonInstance) : 
    
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_DATABASE: str
    
    LOG_STATUS:bool
    LOG_LEVEL:str
    LOG_PATH:str
    LOG_NAME:str
    LOG_MAX_DAY:int
    
    LOG_ERROR_STATUS:bool
    LOG_ERROR_LEVEL:str
    LOG_ERROR_PATH:str
    LOG_ERROR_NAME:str
    LOG_ERROR_MAX_DAY:int
    def __init__(self) -> None:
        load_dotenv()
        self.__setEnv()
        pass
        
    def __setEnv(self):
        self.DB_HOST= os.environ.get("APPSTORE.HOST")
        self.DB_DATABASE = os.environ.get("APPSTORE.DATABASE")
        self.DB_USER = os.environ.get("APPSTORE.DATABASE_USER")
        self.DB_PASSWORD = os.environ.get("APPSTORE.DATABASE_USER_PASS")

        self.LOG_STATUS = EnvManager.getStatus(os.environ.get("LOG.STATUS"))
        self.LOG_LEVEL = EnvManager.getLevel(os.environ.get("LOG.LEVEL")) 
        self.LOG_PATH= os.environ.get("LOG.PATH")
        self.LOG_NAME = os.environ.get("LOG.NAME")
        self.LOG_MAX_DAY = EnvManager.getMaxDay(os.environ.get("LOG.LOG_MAX_DAY"))

        self.LOG_ERROR_STATUS = EnvManager.getStatus(os.environ.get("LOG.ERROR_STATUS"))
        self.LOG_ERROR_LEVEL = EnvManager.getLevel(os.environ.get("LOG.ERROR_LEVEL"))
        self.LOG_ERROR_PATH= os.environ.get("LOG.ERROR_PATH")
        self.LOG_ERROR_NAME = os.environ.get("LOG.ERROR_NAME")
        self.LOG_ERROR_MAX_DAY = EnvManager.getMaxDay(os.environ.get("LOG.LOG_ERROR_MAX_DAY"))

    @staticmethod 
    def getStatus( value ):
        return value == "ON" 
    
    @staticmethod 
    def getLevel( value ):
        levels = ['CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']
        return value if value in levels else 'INFO'
    
    @staticmethod 
    def getMaxDay(value):
        try : 
            return int(value)
        except (TypeError, ValueError) as e :
            return 5 


