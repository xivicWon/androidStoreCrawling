# -*- coding: utf-8 -*-
import sys, rootpath

sys.path.append(rootpath.detect())

from module.EnvManager import EnvManager 
from module.LogManager import LogManager

if __name__ == "__main__":
    
    envManager = EnvManager.instance()
    logManager = LogManager.instance()
    logManager.init(envManager)
    fileMapper = {
        "appleScrapByCategory" : "appleScrapByCategory.py",
        "googleScrapBySavedID" : "googleScrapBySavedID.py",
        "mobileIndexRankApi" : "mobileIndexRankApi.py",
        "appleScrapBySavedID" : "appleScrapBySavedID.py",
        "mobileIndexAppSearch" : "mobileIndexAppSearch.py"
    }
    try : 
        action = sys.argv[1]
        if action == None : 
            raise IndexError
    except IndexError: 
        logManager.error("입력 파라미터를 체크해 주세요. {}".format(sys.argv))
        exit()
        
    fileName = next(filter(lambda f : f == action , fileMapper), None)
    if fileName == None :
        logManager.error("파일을 찾을 수가 없습니다. \"{}\" ex) {}".format(action , ", ".join(list(fileMapper.keys()))))
        exit() 
        
    processingFiles = [fileMapper[fileName]]
    
    for file in processingFiles : 
        logManager.info("##################################")
        logManager.info("# Start File : {} ".format(file))
        logManager.info("##################################")
        exec(open( file=file,encoding="UTF8" ).read())
