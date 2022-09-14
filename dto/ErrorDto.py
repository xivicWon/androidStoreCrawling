from enum import Enum
from dto.Dto import Dto
class ErrorCodeLevel(Enum) :
    TRACE = 0 
    DEBUG = 1
    INFO = 2
    WARN = 3 
    ERROR = 4    

class ErrorCodeValue: 
    __codeNumber: int 
    __level : ErrorCodeLevel
    
    def __init__(self, codeNumber, level:ErrorCodeLevel) -> None:
        self.__codeNumber = codeNumber
        self.__level = level
        pass
    
    def getLevel(self, ):
        return self.__level.name
    
    def getNumber(self, ):
        return self.__codeNumber
    
class ErrorCode(Enum):
    EXCEPTION = ErrorCodeValue(1000, ErrorCodeLevel.ERROR)
    ATTRIBUTE_ERROR = ErrorCodeValue(2001, ErrorCodeLevel.ERROR)
    TYPE_ERROR = ErrorCodeValue(2002, ErrorCodeLevel.ERROR) 
    TOO_MANY_REQUEST = ErrorCodeValue(4000, ErrorCodeLevel.WARN)
    RESPONSE_FAIL = ErrorCodeValue(4001, ErrorCodeLevel.WARN) 
    REQUEST_READ_TIMEOUT = ErrorCodeValue(4002, ErrorCodeLevel.WARN)
    REQUEST_CONNECTION_ERROR = ErrorCodeValue(4003, ErrorCodeLevel.WARN) 
    CHUNKED_ENCODING_ERROR = ErrorCodeValue(4004, ErrorCodeLevel.WARN)  
    URL_OPEN_ERROR = ErrorCodeValue(4005, ErrorCodeLevel.WARN)   
    
class ErrorDto(Dto) : 
    code : ErrorCode
    message : str

    @staticmethod
    def build( code:int, message:str):
        errorDto = ErrorDto()
        errorDto.code = code
        errorDto.message = message
        return errorDto

    def getLevel(self):    
        return self.code.value.getLevel()
        
    def toLog(self,):
        return "{} > {}".format( self.code.name, self.message)