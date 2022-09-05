from enum import Enum
from dto.Dto import Dto
class ErrorCode(Enum):
    ATTRIBUTE_ERROR = 2001
    TYPE_ERROR = 2002
    TOO_MANY_REQUEST = 4000
    RESPONSE_FAIL = 4001
    REQUEST_READ_TIMEOUT = 4002
    REQUEST_CONNECTION_ERROR = 4003
    CHUNKED_ENCODING_ERROR = 4004
    URL_OPRN_ERROR = 4005
class ErrorDto(Dto) : 
    code : ErrorCode
    message : str

    @staticmethod
    def build( code:int, message:str):
        dto = ErrorDto()
        dto.code = code
        dto.message = message
        return dto

    def toLog(self,):
        return "{} > {}".format( self.code.name, self.message)