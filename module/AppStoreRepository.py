import datetime
from typing import List, Optional
from module.Repository import Repository
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from module.OpenDB_v3 import OpenDB
from entity.AppEntity import AppEntity

class AppStoreRepository(Repository) :
    
    def __init__(self, dbManager:OpenDB) -> None:
        self.dbManager = dbManager
        
    def findNoNameAppLimitedTo(self , market_num,  offset :int , limit :int ) -> Optional[List[AppEntity]]:  
        query = """
            SELECT  *
            FROM    app
            WHERE   app_name IS NULL
                AND market_num = %s
            LIMIT   %s , %s
        """
        field = (market_num, offset , limit)
        result = self.dbManager.select(query ,field)
        return list(map( lambda t : AppEntity().ofDict(t) , result )) if type(result) == list else None
        
    def findAppLimitedTo(self , market_num,  offset :int , limit :int ) -> Optional[List[AppEntity]]:  
        query = """
            SELECT  *
            FROM    app
            WHERE   market_num = %s
            LIMIT   %s , %s
        """
        field = (market_num, offset , limit)
        result = self.dbManager.select(query ,field)
        return list(map( lambda t : AppEntity().ofDict(t) , result )) if type(result) == list else None
        
    def findDeveloperByDeveloperNum(self, appMarketDeveloperEntity : AppMarketDeveloperEntity) ->Optional[AppMarketDeveloperEntity]:
        query = """
            SELECT  *
            FROM    app_market_developer
            WHERE   market_num = %s 
                AND developer_market_id = %s
        """
        result = self.dbManager.select(query, (appMarketDeveloperEntity.market_num , appMarketDeveloperEntity.developer_market_id))
        return AppMarketDeveloperEntity().ofDict(result[0]) if type(result) == list  else None
    
    def saveDeveloper(self, appMarketDeveloperEntity : AppMarketDeveloperEntity) -> int:
        try : 
            query = """
                INSERT IGNORE INTO app_market_developer ( market_num , company_num, developer_name, developer_market_id ) 
                VALUES ( %s , %s , %s,  %s) 
            """
        except Exception as e : 
            raise Exception("Error in generate Query ", e)
        return self.dbManager.insert(query, (appMarketDeveloperEntity.market_num , appMarketDeveloperEntity.company_num, appMarketDeveloperEntity.developer_name, appMarketDeveloperEntity.developer_market_id ))
    
    
    def updateApp( self, appEntity : AppEntity): 
        query = """
            UPDATE  app
            SET     app_name = %s,
                    is_active = %s,
                    last_update = %s,
                    developer_num = %s
            WHERE   id = %s
                AND market_num = %s
        """
        try : 
            self.dbManager.update(query, (appEntity.app_name , appEntity.is_active, appEntity.last_update , appEntity.developer_num , appEntity.id, appEntity.market_num))
        except Exception as e : 
            print("[ERROR : {}".format(appEntity.toString()))
            print(e)
