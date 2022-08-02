import pymysql

class OpenDB : 
    
    def __init__(self, host:str, username:str,password:str, database:str) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self._connect()
 
    def _connect(self) :
         self.conn = pymysql.connect(self.host, user=self.username, passwd=self.password, db=self.database, port=3306, use_unicode=True, charset='utf8')
        
        
        
    def insert(self, query:str) :
        if not self.conn.ping() :
            self._connect()
        try : 
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(query)
        finally:
            self.conn.close()
        
    def update(self, query:str) :
        if not self.conn.ping() :
            self._connect()
        try : 
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(query)
        finally:
            self.conn.close()
        
    def select(self, query) -> list :
        
        if not self.conn.ping() :
            self._connect()
        try :
            with self.conn:
                with self.conn.cursor(pymysql.cursors.DictCursor) as cur :
                    cur.execute(query)
                    return cur.fetchall()
        finally:
            self.conn.close()