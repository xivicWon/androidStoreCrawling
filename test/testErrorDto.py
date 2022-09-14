from multiprocessing import Queue
from re import T
import rootpath
import sys
sys.path.append(rootpath.detect())

from module.EnvManager import EnvManager
from module.LogManager import LogManager
from dto.ErrorDto import ErrorCode, ErrorCodeValue, ErrorCodeValueLevel, ErrorDto


if __name__  == '__main__' :
    q = Queue()
    envManager = EnvManager.instance()
    logManager = LogManager.instance()
    logManager.init(envManager)
    url = 'www.naver.com'
    errorCode = ErrorCodeValue(1000, ErrorCodeValueLevel.ERROR)
    dto = ErrorDto.build(ErrorCode.TOO_MANY_REQUEST , url)
    print("GetCode : {}".format(dto.getCode))
    q.put(errorCode)
    q.put(dto)
    q.put(dto)
    q.put("EOQ")
    while True:
        v = q.get()
        if v == "EOQ":
            break
