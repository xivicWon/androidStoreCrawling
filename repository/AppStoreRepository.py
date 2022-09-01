# -*- coding: utf-8 -*-
from logging import Logger
from typing import Final, List, Optional, Tuple

from repository.Repository import Repository
from entity.AppMarketScrap import AppMarketScrap
from entity.AppMarketDeveloperEntity import AppMarketDeveloperEntity
from entity.AppResourceEntity import AppResourceEntity
from entity.AppEntity import AppEntity
from module.OpenDB_v3 import OpenDB
from module.LogModule import LogModule
class AppStoreRepository(Repository) :
    
    __log : LogModule
    def __init__(self, dbManager:OpenDB, logModule:LogModule) -> None:
        self.dbManager = dbManager
        self.__log = logModule
        
    def findAppById(self, market_num:int, id:str )->Optional[AppEntity]:
        query = """
            SELECT  *
            FROM    app
            WHERE   market_num = %s
                AND id = %s
        """
        field = (market_num, id)
        result = self.dbManager.selectOne(query ,field)
        
        if type(result) == dict : 
            return AppEntity().ofDict(result)
        else :
            self.__log.warning("{} return is None".format(self.findAppById.__qualname__ ))
            return None
        
    
    def findNoNameAppLimitedToRecently(self , market_num,  offset :int , limit :int ) -> Optional[List[AppEntity]]:  
        query = """
            SELECT  *
            FROM    app
            WHERE   app_name IS NULL
                AND market_num = %s
            ORDER BY num DESC
            LIMIT   %s , %s
        """
        field = (market_num, offset , limit)
        result = self.dbManager.select(query ,field)
        if type(result) == list : 
            return list(map( lambda t : AppEntity().ofDict(t) , result )) 
        else :
            self.__log.warning("{} return is None".format(self.findNoNameAppLimitedToRecently.__qualname__ ))
            return None
        
    def findAppLimitedTo(self , market_num,  offset :int , limit :int ) -> Optional[List[AppEntity]]:  
        query = """
            SELECT  *
            FROM    app
            WHERE   market_num = %s
            LIMIT   %s , %s
        """
        field = (market_num, offset , limit)
        result = self.dbManager.select(query ,field)
        
        if type(result) == list : 
            return list(map( lambda t : AppEntity().ofDict(t) , result )) 
        else :
            self.__log.warning("{} return is None".format(self.findAppLimitedTo.__qualname__ ))
            return None
        
    def findDeveloperByDeveloperMarketId(self, appMarketDeveloperEntity : AppMarketDeveloperEntity) ->Optional[AppMarketDeveloperEntity]:
        query = """
            SELECT  *
            FROM    app_market_developer
            WHERE   market_num = %s 
                AND developer_market_id = %s
                AND developer_name = %s
        """
        result = self.dbManager.select(
            query, (
                appMarketDeveloperEntity.getMarketNum , 
                appMarketDeveloperEntity.getDeveloperMarketId,
                appMarketDeveloperEntity.getDeveloperName
            )
        )
        return AppMarketDeveloperEntity().ofDict(result[0]) if type(result) == list  else None
    
    def findAllDeveloperByDeveloperMarketId(self, appMarketDeveloperEntities : List[AppMarketDeveloperEntity]) -> Optional[List[AppMarketDeveloperEntity]]:
        query = """
            SELECT  *
            FROM    app_market_developer
            
        """
        
        result = self.dbManager.select(
            query, ()
        )
        return AppMarketDeveloperEntity().ofManyDict(result) if type(result) == list  else []
    
    def findAllDeveloperByDeveloperMarketId_(self, appMarketDeveloperEntities : List[AppMarketDeveloperEntity]) -> Optional[List[AppMarketDeveloperEntity]]:
        query = """
            SELECT  *
            FROM    app_market_developer
            WHERE   market_num in %s 
                AND developer_market_id in %s
        """
        marketNums:List[int] = []
        developerMarketId:List[str] = []
        
        for appMarketDeveloperEntity in appMarketDeveloperEntities : 
            marketNums.append(appMarketDeveloperEntity.getMarketNum)
            developerMarketId.append(appMarketDeveloperEntity.getDeveloperMarketId)
        
        marketNums = list(set(marketNums))
        result = self.dbManager.select(
            query, (
                marketNums, 
                developerMarketId
            )
        )
        return AppMarketDeveloperEntity().ofManyDict(result) if type(result) == list  else []
    
    
    
    def findAllApp(self, appEntities : List[AppEntity]) ->Optional[List[AppEntity]]:
        query = """
            SELECT  *
            FROM    app
            WHERE   market_num in %s 
                AND id in %s
        """
        Ids:List[str] = []
        marketNums:List[int] = []
        for appEntity in appEntities : 
            Ids.append(appEntity.getId)
            marketNums.append(appEntity.getMarketNum)
        Ids = list(set(Ids))
        marketNums = list(set(marketNums))
        
        result = self.dbManager.select(
            query, (
                marketNums,
                Ids
            )
        )
        return AppEntity().ofManyDict(result) if type(result) == list  else []
    
    def saveDeveloper(self, appMarketDeveloperEntity : AppMarketDeveloperEntity) -> int:

        query = """
            INSERT INTO app_market_developer ( market_num , company_num, developer_name, developer_market_id ) 
            VALUES ( %s , %s , %s,  %s) 
            ON DUPLICATE KEY UPDATE 
                developer_name = values(developer_name)
                
        """
        return self.dbManager.insert(query, (appMarketDeveloperEntity.getMarketNum, 
                                             appMarketDeveloperEntity.getCompanyNum, 
                                             appMarketDeveloperEntity.getDeveloperName,
                                             appMarketDeveloperEntity.getDeveloperMarketId ))
    
    
    def saveBulkDeveloper(self, appMarketDeveloperEntities : List[AppMarketDeveloperEntity]) -> int:
 
        query = """
            INSERT INTO app_market_developer ( market_num , company_num, developer_name, developer_market_id ) 
            VALUES ( %s , %s , %s,  %s) 
            ON DUPLICATE KEY UPDATE 
                developer_name = values(developer_name),
                developer_market_id = values(developer_market_id)
        """
    
        fields:List[Tuple] = []
        for appMarketDeveloperEntity in appMarketDeveloperEntities :
            fields.append((
                appMarketDeveloperEntity.getMarketNum, 
                appMarketDeveloperEntity.getCompanyNum, 
                appMarketDeveloperEntity.getDeveloperName,
                appMarketDeveloperEntity.getDeveloperMarketId ))
            
        return self.dbManager.insertBulk(query, fields)
    
    
    def saveResource (self, appResourceEntity : AppResourceEntity): 

        query = """
            INSERT IGNORE INTO apps_resource ( app_num, resource_type, path ) 
            VALUES ( %s, %s, %s) 
        """
        return self.dbManager.insert(query, (appResourceEntity.getAppNum, 
                                             appResourceEntity.getResourceType, 
                                             appResourceEntity.getPath ))
        
     
    def saveBulkApp(self, appEntities: List[AppEntity]):
        query = """
            INSERT INTO app ( id, market_num, app_name, is_active, last_update, developer_num, rating) 
            VALUES (%s, %s, %s,%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                app_name = VALUES(app_name),
                is_active = VALUES(is_active),
                last_update = VALUES(last_update),
                developer_num = VALUES(developer_num),
                rating = VALUES(rating)
        """
        fields = []
        for appEntity in appEntities :
            fields.append(( appEntity.getId,
                            appEntity.getMarketNum,
                            appEntity.getAppName ,
                            appEntity.getIsActive,
                            appEntity.getLastUpdate,
                            appEntity.getDeveloperNum,
                            appEntity.getRating))
            
        return self.dbManager.insertBulk(query, fields)
        
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
            return self.dbManager.insert(
                query, (
                    appEntity.getId, 
                    appEntity.getMarketNum,
                    appEntity.getAppName ,
                    appEntity.getIsActive, 
                    appEntity.getLastUpdate , 
                    appEntity.getDeveloperNum , 
                    appEntity.getRating
                )
            )
        except Exception as e : 
            self.__log.error("{} Exception : {}".format(self.addApp.__qualname__ , appEntity.toString()))
            self.__log.error("{}".format(self.addApp.__qualname__ , e))
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
            self.__log.error("{} Exception : {}".format(self.updateApp.__qualname__ , appEntity.toString()))
            self.__log.error("{}".format(self.updateApp.__qualname__ , e))
            print(e)
    
    def insertAppMappingCode( self, appEntity : AppEntity): 
        query = """
            INSERT INTO app
            SET     id = %s,
                    market_num = %s,
                    is_active = %s,
                    last_update = %s,
                    mapping_code = %s
            ON DUPLICATE KEY UPDATE 
                is_active = VALUES(is_active),
                last_update = VALUES(last_update),
                mapping_code = VALUES(mapping_code)
        """
        try : 
            self.dbManager.insert(
                query, (
                    appEntity.getId, 
                    appEntity.getMarketNum,
                    appEntity.getIsActive, 
                    appEntity.getLastUpdate, 
                    appEntity.getMappingCode
                )
            )
        except Exception as e : 
            self.__log.error("{} Exception : {}".format(self.insertAppMappingCode.__qualname__ , appEntity.toString()))
            self.__log.error("{}".format(self.insertAppMappingCode.__qualname__ , e))
    
        
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
            self.__log.error("{} Exception : {}".format(self.deleteApp.__qualname__ , appEntity.toString()))
            self.__log.error("{}".format(self.deleteApp.__qualname__ , e))


    def findMarketScrapUrl(self , market_num ) -> Optional[List[AppMarketScrap]]:  
        query = """
            SELECT  *
            FROM    app_market_scrap
            WHERE   market_num = %s
        """
        field = (market_num)
        result = self.dbManager.select(query ,field)
        return list(map( lambda t : AppMarketScrap().ofDict(t) , result )) if type(result) == list else None
    
    

    def findAppByUndefinedName(self, market_num ) -> Optional[List[AppEntity]]:  
        query = """
            SELECT  *
            FROM    app
            WHERE   market_num = %s
               AND  app_name is null
            limit 1000
        """
        field = (market_num)
        result = self.dbManager.select(query ,field)
        return list(map( lambda t : AppEntity().ofDict(t) , result )) if type(result) == list else None
    
    

    def saveResourceUseBulk(self, bulkResources: List[AppResourceEntity]):
        query = """
            INSERT INTO apps_resource ( app_num, resource_type, path ) 
            VALUES (%s, %s, %s)
        """
        fields = []
        for appResourceEntity in bulkResources :
            fields.append((appResourceEntity.getAppNum, appResourceEntity.getResourceType, appResourceEntity.getPath))
            
        return self.dbManager.insertBulk(query, fields)
        
        
    def saveAppMappingUseBulk(self, bulkResources: List[AppEntity]):
        query = """
            INSERT INTO app ( id, market_num, mapping_code, is_active, last_update) 
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE  
                mapping_code = VALUES(mapping_code),
                is_active = VALUES(is_active),
                last_update = VALUES(last_update)
        """
        fields = []
        for appEntity in bulkResources :
            fields.append(
                (
                    appEntity.getId,
                    appEntity.getMarketNum,
                    appEntity.getMappingCode,
                    appEntity.getIsActive,
                    appEntity.getLastUpdate
                )
            )
            
        return self.dbManager.insertBulk(query, fields)
        