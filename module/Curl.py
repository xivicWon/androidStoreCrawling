from enum import Enum
import requests, json

class CurlMethod (Enum): 
    POST = "POST"
    GET = "GET"
    
class Curl : 
    
    @staticmethod
    def request(method:CurlMethod, url:str, data:dict, headers:dict, timeout=10)->requests.Response:
        if method == CurlMethod.GET:
            return Curl.get(url=url, header=headers, timeout=timeout )
        elif method == CurlMethod.POST:
            return Curl.post(url=url, data=data, headers=headers, timeout=timeout)
        else :
            return None   
        
    @staticmethod
    def get(url:str, header:dict, timeout:int)->requests.Response: 
        return requests.get(url, headers=header, timeout=timeout)
       
    @staticmethod
    def post( url:str, data:dict, headers:dict, timeout:int):
        return requests.post(url, data=json.dumps(data) , headers=headers, timeout=timeout) 
       
        