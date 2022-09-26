# -*- coding: utf-8 -*-
from re import S
import sys, rootpath
sys.path.append(rootpath.detect())
from functools import reduce
from typing import  List
from module.LogModule import LogModule
import pymysql
class OpenDB : 
    __host:str
    __username:str
    __password:str
    __database:str
    __log:LogModule
    conn : pymysql.connect
    
    def __init__(self, host:str, username:str,password:str, database:str, logModule:LogModule ) -> None:
        self.__host = host
        self.__username = username
        self.__password = password
        self.__database = database
        self.__log = logModule

    def _connect(self) :
        try : 
            conn =  pymysql.connect(
                host=self.__host, 
                user=self.__username, 
                passwd=self.__password, 
                db=self.__database, 
                port=3306, 
                use_unicode=True,
                cursorclass=pymysql.cursors.DictCursor,
                charset="utf8mb4",
                autocommit=True
            )
            conn.set_charset("utf8mb4")
        except pymysql.err.OperationalError as e : 
            print("계정설정을 확인해주세요.")
            print(e)
            exit()
        return conn
    
    def checkVars(self):
        localValues = vars(self)
        return ",".join(reduce( lambda acc, key : acc+[localValues[key]] , localValues.keys() , []))
    
    
    def truncate(self , table) :
        conn = self._connect()
        with conn:
            with conn.cursor() as cur:
                cur.execute("TRUNCATE " + table)
                 
    def selectOne(self, query:str, fields:tuple) -> list :
        conn = self._connect()
        with conn:
            with conn.cursor() as cur:
                try : 
                    cur.execute(query=query, args=fields)
                    return cur.fetchone()
                except pymysql.err.ProgrammingError as e :
                    self.__log.error("{} ProgrammingError : {}".format(self.select.__qualname__ , e))
                    self.__log.error(query % fields)
                except pymysql.err.OperationalError as e : 
                    self.__log.error("{} OperationalError : {}".format(self.select.__qualname__ , e))
                except UnicodeDecodeError as e :
                    self.__log.error("{} UnicodeDecodeError : {}".format(self.select.__qualname__ , e))
                return None
            
    def select(self, query:str, fields:tuple) -> list :
        conn = self._connect()
        with conn:
            with conn.cursor() as cur:
                try : 
                    cur.execute(query=query, args=fields)
                    return cur.fetchall()
                except pymysql.err.ProgrammingError as e :
                    self.__log.error("{} ProgrammingError : {}".format(self.select.__qualname__ , e))
                    self.__log.error(query % fields)
                except pymysql.err.OperationalError as e : 
                    self.__log.error("{} OperationalError : {}".format(self.select.__qualname__ , e))
                except UnicodeDecodeError as e :
                    self.__log.error("{} UnicodeDecodeError : {}".format(self.select.__qualname__ , e))
                return None

    def insert(self, query:str, fields:tuple) :
        conn = self._connect()
        with conn:
            with conn.cursor() as cur:
                try : 
                    cur.execute(query=query, args=fields)
                    return cur.lastrowid
                except Exception as e : 
                    self.__log.error("{} Exception : {}".format(self.insert.__qualname__ , e))
        
        
    def insertBulk(self, query:str, fields:List[tuple]) :
        conn = self._connect()
        with conn:
            with conn.cursor() as cur:
                try :
                    cur.executemany(query, fields)
                except Exception as e : 
                    self.__log.error("{} Exception : {}".format(self.insertBulk.__qualname__ , e))
                     
    def update(self, query:str, fields:tuple) :
        conn = self._connect()
        with conn:
            with conn.cursor() as cur:
                try : 
                    cur.execute(query=query, args=fields)
                except Exception as e:
                    self.__log.error("{} Exception : {}".format(self.update.__qualname__ , e))
                 