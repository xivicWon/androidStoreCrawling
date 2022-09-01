
class Tag_A :
    href : str 
    
    @property
    def getHref(self ):
        return self.href
    
    @classmethod
    def of(cls, obj:dict ): 
        tag = cls()
        tag.href = obj["href"]
        return tag