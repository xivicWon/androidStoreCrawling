# -*- coding: utf-8 -*-
import os
import sys, rootpath
sys.path.append(rootpath.detect())
from module.ImageConverter import ImageConverter        
        
def validateInput(value) : 
    return type(value) == str or value != ""
      
# "./images"
print("Enter a directory what you want to convert images :")
dir_path = input()

if type(dir_path) != str or not os.path.isdir(dir_path) :
    print("It's Wrong answer it's not a directory")
    exit()

print("\n")
print("Scanning directories.")
fileLength:int = 0
for (root, directories, files) in os.walk(dir_path):
    fileLength+= len(files)
    
    
print("\n")
print("I found {} files in {} directories, If you want to continue, Please enter 'Y' ".format(dir_path, fileLength))
confirm = input()
if( type(confirm) != str or confirm != "Y"):
    print("User cancel process.")
    exit()

convertFileCount:int = 0
for (root, directories, files) in os.walk(dir_path):
    for file in files:
        file_path = os.path.join(root, file)
        ImageConverter.convert(file_path)
        convertFileCount+=1

print("Finished >> Total {} files Converted.".format(convertFileCount))