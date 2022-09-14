import sys, rootpath

sys.path.append(rootpath.detect())
from typing import  Callable, List
from threading import Thread
from multiprocessing import Process, Queue, current_process
class MultiProcessThread :
    __processCount: int 
    __maxThreadCount: int 
    __jobList : List
    __hasConsumer : bool
    __supplier : Callable
    __consumer : Callable
     
    def __init__(self, processCount:int, maxThreadCount:int , supplier: Callable ):
        self.__processCount = processCount
        self.__maxThreadCount = maxThreadCount
        self.__hasConsumer = False
        self.__supplier = supplier
        pass 
    
    
    def addThreadJob (self, jobList:List):
        self.__jobList = jobList
        return self
    
    def run(self):
        q = Queue()
            
        if(self.__hasConsumer):
            consumer = Process(target=self.__consumer , name="[ consumer process ]", args=(q,))
            consumer.start()
            
        jobCount = len(self.__jobList)
        jobLengthEachProcess = max( jobCount % self.__processCount, 
                                   int(jobCount / self.__processCount))
        processList: List[Process] = []
        processNum = 0
        while len(self.__jobList) > 0:
            if len(processList) + 1 == self.__processCount:
                processJob = self.__jobList[:]
                del self.__jobList[:]
            else :
                processJob = self.__jobList[:jobLengthEachProcess]
                del self.__jobList[:jobLengthEachProcess]
                
            if len(processJob) > 0 : 
                processNum += 1 
                processList.append(
                    Process( 
                        target=self.workToProcess , 
                        name="[ {}th process ]".format(processNum), 
                        args=(self.__maxThreadCount, q, self.__supplier,  processJob) 
                    )
                )
                
        print("** Total Process Count {}".format(len(processList)))
        
        for process in processList:
            process.start()
            print(process.name + " >> {}".format("LIVE" if process.is_alive() else "DIE"))
        
        for process in processList:
            process.join()
            print(process.name + " >> {}".format("LIVE" if process.is_alive() else "DIE"))
        
        q.put("None")
        if(self.__hasConsumer):
            consumer.join()
        q.close()
        
        
    def setConsumer(self, consumer: Callable) : 
        self.__hasConsumer = True
        self.__consumer = consumer
    
    def workToProcess(self, threadCount : int , q : Queue, callBack : Callable, jobList: list) :
        processName = current_process().name
        threadlist: List[Thread] = []
        allThreadList: List[Thread] = []
        responseList:List = [] 
        errorList : List = []
        threadIndex = 0 
        jobCount = len(jobList)
        print("workToProcess Count : {0:,}".format(jobCount))
        while( len(jobList) >= 1 ):
            if len(threadlist) >= threadCount :
                threadlist = list(filter( self.filteredAliveThread , threadlist))
            else :
                objItem = jobList.pop()
                ## 여러개의 작업리스트를 전달하도록.
                threadIndex += 1 
                workThread = Thread(
                    target=callBack ,
                    name="{} [{}th thread ]".format(processName, threadIndex), 
                    args=(objItem, responseList, errorList, )
                )
                threadlist.append(workThread)
                allThreadList.append(workThread)
                workThread.start()
                
        for thread in allThreadList:
            thread.join()
        
        # info = "{}'s Result ]  {} / {} ".format(processName , len(responseList), jobCount)
        # q.put(info)
        q.put(responseList)
        q.put(errorList)
            
    def filteredAliveThread(self, t : Thread):
        if t.is_alive() :
            return True
        else :
            t.join()
            return False
        