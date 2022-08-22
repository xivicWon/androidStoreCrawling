from threading import Thread
from typing import List
from urllib import request


def getImage( url:str , size:int , imageName:str, imageExt: str ):
    fullImageUrl = url + "/" + str(size) + "x0w.webp"
    request.urlretrieve(fullImageUrl,  imageName + "." + imageExt )

appImageUrl = "https://is1-ssl.mzstatic.com/image/thumb/Purple122/v4/11/5f/65/115f65e0-0dc8-25a4-cd4a-3a141ab70f8b/AppIcon-0-0-1x_U007emarketing-0-0-0-5-0-0-sRGB-0-0-0-GLES2_U002c0-512MB-85-220-0-0.png"
downloadImageExt = "png"

sizeList = [32, 64, 128, 256, 512 ]

threadlist:List[Thread] = []
for size in sizeList:
    downloadImageName = "test" + str(size )
    threadlist.append(Thread(target=getImage , name="[{}th thread ]".format(len(threadlist)), args=(appImageUrl, size ,downloadImageName ,downloadImageExt,)))
    
for thread in threadlist :
    thread.start()
    
for thread in threadlist :
    thread.join()