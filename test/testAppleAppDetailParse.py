
from ast import Str

import rootpath, sys
sys.path.append(rootpath.detect())

import requests
from module.DomParser import DomParser
from module.Curl import Curl, CurlMethod
from dto.RequestDto import RequestDto

def requestUrl(url : str):
    header = {"Accept-Language" : "ko-KR"}
    res:requests.Response = Curl.request(method=CurlMethod.GET, url=url, headers=header, data=None ,timeout=10)
    data = RequestDto(url, res)
    DomParser.parseAppleAppDetail(data.getResponse())


url = "https://apps.apple.com/kr/app/id1257651611"
requestUrl(url)