from entity.Entity import Entity

class AppResourceEntity(Entity):
        
    __app_num : int
    __resource_type : str
    __path : str 
    
    @property
    def getAppNum(self):
        return self.__app_num

    @property
    def getResourceType(self):
        return self.__resource_type

    @property
    def getPath(self):
        return self.__path

    def setAppNum(self, app_num):
        self.__app_num = app_num 
        return self
    
    def setResourceType(self, resource_type):
        self.__resource_type = resource_type
        return self
    
    def setPath(self, __path):
        self.__path = __path 
        return self
    
    @staticmethod
    def ofDict(obj:dict):
        appResourceEntity = AppResourceEntity()
        appResourceEntity.__app_num = obj["app_num"] if "app_num" in obj else None
        appResourceEntity.__resource_type = obj["resource_type"] if "resource_type" in obj else None
        appResourceEntity.__path = obj["path"] if "path" in obj else None
        return appResourceEntity