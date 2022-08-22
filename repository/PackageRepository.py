from module.OpenDB import OpenDB

class PackageRepository:
    
    def __init__(self, dbManager:OpenDB) -> None:
        self.dbManager = dbManager
        
    def activePackages(self, packages:list) :
        
        queryStr = """
            insert into app_checked (app_num)
            select  num
            from    app
            where   id in ( '{}' ) 
            """.format("\',\'".join(packages))
        self.dbManager.insert(query=queryStr)
        
    def inactivePackages(self, packages:list) :
        queryStr = """
            update  app 
            set     is_active = 'N' 
            where   id in ( '{}' ) 
            """.format("\',\'".join(packages))
        self.dbManager.update(query=queryStr)
        
        queryStr = """
            insert into app_checked (app_num)
            select  num
            from    app
            where   id in ( '{}' ) 
            """.format("\',\'".join(packages))
        self.dbManager.insert(query=queryStr)
        
    def findAppIdbyOffset(self, offset , limit ) -> list :
        queryStr = """
            select  id 
            from    app AS A 
                LEFT JOIN app_checked AS C 
                    ON A.num = C.app_num
            where   id <> ''
                AND C.app_num is null 
            limit {}, {}
            """.format(offset, limit)
        record = self.dbManager.select(query=queryStr)
        return [item["id"] for item in record ]
        