#!/usr/bin/env python
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from oai import app as application
from ConfigParser import ConfigParser
from flask import globals as g


#config = ConfigParser()
#path = os.path.abspath(os.path.dirname(__file__)) + os.sep + "lod.ini"
#config.read(path)
#g.modules = config._sections

from oai import index

def main():
    application.debug = False
    application.run()

if __name__ == "__main__":
    #for item in g.modules:
    #    modules = __import__("lod." + g.modules[item]["__name__"])
    #pass
    pass
