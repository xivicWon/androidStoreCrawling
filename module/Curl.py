import json
from requests import get, post
import requests

class Curl : 
    METHOD_POST:str ="post"
    METHOD_GET:str ="get"
    
    @staticmethod
    def request(method, url, data, headers, timeout=10)->requests.Response:
        if method == Curl.METHOD_GET:
            return Curl.get(url=url, header=headers, timeout=timeout )
        elif method ==Curl.METHOD_POST:
            return Curl.post(url, data=data, headers=headers, timeout=timeout)
        else :
            return None   
        
    @staticmethod
    def get(url:str, header, timeout)->requests.Response: 
        try :
            return get(url, headers=header, timeout=timeout)
        except requests.exceptions.ReadTimeout: 
            print("ReadTimeout - url : {} ".format(url))
            return None
        except requests.exceptions.ConnectionError: 
            print("ConnectionError - url : {} ".format(url))
            return None
        except requests.exceptions.ChunkedEncodingError:
            print("ChunkedEncodingError - url : {} ".format(url))
            return None
    
    @staticmethod
    def post( url, data, headers, timeout):
        try :
            return post(url, data=json.dumps(data) , headers=headers, timeout=timeout) 
        except requests.exceptions.ReadTimeout: 
            print("ReadTimeout - url : {} ".format(url))
            return None
        except requests.exceptions.ConnectionError: 
            print("ConnectionError - url : {} ".format(url))
            return None
        except requests.exceptions.ChunkedEncodingError:
            print("ChunkedEncodingError - url : {} ".format(url))
            return None

        