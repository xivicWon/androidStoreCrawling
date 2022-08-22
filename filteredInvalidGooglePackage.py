import sys, rootpath 
sys.path.append(rootpath.detect())
import requests, time
from threading import Thread, current_thread 
from multiprocessing import Process, current_process
from module.EnvStore import EnvStore 
from module.OpenDB import OpenDB
from repository.PackageRepository import PackageRepository

Env = EnvStore()
appStore = Env.getAppStore
openDB: OpenDB = OpenDB(appStore["host"], appStore["user_name"]  ,appStore["password"] , appStore["database"] )

class ThreadResult:
    done_package = []
    success_package = []
    
    @classmethod 
    def addFail (self, item) :
        self.done_package.append(item)

    @classmethod 
    def getFail(self):
        return self.done_package
    
    @classmethod 
    def addSuccess (self, item) :
        self.success_package.append(item)

    @classmethod 
    def getSuccess(self):
        return self.success_package


def getGoogleAppStore(url):
    prefixUrl = "https://play.google.com/store/apps/details?id="
    requestUrl = prefixUrl + url
    # with urllib.request.urlopen(url, timeout=timeout) as conn:
    # conn.read()        
    try:
        res = requests.get(requestUrl, timeout=2)
        if res.status_code == 404 :
            ThreadResult.addFail(url)
        else :
            ThreadResult.addSuccess(url)

    except requests.exceptions.ReadTimeout: 
        return 
        # print(current_thread().getName() + " request Fail : {}".format(requestUrl))
    except requests.exceptions.ConnectionError: 
        return 
        # print(current_thread().getName() + "request Fail : {}".format(requestUrl))
    except requests.exceptions.ChunkedEncodingError:
        return 

def filteredAliveThread(t):
    if t.is_alive() :
        return True
    else :
        t.join()
        return False


def workToThread(crwlingJob:list ) :
    processName = current_process().name
    maxThreadCount = 400
    totalJobCount = len(crwlingJob)
    threadlist: list[Thread] = []
    allThreadList: list[Thread] = []
    # print("in Thread Work Count : {}".format(len(crwlingJob))) 
    while( len(crwlingJob) >= 1 ):
        if len(threadlist) >= maxThreadCount :
            # 전체 내역중에 종료된 내역이 있는지 체크.
            # threadlist = list(filter( lambda t: isinstance( t, Thread) and t.is_alive() , threadlist))
            threadlist = list(filter( filteredAliveThread , threadlist))
            # if closedThreadCount > 0 :
                # print( "{} 개의 프로세스 Joined".format( closedThreadCount ) )
        else :
            url = crwlingJob.pop()
            workThread = Thread(target=getGoogleAppStore , name="{} [{}th thread ]".format(processName, len(threadlist)), args=(url,))
            threadlist.append(workThread)
            allThreadList.append(workThread)
            workThread.start()

    for thread in allThreadList:
        thread.join()
    if len( ThreadResult.getFail()) > 0 :
        packageRepository.inactivePackages(ThreadResult.getFail() )
        
    if len( ThreadResult.getSuccess()) > 0 :
        packageRepository.activePackages(ThreadResult.getSuccess() )

    networkFail = totalJobCount - len(ThreadResult.getSuccess()) - len(ThreadResult.getFail())
    print (current_thread().getName() + "totalCount : {} Success : {} Fail : {} Network Fail : {}".format(totalJobCount, len(ThreadResult.getSuccess()), len(ThreadResult.getFail()),networkFail ))

crwlingJob = []
start = time.time()
openDB: OpenDB = OpenDB(appStore["host"], appStore["user_name"]  ,appStore["password"] , appStore["database"] )
packageRepository: PackageRepository = PackageRepository(openDB)
if __name__  == '__main__' :
    jobCount = 10000
    MAX_PROCESS_COUNT = 4
    jobLengthEachProcess = int(jobCount / MAX_PROCESS_COUNT)
    sqlResult = packageRepository.findAppIdbyOffset(0, jobCount )
    crwlingJob.extend(sqlResult)
    processList: 'list[Process]' = []
    startPoint = 0 
    print(" process : {}  total job length : {} each work : {} ".format(MAX_PROCESS_COUNT, jobCount, jobLengthEachProcess ))
    print("총 {} 건 작업 시작~ ".format(len(crwlingJob)) )
    if len(crwlingJob) > jobLengthEachProcess :
        processNum = 1
        while len(crwlingJob) > 0 and len(processList) < MAX_PROCESS_COUNT :
            processJob = crwlingJob[:jobLengthEachProcess]
            del crwlingJob[:jobLengthEachProcess]
            processList.append( Process(target=workToThread , name="[ {}th process ]".format(processNum), args=(processJob,) ))
            processNum += 1 
    else :
        processList.append( Process(target=workToThread , name="[ 0th process ]", args=(crwlingJob,)))
    
    print("processlist Count {}".format(len(processList)))

    for process in processList:
        process.start()
        print(process.name + " >> {}".format("LIVE" if process.is_alive() else "DIE"))

    
    for process in processList:
        process.join()
        print(process.name + " >> {}".format("LIVE" if process.is_alive() else "DIE"))

    print(" time : {}  ".format(time.time() - start  ))