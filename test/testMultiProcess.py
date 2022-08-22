from multiprocessing import current_process
from random import random
import sys, rootpath
from typing import List
sys.path.append(rootpath.detect())
from  MultiProcessThread import MultiProcess

def testWorking(param:int , dataSet: List):
    # print("testWorking:: {}".format(param))
    dataSet.append(param)

if __name__  == '__main__' :

    limitWorkCount = 1000
    crwlingJob = []
    while ( len(crwlingJob) < limitWorkCount): 
        crwlingJob.append(int( random() * 1000 ))

    mp = MultiProcess(jobList=crwlingJob , work=testWorking, threadCount=10, processCount=2)
    mp.run()

