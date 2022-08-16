from random import random
from typing import List
import time
from threading import Thread
from multiprocessing import Process,Queue , current_process

def workToProcess(crwlingJob:int,  q:Queue ) :
    processName = current_process().name
    maxThreadCount = 50
    jobCount = 1000
    threadlist: List[Thread] = []
    processData = []
    incJobCount = 0
    while( incJobCount < crwlingJob ):
        if len(threadlist) >= maxThreadCount :
            threadlist = list(filter( filteredAliveThread , threadlist))
        else :
            incJobCount += jobCount
            workThread = Thread(target=workToThread , name="{} [{}th thread ]".format(processName, len(threadlist)), args=(jobCount, processData))
            threadlist.append(workThread)
            workThread.start()

    if( len(threadlist) > 0 ):
        for t in threadlist :
            t.join()
    print("{} put Count : {} ".format( processName, format(len(processData), ",")))
    q.put(processData)
    
def filteredAliveThread(t: Thread):
    if t.is_alive() :
        t.join()
        return True
    else :
        return False

def workToThread (jobCount: int ,processData:List[int] ): 
    urls = generateRandom(jobCount)
    for url in urls :
        processData.append(url)

def workToConsumerProcess( q:Queue ):
    consumeCount = 0
    processResults = []
    while True :
        value = q.get()
        if value != QUEUE_CLOSE_WORD:
            consumeCount += 1 
            print("\tConsumer : {} [{}]".format(  format(len(value), ","), consumeCount))
            processResults.append(value)
        else :
            break
    result = []
    for items in processResults:
        result.extend(items)
    print( "\tConsumer Process Result : {} ".format(format(len(result) , ",")) )
    
def generateRandom(count: int):
    crwlingJob= []
    while ( len(crwlingJob) < count): 
        crwlingJob.append(int( random() * 1000 ))
    return crwlingJob

def main(): 
    start = time.time()
    queue = Queue()
    jobLengthEachProcess =  max(int(JOB_COUNT / MAX_PROCESS_COUNT), 1 )
    processList: List[Process] = []
    print("-------------------------------------------------------------")
    print("Process : {}  Total job : {} Each work : {}".format(format(MAX_PROCESS_COUNT, ","), format(JOB_COUNT , ","), format(jobLengthEachProcess , ",") ))
    print("-------------------------------------------------------------\n\n")
    processNum = 1
    incJobProcessCount = 0
    while len(processList) < MAX_PROCESS_COUNT  :
        incJobProcessCount += jobLengthEachProcess
        processList.append( Process(target=workToProcess , name="[ {}th ]".format(processNum), args=(jobLengthEachProcess, queue, ) ))
        processNum += 1 
    
    consumer = Process(target=workToConsumerProcess , name="[ consumer Process ]", args=(queue, ) )
    consumer.start()
    for process in processList:
        process.start()
    
    for process in processList:
        process.join()
        print(process.name + " >> {}".format("LIVE" if process.is_alive() else "DIE"))
    
    queue.put(QUEUE_CLOSE_WORD)
    consumer.join()
    
    print(" time : {}  ".format(time.time() - start  ))

QUEUE_CLOSE_WORD= "None"
MAX_PROCESS_COUNT = 5
JOB_COUNT = 10000000
if __name__  == '__main__' :
    main()
    