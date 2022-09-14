import rootpath
import sys
sys.path.append(rootpath.detect())

from module.EnvManager import EnvManager
from module.LogManager import LogManager
from dto.ErrorDto import ErrorCode, ErrorDto


envManager = EnvManager.instance()
logManager = LogManager.instance()
logManager.init(envManager)
url = 'www.naver.com'
value = ErrorDto.build(ErrorCode.TOO_MANY_REQUEST , url)

print(value)
if isinstance( value, ErrorDto):
    print(value.getLevel())
    logManager.error(value)