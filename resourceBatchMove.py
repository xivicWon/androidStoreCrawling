# -*- coding: utf-8 -*-
# Resource( icon ) 일괄 이동 처리 파일.
#


import os
from module.FileManager import FileManager

fm = FileManager.instance()

def batchImageMove(dir: str):
    files = os.listdir(dir)
    
    ## image 경로로 새로운경로와ID 를 추출해야함.
    
    directories = fm.getRestoreDirecties( len(files))

    for dir in directories : 
        emptySpaceCount = dir.emptySpace 
        
    
    

def main():
        
    appleFileDir = "/images/apple"
    googleFileDir = "/images/google"
    batchImageMove(appleFileDir)
    batchImageMove(googleFileDir)
        

if __name__  == '__main__' :
    main()


        
# 1. 기존에 저장된 이미지를 변경. -> 새로 저장되는것들은 그대로 또 생성됨. -> 또 처리해주고. 방식은 같음.

