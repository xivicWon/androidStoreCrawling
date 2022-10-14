# fileCount(dir) 디렉토리에 파일 갯수 조회 함수.

# getDirEmptySpaceList(dir, fileCount) 해당 디렉토리 내에 파일 갯수를 저장할 수 있는 경로를 object 로 반환 
# - [ {path : '/tmp/10022' , emptySpace: 1000 }, {path : '/tmp/10022' , emptySpace: 1000 } ] 

# fileMove(before, after) 파일을 이동시키고 그 결과 경로를 반환

# 디렉토리별 최대 파일갯수 제한.

# 처리할 파일 목록을 조회.(db)
# 저장할 디렉토리 체크. 가장 마지막에 생성된 디렉토리경로 및 파일 갯수 조회.
# /1111 에 파일 400개 있음. 1000개 제한일때 600개 가능. 


# 신규 디렉토리 부여

# 파일 이동 및 DB 업데이트.


# 기존에 저장할때 고정된 경로로 저장.
# - 이동에 대한 자원낭비가 없음.
# - 방법의 불투명성. 
# 저장전 데이터를 조회하고, 데이터가 있으면, 이미지 저장은 제외? 
import datetime
import os
import random
from module.SingletonInstance import SingletonInstance

class FileManager(SingletonInstance):
    MAX_DIRECTORY_COUNT_FOR_MONTHLY: int = 3
    
    @staticmethod
    def setFileOwnWithMod(fileDir:str) :
        daemonUid = 2 
        os.chown(fileDir , daemonUid, daemonUid)
        os.chmod(path=fileDir, mode=0o755)
        
    @staticmethod
    def makeDirs(directory :str) :
        if not os.path.exists(directory):
            os.makedirs(directory)
            FileManager.setFileOwnWithMod(directory)
    
        
    # @staticmethod
    # def isFullInDirectory(dir:str):
    #     return len(os.listdir(dir)) >= FileManager.__MAX_DIRECTORY_FULL_LENGTH
    

    def getLastGenerateDir(dir:str):
        return os.listdir(dir)


    @staticmethod
    def removeFile(filePath:str):
        return os.remove(filePath)
    

    @staticmethod
    def randomResourceSubDirectory():
        return datetime.datetime.now().strftime("%Y%m") + "_" + str(random.randrange(1,FileManager.MAX_DIRECTORY_COUNT_FOR_MONTHLY))