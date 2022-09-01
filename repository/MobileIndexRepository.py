
from typing import List
from LogManager import LogManager
from dto.mobileIndex.MobileIndexDto import MobileIndexDto
from module.OpenDB_v3 import OpenDB


class MobileIndexRepository :
    maxInsertClauseCount: int = 1000 
    dbManager : OpenDB
    def __init__(self, dbManager:OpenDB, logModule:LogManager) -> None:
        self.dbManager = dbManager
    
    def _createSaveClause(self, insertClause, insertValueClause ):
        tableName = "app_tmp"
        query = "INSERT IGNORE INTO " + tableName  + " "+ insertClause + " VALUES "
        query += ",".join(insertValueClause)
        return query
        
    def save(self, dataList: List[MobileIndexDto]):
        insertValueClause = []
        for idx, data in enumerate(dataList) :
            if idx == 0 :
                insertClause = data.toAppEntity().getInsertClause()
        
            insertValueClause.append( data.toAppEntity().getInsertValueClause())
            
            if len(insertValueClause) >= self.maxInsertClauseCount :
                query = self._createSaveClause(insertClause, insertValueClause)
                insertValueClause = []
                # print(query)
                self.dbManager.insert(query)
                
        if len(insertValueClause) > 0 :
            query = self._createSaveClause(insertClause, insertValueClause)
            # print(query)
            self.dbManager.insert(query)