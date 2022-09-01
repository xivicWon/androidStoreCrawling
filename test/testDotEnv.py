import os, sys, rootpath 
sys.path.append(rootpath.detect())
import os
from module.EnvManager import EnvManager


Env = EnvStore()
appStore = Env.getAppStore
print(appStore)

