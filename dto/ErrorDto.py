from enum import Enum
from dto.Dto import Dto

class StrEnum (Enum):
    def __repr__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.name
    
class ErrorCodeValueLevel(Enum) :
    TRACE = 0 
    DEBUG = 1
    INFO = 2
    WARN = 3 
    ERROR = 4    

class ErrorCodeValue: 
    __codeNumber: int 
    __level : ErrorCodeValueLevel
    
    def __init__(self, codeNumber:int, level:ErrorCodeValueLevel):
        self.__codeNumber = codeNumber
        self.__level = level
    
    def getLevel(self, ):
        return self.__level.name
    
    def getNumber(self, ):
        return self.__codeNumber
    
class ErrorCodeNotWorked(StrEnum):
    EXCEPTION = ErrorCodeValue(1000, ErrorCodeValueLevel.ERROR)
    ATTRIBUTE_ERROR = ErrorCodeValue(2001, ErrorCodeValueLevel.ERROR)
    TYPE_ERROR = ErrorCodeValue(2002, ErrorCodeValueLevel.ERROR) 
    TOO_MANY_REQUEST = ErrorCodeValue(4000, ErrorCodeValueLevel.WARN)
    RESPONSE_FAIL = ErrorCodeValue(4001, ErrorCodeValueLevel.WARN) 
    REQUEST_READ_TIMEOUT = ErrorCodeValue(4002, ErrorCodeValueLevel.WARN)
    REQUEST_CONNECTION_ERROR = ErrorCodeValue(4003, ErrorCodeValueLevel.WARN) 
    CHUNKED_ENCODING_ERROR = ErrorCodeValue(4004, ErrorCodeValueLevel.WARN)  
    URL_OPEN_ERROR = ErrorCodeValue(4005, ErrorCodeValueLevel.WARN)   

class ErrorCode(Enum):
    EXCEPTION = 1000
    ATTRIBUTE_ERROR = 2001
    TYPE_ERROR = 2002
    TOO_MANY_REQUEST = 4000
    RESPONSE_FAIL = 4001
    REQUEST_READ_TIMEOUT = 4002
    REQUEST_CONNECTION_ERROR = 4003
    CHUNKED_ENCODING_ERROR = 4004
    URL_OPEN_ERROR = 4005


class ErrorDto(Dto) : 
    __code : ErrorCode
    __message : str

    @staticmethod
    def build( code:ErrorCode, message:str):
        errorDto = ErrorDto()
        errorDto.__code = code
        errorDto.__message = message
        return errorDto

    @property
    def getCode(self):
        return self.__code
    
    def toLog(self,):
        return "{} > {}".format( self.__code.name, self.__message)