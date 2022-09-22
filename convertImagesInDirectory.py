# -*- coding: utf-8 -*-
import os
import sys, rootpath
sys.path.append(rootpath.detect())
from module.ImageConverter import ImageConverter        
        
def validateInput(value) : 
    return type(value) == str or value != ""
      
# "./images"
try : 
    dir_path = sys.argv[1]
    if dir_path == None : 
        raise IndexError
except IndexError: 
    print("입력 파라미터를 체크해 주세요. {}".format(sys.argv))
    exit()
    
if type(dir_path) != str or not os.path.isdir(dir_path) :
    print("It's Wrong answer it's not a directory")
    exit()

print("\n")
print("Scanning directories.")
fileLength:int = 0
for (root, directories, files) in os.walk(dir_path):
    fileLength+= len(files)
    
convertFileCount:int = 0
for (root, directories, files) in os.walk(dir_path):
    for file in files:
        file_path = os.path.join(root, file)
        ImageConverter.convert(file_path)
        convertFileCount+=1

print("Finished >> Total {} files Converted.".format(convertFileCount))