from time import sleep
import rootpath
import sys
sys.path.append(rootpath.detect())

from TimeChecker import ProcessTimer



p = ProcessTimer()
p.start("aa")
sleep(2)
p.stop("aa")
p.display("aa")