import uuid

id = []
for i in range(100000):
    id.append( uuid.uuid4())
    
print (len(id))
print (len(list(set(id))))