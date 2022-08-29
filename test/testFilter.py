from time import sleep
import rootpath
import sys
sys.path.append(rootpath.detect())
from typing import Callable, List
from entity.Entity import Entity
from entity.AppEntity import AppEntity

    
findAllAppEntities:List[AppEntity]  = []

findAllAppEntities.append(AppEntity().setId("id464205249"))
findAllAppEntities.append(AppEntity().setId("id987782077"))

dtos:List[AppEntity] = []

dtos.append(AppEntity().setId("id987782077"))
dtos.append(AppEntity().setId("id464205249"))

for dto in dtos :
    print("dto : {}  type : {} ".format(dto.getId , type(dto.getId)))
    
for findAppEntity in findAllAppEntities :
    print("findApp : {} type : {} ".format(findAppEntity.getId, type(findAppEntity.getId) ))
        
#3. resource 등록 ( Bulk Insert 가능. )
for dto in dtos :
    filterAppEntity:Callable[[AppEntity] , bool] = lambda t : t.getId == dto.getId
    findOneAppEntity:AppEntity = next(filter(filterAppEntity, findAllAppEntities), None)
    if findOneAppEntity == None :
        print("Error [Not Found AppEntity] : {}".format(dto.toString()))
        continue
    else :
        print("Success [Found AppEntity] : {}".format(findOneAppEntity.toString()))
        