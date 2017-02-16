#!/usr/bin/env python

import os
import sys
import time
import urllib
import pymongo
import hashlib
import datetime
import lxml_lib


class mongoDB_client():
    dbHandler = False
    def __init__(self, serverName="192.87.165.3", port=27017):
        try:
            self.dbHandler = pymongo.Connection(serverName, port)
        except:
            sys.stdout.write("Could not open " + serverName + " on port " + str(port) + "\n")
            os._exit(-1)

if __name__ == "__main__":
    handler = mongoDB_client()



    for item in handler.dbHandler["OAI"].collection_names():
        if not item == "system.indexes":
            #handler.dbHandler["OAI"][item].ensure_index("status")
            #handler.dbHandler["OAI"].command({"reIndex" : item})

            print("Collection : %s" %(item))
            new=handler.dbHandler["OAI"][item].find({"status" : "new"}).count()
            print("todo       : %10i" %(new))
            finished=handler.dbHandler["OAI"][item].find({"status" : "done"}).count()
            print("finished   : %10i" %(finished))
            indexed=handler.dbHandler["OAI"][item].find({"status" : "indexed"}).count()
            print("indexed : %10i" %(indexed))
