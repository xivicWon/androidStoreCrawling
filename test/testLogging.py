import sys, rootpath

sys.path.append(rootpath.detect())

from module.LogManager import LogManager


log = LogManager.instance()

log.info("info message")