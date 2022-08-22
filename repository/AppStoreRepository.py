from typing import List, Optional
from repository.Repository import Repository
from entity.AppMarketScrap import AppMarketScrap
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from entity.AppResourceEntity import AppResourceEntity
from entity.AppEntity import AppEntity
from module.OpenDB_v3 import OpenDB

class AppStoreRepository(Repository) :
    
    def __init__(self, dbManager:OpenDB) -> None:
        self.dbManager = dbManager
    
    def findAppById(self, market_num:int, id:str )->Optional[AppEntity]:
        query = """
            SELECT  *
            FROM    app
            WHERE   market_num = %s
                AND id = %s
        """
        field = (market_num, id)
        result = self.dbManager.select(query ,field)
        return AppEntity().ofDict(result[0]) if type(result) == list else None
        
    
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
        
        
    def findDeveloperByDeveloperMarketId(self, appMarketDeveloperEntity : AppMarketDeveloperEntity) ->Optional[AppMarketDeveloperEntity]:
        query = """
            SELECT  *
            FROM    app_market_developer
            WHERE   market_num = %s 
                AND developer_market_id = %s
        """
        result = self.dbManager.select(query, (appMarketDeveloperEntity.getMarketNum , 
                                               appMarketDeveloperEntity.getDeveloperMarketId))
        return AppMarketDeveloperEntity().ofDict(result[0]) if type(result) == list  else None
    
    def saveDeveloper(self, appMarketDeveloperEntity : AppMarketDeveloperEntity) -> int:
        try : 
            query = """
                INSERT INTO app_market_developer ( market_num , company_num, developer_name, developer_market_id ) 
                VALUES ( %s , %s , %s,  %s) 
                ON DUPLICATE KEY UPDATE 
                    developer_name = values(developer_name)
                    
            """
        except Exception as e : 
            # 쿼리 자체 에러.
            raise Exception("Error in generate Query ", e)
        return self.dbManager.insert(query, (appMarketDeveloperEntity.getMarketNum, 
                                             appMarketDeveloperEntity.getCompanyNum, 
                                             appMarketDeveloperEntity.getDeveloperName,
                                             appMarketDeveloperEntity.getDeveloperMarketId ))
    
    def saveResource (self, appResourceEntity : AppResourceEntity): 
        try : 
            query = """
                INSERT IGNORE INTO apps_resource ( app_num, resource_type, path ) 
                VALUES ( %s, %s, %s) 
            """
        except Exception as e : 
            # 쿼리 자체 에러.
            raise Exception("Error in generate Query ", e)
        return self.dbManager.insert(query, (appResourceEntity.getAppNum, 
                                             appResourceEntity.getResourceType, 
                                             appResourceEntity.getPath ))
        
         
    def addApp ( self, appEntity : AppEntity) -> Optional[int] : 
        query = """
            INSERT INTO app
            SET     id = %s,
                    market_num = %s,
                    app_name = %s,
                    is_active = %s,
                    last_update = %s,
                    developer_num = %s,
                    rating = %s
            ON DUPLICATE KEY UPDATE 
                app_name = VALUES(app_name),
                is_active = VALUES(is_active),
                last_update = VALUES(last_update),
                rating = VALUES(rating),
                developer_num = VALUES(developer_num)
        """
        try : 
            return self.dbManager.insert(query, (appEntity.getId, 
                                          appEntity.getMarketNum,
                                          appEntity.getAppName ,
                                          appEntity.getIsActive, 
                                          appEntity.getLastUpdate , 
                                          appEntity.getDeveloperNum , 
                                          appEntity.getRating ))
        except Exception as e : 
            print("[ERROR : {}".format(appEntity.toString()))
            print(e)
            return None

        
        
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
            self.dbManager.update(query, (appEntity.getAppName , 
                                          appEntity.getIsActive, 
                                          appEntity.getLastUpdate ,
                                          appEntity.getDeveloperNum , 
                                          appEntity.getId, 
                                          appEntity.getMarketNum))
        except Exception as e : 
            print("[ERROR : {}".format(appEntity.toString()))
            print(e)
    
        
    def deleteApp( self, appEntity : AppEntity): 
        query = """
            DELETE  *
            FROM    app
            WHERE   id = %s
                AND market_num = %s
        """
        try : 
            self.dbManager.update(query, ( appEntity.getId, appEntity.getMarketNum))
        except Exception as e : 
            print("[ERROR : {}".format(appEntity.toString()))
            print(e)


    def findMarketScrapUrl(self , market_num ) -> Optional[List[AppMarketScrap]]:  
        query = """
            SELECT  *
            FROM    app_market_scrap
            WHERE   market_num = %s
        """
        field = (market_num)
        result = self.dbManager.select(query ,field)
        return list(map( lambda t : AppMarketScrap().ofDict(t) , result )) if type(result) == list else None
    
    

    def saveResourceUseBulk(self, bulkResources: List[AppResourceEntity]):
        query = """
            INSERT INTO apps_resource ( app_num, resource_type, path ) 
            VALUES (%s, %s, %s)
        """
        fields = []
        for appResourceEntity in bulkResources :
            fields.append((appResourceEntity.getAppNum, appResourceEntity.getResourceType, appResourceEntity.getPath))
            
        return self.dbManager.insertBulk(query, fields)
        
        

    def saveAppTmpUseBulk(self, bulkResources: List[AppEntity]):
        query = """
            INSERT INTO app_tmp ( id, market_num, app_name, is_active, last_update, developer_num, rating) 
            VALUES (%s, %s, %s,%s, %s, %s, %s)
        """
        fields = []
        for appEntity in bulkResources :
            fields.append(( appEntity.getId,
                            appEntity.getMarketNum,
                            appEntity.getAppName ,
                            appEntity.getIsActive,
                            appEntity.getLastUpdate,
                            appEntity.getDeveloperNum,
                            appEntity.getRating))
            
        return self.dbManager.insertBulk(query, fields)
        