import json
class Dto:
    
    def __init__(self) -> None:
        pass
    
    def toString(self):
        return json.dumps(vars(self))
    