from functools import reduce
import json

class Entity :
    
    
    def __str__(self):
        return json.dumps(vars(self))
    
    def toString(self):
        return json.dumps(vars(self))
    
    def getInsertClause(self):
        localVariable = vars(self)
        return "({})".format(
            ",".join(
                reduce(lambda acc, key : acc+["{}".format(key ) ] ,localVariable.keys(), [])
                )
            )
        
    def getInsertValueClause(self ):
        localVariable = vars(self)
        return "({})".format(
            ",".join(
                reduce(lambda acc, key : acc+["'{}'".format(localVariable[key] ) ] ,localVariable.keys(), [])
                )
            )
    