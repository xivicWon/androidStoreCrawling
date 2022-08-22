from entity.Entity import Entity

class AppResourceEntity(Entity):
        
    __app_num : int
    __resource_type : str
    __path : str 
    
    def ofDict(self, obj:dict):
        self.__app_num = obj["app_num"]
        self.__resource_type = obj["resource_type"]
        self.__path = obj["path"]

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
    
    def setPath(self, path):
        self.__path = path 
        return self
    

