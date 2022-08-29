# -*- coding: utf-8 -*-
from functools import reduce
from typing import List
import pymysql
class OpenDB : 
    
    conn : pymysql.connect
    
    def __init__(self, host:str, username:str,password:str, database:str) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.database = database
 
    def _connect(self) :
        conn =  pymysql.connect(
            host=self.host, 
            user=self.username, 
            passwd=self.password, 
            db=self.database, 
            port=3306, 
            use_unicode=True, 
            cursorclass=pymysql.cursors.DictCursor,
            charset="utf8")
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
        
        
    def select(self, query:str, fields:tuple) -> list :
        conn = self._connect()
        with conn:
            with conn.cursor() as cur:
                try : 
                    cur.execute(query, fields)
                    return cur.fetchall()
                except pymysql.err.ProgrammingError as e :
                    print("Error: {}".format(e))
                return None                    

    def insert(self, query:str, fields:tuple) :
        conn = self._connect()
        with conn:
            with conn.cursor() as cur:
                try : 
                    cur.execute(query=query, args=fields)
                    return cur.lastrowid
                except Exception as e : 
                    print(query , fields)
                    print(e)
        
    def update(self, query:str, fields:tuple) :
        conn = self._connect()
        with conn:
            with conn.cursor() as cur:
                try : 
                    cur.execute(query, fields)
                except Exception as e:
                    print("{} SQL 오류 ".format(query)) 
                    print(e)
        
    def insertBulk(self, query:str, fields:List[tuple]) :
        conn = self._connect()
        with conn:
            with conn.cursor() as cur:
                try : 
                    cur.executemany(query, fields)
                except Exception as e : 
                    print(query , fields)
                    print(e)
                     