#!/usr/bin/env python

import os
import sys
import time
import urllib
from httplib import HTTPConnection
from httplib2 import Http
import pymongo
import hashlib
import datetime
import lxml_lib

from pprint import pprint


def post_url(data, colname):

    http = Http(timeout=10)
    print(data)
    try:
        headers, response = http.request("http://localhost/solr/"+colname.lower()+"/raw/update", method="POST",body=bytes(data.encode('utf-8')),  headers={'Content-type': 'text/xml'}) 
    except:
        time.sleep(2)
        headers, response = http.request("http://localhost/solr/"+colname.lower()+"/raw/update", method="POST",body=bytes(data.encode('utf-8')),  headers={'Content-type': 'text/xml'}) 
    return(headers)

class mongoDB_client():
    dbHandler = False
    def __init__(self, serverName="192.87.165.3", port=27017):
        try:
            self.dbHandler = pymongo.Connection(serverName, port)
        except:
            sys.stdout.write("Could not open " + serverName + " on port " + str(port) + "\n")
            os._exit(-1)

if __name__ == "__main__":


    colname="GGC"

    handler = mongoDB_client()

    handler.dbHandler["OAI"]
    handle=handler.dbHandler["OAI"][colname].find({"status" : "done" })
    print(handle.count())
    #record = handle.next()
    """
    i=0
    while record:
        
        record = handle.next()
        fh=open("/tmp/in_"+record["_id"]+".xml", "wb")
        fh.write(record["data"].encode('utf-8'))
        fh.close()

        post_data=os.popen("/usr/bin/xsltproc /home/wfa010/trunk/misc/OAI/xsl/"+colname+"_default.xsl /tmp/in_"+record["_id"]+".xml 2>/dev/null").read().decode('UTF-8')
        if (len(post_data) > 0):
            response = post_url(post_data, colname)
            if int(response["status"]) == 200:
                record["status"] = "indexed"
                handler.dbHandler["OAI"][colname].save(record)
                os.unlink("/tmp/in_"+record["_id"]+".xml")
            else:
                print("error")
        else:
            print("Err")
            try:
                os.unlink("/tmp/in_"+record["_id"]+".xml")
            except:
                pass
    """
