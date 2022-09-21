import requests

from dto.Dto import Dto


class RequestDto (Dto): 
    url : str
    response : requests.Response

    def __init__(self, url, response) -> None:
        self.url = url
        self.response = response    
    
    @property
    def getUrl(self):
        return self.url 
    
    @property
    def getResponse(self):
        return self.response 