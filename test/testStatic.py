import sys, rootpath
sys.path.append(rootpath.detect())
from annotations.static_vars import static_vars


class A():
    
    counter :int
    d : dict 
    def getCounter(self):
        return self.d
    
    def __new__(cls) :
        print("__NEW__")
        print(cls.d)
        return super().__new__(cls)
    
    def __init__(self) -> None:
        print("__INIT__")
        pass
    
    @classmethod
    def instance(cls):
        if not hasattr(cls, "d") :
            cls.d = {} 
        return cls.d
    
        

d1 = A.instance()
d2 = A.instance()


print(d1)
print(d2)
print(id(d1))
print(id(d2))
