# -*- coding: utf-8 -*-
import sys, rootpath

sys.path.append(rootpath.detect())

from module.LogManager import LogManager

if __name__ == "__main__":
    
    scrapingAppleStore ="scrapingAppleStore.py"
    mobileIndexRank ="mobileIndexRank.py"
    scrapingGoogleStore ="scrapingGoogleStore.py" 
    processingFiles = [mobileIndexRank,scrapingAppleStore, scrapingGoogleStore]
    # processingFiles = [scrapingGoogleStore]
    for file in processingFiles : 
        LogManager.info("start >> [{}]".format(file))        
        print("#############################")
        print("# Start File : {} ".format(file))
        print("#############################")
        exec(open( file=file,encoding="utf8" ).read())
