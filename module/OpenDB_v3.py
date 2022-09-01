# -*- coding: utf-8 -*-
import logging
import sys, rootpath

sys.path.append(rootpath.detect())
from functools import reduce
from typing import Final, List
from module.LogManager import LogManager
import pymysql
class OpenDB : 
    
    conn : pymysql.connect
    def __init__(self, host:str, username:str,password:str, database:str) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.database = database
 
    def _connect(self) :
        try : 
            conn =  pymysql.connect(
                host=self.host, 
                user=self.username, 
                passwd=self.password, 
                db=self.database, 
                port=3306, 
                use_unicode=True,
                cursorclass=pymysql.cursors.DictCursor,
                charset="utf8mb4",
                init_command= "SET NAMES utf8mb4"
            )
        except pymysql.err.OperationalError as e : 
            print("계정설정을 확인해주세요.")
            print(e)
            exit()
        return conn
    
    def checkVars(self):
        localValues = vars(self)
        return ",".join(reduce( lambda acc, key : acc+[localValues[key]] , localValues.keys() , []))
    
    
    def _query(self, query:str):
        conn = self._connect()
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
            
    
    def truncate(self , table) :
        self._query("TRUNCATE " + table) 
                 
    def selectOne(self, query:str, fields:tuple) -> list :
        conn = self._connect()
        with conn:
            with conn.cursor() as cur:
                try : 
                    cur.execute(query, fields)
                    return cur.fetchone()
                except pymysql.err.ProgrammingError as e :
                    LogManager.error("{} ProgrammingError : {}".format(self.select.__qualname__ , e))
                except pymysql.err.OperationalError as e : 
                    LogManager.error("{} OperationalError : {}".format(self.select.__qualname__ , e))
                except UnicodeDecodeError as e :
                    LogManager.error("{} UnicodeDecodeError : {}".format(self.select.__qualname__ , e))
                return None
            
    def select(self, query:str, fields:tuple) -> list :
        conn = self._connect()
        with conn:
            with conn.cursor() as cur:
                try : 
                    cur.execute(query, fields)
                    return cur.fetchall()
                except pymysql.err.ProgrammingError as e :
                    LogManager.error("{} ProgrammingError : {}".format(self.select.__qualname__ , e))
                except pymysql.err.OperationalError as e : 
                    LogManager.error("{} OperationalError : {}".format(self.select.__qualname__ , e))
                except UnicodeDecodeError as e :
                    LogManager.error("{} UnicodeDecodeError : {}".format(self.select.__qualname__ , e))
                return None

    def insert(self, query:str, fields:tuple) :
        conn = self._connect()
        with conn:
            with conn.cursor() as cur:
                try : 
                    cur.execute(query=query, args=fields)
                    return cur.lastrowid
                except Exception as e : 
                    LogManager.error("{} Exception : {}".format(self.select.__qualname__ , e))
        
    def update(self, query:str, fields:tuple) :
        conn = self._connect()
        with conn:
            with conn.cursor() as cur:
                try : 
                    cur.execute(query, fields)
                except Exception as e:
                    LogManager.error("{} Exception : {}".format(self.select.__qualname__ , e))
        
    def insertBulk(self, query:str, fields:List[tuple]) :
        conn = self._connect()
        with conn:
            with conn.cursor() as cur:
                try : 
                    cur.executemany(query, fields)
                except Exception as e : 
                    LogManager.error("{} Exception : {}".format(self.select.__qualname__ , e))
                     