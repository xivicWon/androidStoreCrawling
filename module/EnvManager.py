import os
from dotenv import load_dotenv

class EnvManager : 
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_DATABASE: str
    
    LOG_LEVEL : str
    LOG_PATH : str
    LOG_FILENAME : str
    def __init__(self) -> None:
        load_dotenv()
        self.__setEnv()
        pass
    
    def __setEnv(self):
        self.DB_HOST= os.environ.get("APPSTORE.HOST")
        self.DB_DATABASE = os.environ.get("APPSTORE.DATABASE")
        self.DB_USER = os.environ.get("APPSTORE.DATABASE_USER")
        self.DB_PASSWORD = os.environ.get("APPSTORE.DATABASE_USER_PASS")

        self.LOG_LEVEL = os.environ.get("LOG.LEVEL")
        self.LOG_PATH= os.environ.get("LOG.PATH")
        self.LOG_FILENAME = os.environ.get("LOG.FILENAME")


