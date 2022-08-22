
from requests import get
import requests

class Curl : 
        
    def request(self, url:str)->requests.Response: 
        res = get(url, timeout=10)
        try :
            return res
        except requests.exceptions.ReadTimeout: 
            return None
        except requests.exceptions.ConnectionError: 
            return None
        except requests.exceptions.ChunkedEncodingError:
            return None
