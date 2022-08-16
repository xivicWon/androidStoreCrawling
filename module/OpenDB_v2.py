from functools import reduce
import pymysql
class OpenDB : 
    def __init__(self, host:str, username:str,password:str, database:str) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.database = database
 
    def _connect(self) :
        return pymysql.connect(
            host=self.host, 
            user=self.username, 
            passwd=self.password, 
            db=self.database, 
            port=3306, 
            use_unicode=True, 
            cursorclass=pymysql.cursors.DictCursor,
            charset='utf8')
    
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
        
    def insert(self, query:str) :
        conn = self._connect()
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.lastrowid
            
        
    def update(self, query:str) :
        conn = self._connect()
        with conn:
            with conn.cursor() as cur:
                try : 
                    cur.execute(query)
                except Exception as e:
                    raise print("{} SQL 오류 ".format(query)) 
        
    def select(self, query) -> list :
        conn = self._connect()
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()


    def escapeString(self, text: str) : 
        return self.conn