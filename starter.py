# -*- coding: utf-8 -*-
if __name__ == "__main__":
    
    scrapingAppleStore ="scrapingAppleStore.py"
    mobileIndexRank ="mobileIndexRank.py"
    scrapingGoogleStore ="scrapingGoogleStore.py" 
    
    # processingFiles = [mobileIndexRank,scrapingAppleStore, scrapingGoogleStore]
    processingFiles = [scrapingGoogleStore]
    for file in processingFiles : 
        print("#############################")
        print("# ")
        print("# Start File : {} ".format(file))
        print("# ")
        print("#############################")
        exec(open(file).read())
