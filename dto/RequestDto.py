import requests

from dto.Dto import Dto


class RequestDto (Dto): 
    url : str
    response : requests.Response

    def __init__(self, url, response) -> None:
        self.url = url
        self.response = response    
    
    def getUrl(self):
        return self.url 
    
    def getResponse(self):
        return self.response 