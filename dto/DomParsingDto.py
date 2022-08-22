from dto.Dto import Dto


class DomParsingDto(Dto): 
    
    author: str
    developer_url: str
    appName: str
    
    def __init__(self , author, developer_url, appName ) -> None:
        self.author = author
        self.developer_url = developer_url
        self.appName = appName
        pass
    
    def getAuthor( self) : 
        return self.author
    
    def getUrl( self) : 
        return self.developer_url
    
    def getAppName( self) : 
        return self.appName