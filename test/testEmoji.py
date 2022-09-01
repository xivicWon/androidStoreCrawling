import sys, rootpath
import time
from urllib import parse

sys.path.append(rootpath.detect())
from repository.Repository import Repository
from service.Service import Service
from dto.Dto import Dto
import requests, json
from typing import  Callable, List
from bs4 import BeautifulSoup as bs
from bs4.element import Tag
from threading import Thread, current_thread 
from multiprocessing import Queue, current_process
from dto.AppDto import AppDto
from dto.AppWithDeveloperWithResourceDto import AppWithDeveloperWithResourceDto
from dto.RequestDto import RequestDto
from entity.AppEntity import AppEntity
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from entity.AppResourceEntity import AppResourceEntity
from module.Curl import Curl
from module.TimeChecker import TimeChecker

from urllib import request


requestUrl = "https://play.google.com/store/apps/details?id=calculator.scientific.accounting"

res:requests.Response = Curl.request("get", requestUrl, None, None)
try : 
    soup = bs(res.text, "html.parser")
    data = json.loads(soup.find('script', type='application/ld+json').text)
    data["id"] = res.url.split("id=").pop()
    data["author"]["id"] = soup.find("a", string=data['author']['name'])["href"]\
        .replace("/store/apps/developer?id=", "")\
        .replace("/store/apps/dev?id=", "")
    print(data["author"]["name"].encode("utf8"))
    developerUrl = "https://play.google.com/store/apps/developer?id=" + data["author"]["id"]
    print(developerUrl)
    res:requests.Response = Curl.request("get", developerUrl, None, None)
    print(res.status_code)
except AttributeError as e : 
    print("AttributeError] Response [status code : {} , url : {}, data : {} ]".format(res.status_code , res.url, data ))
except TypeError as e : 
    print("TypeError] Response [status code : {} , url : {}, data : {}  ]".format(res.status_code , res.url, data))
    print ( e)
