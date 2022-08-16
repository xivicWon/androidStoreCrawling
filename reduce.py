from functools import reduce


class AppEntityTest:
    num : int
    id : int 
    market_num : int
    
    def __init__(self , obj):
        self.num = obj["num"]
        self.id = obj["id"]
        self.market_num = obj["market_num"]
    
    def getClause(self):
        localVariable = vars(self)
        return reduce(lambda acc, key : acc+["{}='{}'".format(key , localVariable[key] ) ] ,localVariable.keys(), [])
    
    
appEntity = AppEntityTest({"num" : 1, "id": 1,"market_num":22})
print(appEntity.getClause())
   