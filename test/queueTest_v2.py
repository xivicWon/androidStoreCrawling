from random import random
from typing import List
import time
from threading import Thread
from multiprocessing import Process,Queue , current_process


def workToThread(crwlingJob:list,  q:Queue ) :
    processName = current_process().name
    maxThreadCount = 50
    # print("{} thread working Count : {}".format(processName, len(crwlingJob)))
    threadlist: List[Thread] = []
    # print("in Thread Work Count : {}".format(len(crwlingJob))) 
    while( len(crwlingJob) >= 1 ):
        url = crwlingJob.pop()
        work(url,q )
        
        
        if len(threadlist) >= maxThreadCount :
            # 전체 내역중에 종료된 내역이 있는지 체크.
            threadlist = list(filter( filteredAliveThread , threadlist))
            None
        else :
            url = crwlingJob.pop()
            workThread = Thread(target=work , name="{} [{}th thread ]".format(processName, len(threadlist)), args=(url,q ))
            threadlist.append(workThread)
            workThread.start()

    for thread in threadlist:
        thread.join()



def filteredAliveThread(t: Thread):
    if t.is_alive() :
        t.join()
        return True
    else :
        return False


def work (data: int , q:Queue  ): 
    processName = current_process().name
    # print( "processName : {} Thread name : {} ".format(processName,current_thread().getName()  ))
    # print("{} > Queue Stack Length : {} ".format(time.time() ,data, q.qsize()))
    # print("working {}".format(data))
    if not q.full():
        q.put(data)
   
def getAllItemInQueue(q : Queue)->List[int]:
    item = []
    while not q.empty():
        value = q.get()
        item.append(value)
        
    print("Put itemCount : {}".format(len(item)))
    return item 


if __name__  == '__main__' :
    start = time.time()
    # Google MarketNum
    marketNum = 1 
    limitWorkCount = 100000
    q = Queue(limitWorkCount)
    crwlingJob= []
    while ( len(crwlingJob) < limitWorkCount): 
        crwlingJob.append(int( random() * 1000 ))
        
    jobCount = len(crwlingJob)
    MAX_PROCESS_COUNT = 5 
    jobLengthEachProcess =  max(int(jobCount / MAX_PROCESS_COUNT)  ,1 )
    processList: List[Process] = []
    startPoint = 0 
    print(" process : {}  total job length : {} each work : {} ".format(MAX_PROCESS_COUNT, jobCount, jobLengthEachProcess ))
    print("총 {} 건 작업 시작~ ".format(jobCount)) 
    processNum = 1
    while len(crwlingJob) > 0  :
        processJob = crwlingJob[:jobLengthEachProcess]
        if len(processJob) > 0 : 
            del crwlingJob[:jobLengthEachProcess]
            processList.append( Process(target=workToThread , name="[ {}th process ]".format(processNum), args=(processJob,q, ) ))
            processNum += 1 

    # print("processlist Count {}".format(len(processList)))

    allItem = []
    for process in processList:
        process.start()
        # print(process.name + " >> {}".format("LIVE" if process.is_alive() else "DIE"))
        # allItem.extend( getAllItemInQueue(q) )
        
    for process in processList:
        allItem.extend( getAllItemInQueue(q))
        process.join()
        # print(process.name + " >> {}".format("LIVE" if process.is_alive() else "DIE"))



    allItem.extend( getAllItemInQueue(q))
    print("itemCount : {}".format(len(allItem)))
    print(" time : {}  ".format(time.time() - start  ))
    