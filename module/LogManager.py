# -*- coding: utf-8 -*-
import logging
import rootpath
from typing import Callable, Final
from module.EnvManager import EnvManager
class LogManager():
    __logger : Final[logging.Logger]
    __isSetHandler : bool = False
    __useFileHandler : bool = True
    __useStreamHandler : bool = True
    
    @classmethod
    def initHandler(cls,) : 
        if not cls.__isSetHandler : 
            envManager = EnvManager()
            
            cls.__logger = logging.getLogger()
            cls.__logger.setLevel(envManager.LOG_LEVEL)
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            streamHandlerFilterCondition : Callable[[logging.Handler] , bool] = lambda h : type(h) == logging.StreamHandler
            
            if cls.__useStreamHandler and next(filter(streamHandlerFilterCondition, cls.__logger.handlers[:] ) , False):
                stream_handler = logging.StreamHandler()
                stream_handler.setFormatter(formatter)
                cls.__logger.addHandler(stream_handler)

            fileHandlerFilterCondition : Callable[[logging.Handler] , bool] = lambda h : type(h) == logging.FileHandler
            if cls.__useFileHandler and next(filter(fileHandlerFilterCondition, cls.__logger.handlers[:]  ) , False) :
                filePath = "\\".join( [rootpath.detect() , envManager.LOG_PATH , envManager.LOG_FILENAME ] )
                file_handler = logging.FileHandler(filename=filePath, encoding="utf8")
                file_handler.setFormatter(formatter)
                cls.__logger.addHandler(file_handler)
            cls.__isSetHandler = True
    
    @classmethod
    def wrappingMessage(cls,message):
        return message
    
    @classmethod
    def debug(cls, msg) : 
        cls.initHandler()
        cls.__logger.debug(cls.wrappingMessage(msg))
        
    @classmethod
    def info(cls, msg) : 
        cls.initHandler()
        cls.__logger.info(cls.wrappingMessage(msg))
    
    @classmethod
    def warning(cls, msg) :
        cls.initHandler() 
        cls.__logger.warning(cls.wrappingMessage(msg))
        
    @classmethod
    def error(cls, msg) : 
        cls.initHandler()
        cls.__logger.error(cls.wrappingMessage(msg))
        
    @classmethod
    def critical(cls, msg) : 
        cls.initHandler()
        cls.__logger.critical(cls.wrappingMessage(msg))
    
    