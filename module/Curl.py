
import json
from requests import get, post
import requests

class Curl : 
        
    @staticmethod
    def request(method, url, data, headers, timeout=10)->requests.Response:
        if method == 'get' :
            return Curl.get(url=url, header=headers, timeout=timeout )
        elif method == "post":
            return Curl.post(url, data=data, headers=headers, timeout=timeout)
            
    @staticmethod
    def get(url:str, header, timeout)->requests.Response: 
        res = get(url, headers=header, timeout=timeout)
        try :
            return res
        except requests.exceptions.ReadTimeout: 
            return None
        except requests.exceptions.ConnectionError: 
            return None
        except requests.exceptions.ChunkedEncodingError:
            return None

    
    @staticmethod
    def post( url, data, headers, timeout):
        res = post(url, data=json.dumps(data) , headers=headers, timeout=timeout)
        try :
            return res
        except requests.exceptions.ReadTimeout: 
            return None
        except requests.exceptions.ConnectionError: 
            return None
        except requests.exceptions.ChunkedEncodingError:
            return None

        