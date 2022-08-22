import rootpath
import sys, os


print ( os.path.dirname(__file__))
print ( os.path.abspath(os.path.dirname(__file__)))
print ( os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
print(rootpath.detect())
sys.path.append(os.path.dirname(rootpath.ROOT_PATH ))
from TimeChecker import ProcessTimer



p = ProcessTimer()
p.start("aa")
p.stop("aa")
p.display("aa")