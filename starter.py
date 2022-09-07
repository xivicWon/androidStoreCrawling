# -*- coding: utf-8 -*-
import sys, rootpath

sys.path.append(rootpath.detect())

from module.EnvManager import EnvManager 
from module.LogManager import LogManager

if __name__ == "__main__":
    
    envManager = EnvManager.instance()
    logManager = LogManager.instance()
    logManager.init(envManager)
    scrapingAppleStore ="scrapingAppleStore.py"
    mobileIndexRank ="mobileIndexRank.py"
    scrapingGoogleStore ="scrapingGoogleStore.py" 
    processingFiles = [mobileIndexRank,scrapingAppleStore, scrapingGoogleStore]
    # processingFiles = [scrapingGoogleStore]
    # processingFiles = [scrapingAppleStore]
    # processingFiles = [mobileIndexRank]
    for file in processingFiles : 
        logManager.info("##################################")
        logManager.info("# Start File : {} ".format(file))
        logManager.info("##################################")
        exec(open( file=file,encoding="UTF8" ).read())
