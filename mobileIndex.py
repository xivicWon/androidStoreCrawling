import sys, rootpath
sys.path.append(rootpath.detect())
import requests, datetime
from typing import List

from threading import Thread
from multiprocessing import current_process
from dto.mobileIndex.MobileIndexDto import MobileIndexDto
from repository.MobileIndexRepository import MobileIndexRepository
from module.OpenDB_v3 import OpenDB 
from module.EnvStore import EnvStore 
from module.Curl import Curl 
from module.TimeChecker import TimeChecker

def getMobileIndex(url , data ):
    headers = getRequstHeader()
    response = Curl(url, headers= headers, data=data)
    if( response != None):
        responseList.append(response)

def filteredAliveThread(t:Thread):
    if t.is_alive() :
        return True
    else :
        t.join()
        return False
    
def getRequstHeader  () : 
    return {
        'Content-Type': 'application/json; charset=utf-8',
        'referer' : 'https://www.mobileindex.com/mi-chart/daily-rank'
    }


def getRequestData ( appType:str) : 
    return {
        'market': 'all',
        'country': 'kr',
        'rankType': 'gross',
        'appType': appType, 
        'date': datetime.datetime.now().strftime("%Y%m%d"),
        'startRank': 1,
        'endRank': 100
    }
    
def workToThread() :
    processName = current_process().name
    threadlist: List[Thread] = []

    url = "https://www.mobileindex.com/api/chart/global_rank_v2"
    threadlist.append(Thread(target=getMobileIndex , name="{} [{}th thread ]".format(processName, len(threadlist)), args=(url, getRequestData('game'),)))
    threadlist.append(Thread(target=getMobileIndex , name="{} [{}th thread ]".format(processName, len(threadlist)), args=(url, getRequestData('app'),)))

    for thread in threadlist:
        thread.start()
        
    for thread in threadlist:
        thread.join()
        

Env = EnvStore()
appStore = Env.getAppStore
openDB: OpenDB = OpenDB(appStore["host"], appStore["user_name"]  ,appStore["password"] , appStore["database"] )
mobileIndexRepository = MobileIndexRepository(openDB)

if __name__  == '__main__' :
    
    timeChecker = TimeChecker()
    timeChecker.start(code="main")
    responseList: List[requests.Request] = []
    startPoint = 0 
    print("작업 시작 ~ ")
    workToThread()
    
    for res in responseList :
        responseData = res.json()
        dataList = list(map(lambda t: MobileIndexDto().ofDict(t), responseData["data"]) )    
        mobileIndexRepository.save(dataList)
    
    
    timeChecker.stop(code="main")
    timeChecker.display(code="main")