# -*- coding: utf-8 -*-
import logging, rootpath, os
from multiprocessing import current_process
from typing import Callable
from module.LogModule import LogModule
from module.SingletonInstance import SingletonInstance
from module.EnvManager import EnvManager
class LogManager(SingletonInstance, LogModule):
    __statusLogFileHandler : bool = False
    __statusErrorFileHandler : bool = False
    __env : EnvManager
    
    def __new__(cls) :
        return super().__new__(cls)
    
    def __init__(self) -> None:
        super().__init__()
    
    def init(self, env):
        self.__env = env
    
    def setFileHandler(self, path:str , name:str, formatter:logging.Formatter, level:str ):
        directory = "/".join( [rootpath.detect().replace("\\" ,"/") , path ])
        if not os.path.exists(directory):
            os.makedirs(directory)
        filePath = directory + "/" + name
        file_handler = logging.FileHandler(filename=filePath, encoding="utf8")
        file_handler.set_name(name)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        logger = logging.getLogger()
        logger.addHandler(file_handler)
    
    def initHandler(self,) : 
        self.__statusLogFileHandler = self.__env.LOG_STATUS
        self.__statusErrorFileHandler = self.__env.LOG_ERROR_STATUS
        
        logger = logging.getLogger()
        logger.setLevel(self.__env.LOG_LEVEL)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        
        streamHandlerFilterCondition : Callable[[logging.Handler] , bool] = lambda h : isinstance( h, logging.StreamHandler ) 
        fileHandlerFilterCondition : Callable[[logging.Handler] , bool] = lambda h : isinstance( h, logging.FileHandler )
        
        if self.__statusLogFileHandler and not self.hasStreamHandler(streamHandlerFilterCondition , self.__env.LOG_NAME) :
            stream_handler = logging.StreamHandler()
            stream_handler.set_name(self.__env.LOG_NAME)
            stream_handler.setFormatter(formatter)
            stream_handler.setLevel(self.__env.LOG_LEVEL)
            logger.addHandler(stream_handler)

        if self.__statusLogFileHandler and not self.hasFileHandler(fileHandlerFilterCondition, self.__env.LOG_NAME):
            self.setFileHandler(
                path=self.__env.LOG_PATH , 
                name=self.__env.LOG_NAME, 
                formatter=formatter,
                level= self.__env.LOG_LEVEL)
            
        if self.__statusErrorFileHandler and not self.hasFileHandler(fileHandlerFilterCondition, self.__env.LOG_ERROR_NAME):
            self.setFileHandler(
                path=self.__env.LOG_ERROR_PATH, 
                name=self.__env.LOG_ERROR_NAME, 
                formatter=formatter,
                level= self.__env.LOG_ERROR_LEVEL)

    def hasStreamHandler(self, condition, name:str):
        condition : Callable[[logging.Handler] , bool] = lambda h : isinstance( h, logging.StreamHandler ) and h.get_name() == name 
        result = next(filter(condition, logging.getLogger().handlers ), False)
        return isinstance( result , logging.Handler) 

    def hasFileHandler(self, condition, name:str):
        condition : Callable[[logging.Handler] , bool] = lambda h : isinstance( h, logging.FileHandler ) and h.get_name() == name 
        result = next(filter(condition, logging.getLogger().handlers ), False)
        return isinstance( result , logging.Handler) 
                
    def wrappingMessage(self,message):
        return message
    
    def debug(self, msg) : 
        self.initHandler()
        logging.getLogger().debug(self.wrappingMessage(msg))
        
    def info(self, msg) : 
        self.initHandler()
        logging.getLogger().info(self.wrappingMessage(msg))
    
    def warning(self, msg) :
        self.initHandler() 
        logging.getLogger().warning(self.wrappingMessage(msg))
        
    def error(self, msg) : 
        self.initHandler()
        logging.getLogger().error(self.wrappingMessage(msg))
        
    def critical(self, msg) : 
        self.initHandler()
        logging.getLogger().critical(self.wrappingMessage(msg))
    
    
    @staticmethod
    def listloggers():
        rootlogger = logging.getLogger()
        print("{} ({})".format(rootlogger, id(rootlogger)))
        for h in rootlogger.handlers:
            print('     {} - {}'.format(current_process().name, h))

        # for nm, lgr in logging.Logger.manager.loggerDict.items():
        #     print('+ [%-20s] %s ' % (nm, lgr))
        #     if not isinstance(lgr, logging.PlaceHolder):
        #         for h in lgr.handlers:
        #             print('     %s' % h)
 
    @staticmethod
    def disabledAllHandler() : 
        LogManager.listloggers()
        logger = logging.getLogger()
        for handler in logger.handlers:
            handler.close()
            logger.removeHandler(handler)
    