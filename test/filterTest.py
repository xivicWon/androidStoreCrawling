from typing import Callable, List

ids:List[str] = []
dtos = [1,2,3,1,2,3,1,2,3,]
for idx, currentId in enumerate( dtos ):
    condition : Callable[[str], bool]  = lambda id : id == currentId 
    filtered = next(filter( condition, ids ), None)
    if filtered != None:
        print("{} >> {} 중복로 인한 패스!".format(idx, currentId))
        continue
    
    ids.append(currentId)