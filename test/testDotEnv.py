import os, sys, rootpath 
sys.path.append(rootpath.detect())
import os
from module.EnvStore import EnvStore


Env = EnvStore()
appStore = Env.getAppStore
print(appStore)

