
from dto.AppWithDeveloperWithResourceDto import AppWithDeveloperWithResourceDto
from dto.Dto import Dto

class ThreadJobDto (Dto): 
    __url : str
    __resourceDir: str
    __dto : AppWithDeveloperWithResourceDto
    
    def __init__(self, url , resourceDir, dto) -> None:
        self.__url = url
        self.__resourceDir = resourceDir
        self.__dto = dto
    
    @property
    def getUrl(self):
        return self.__url 
    
    @property
    def getResourceDir(self):
        return self.__resourceDir 
    
    