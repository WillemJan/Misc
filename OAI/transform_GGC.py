#!/usr/bin/env python

##
##  harvest_identifiers.py
##
##  Copyright (C) 2010 Willem Jan Faber
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

import os
import sys
import time
import urllib
import pymongo
import hashlib
import datetime
import libxml2
import libxslt
from httplib import HTTPConnection                                                                                                                                                                                                
from httplib2 import Http                                                                                                                                                                                                         


DEBUG = True

def post_url(data, colname="GGC"):
    http = Http(timeout=10)
    headers, response = http.request("http://kbresearch.nl/solr/"+colname.lower()+"/raw/update", method="POST",body=bytes(data),  headers={'Content-type': 'text/xml'}) 
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
    mongoDB = mongoDB_client()

    setname = "GGC"

    count=mongoDB.dbHandler["OAI"][setname].find({"status" : "new"})
    total=count.count()

    template=libxml2.parseFile("ggc.xsl")
    style = libxslt.parseStylesheetDoc(template)

    record=mongoDB.dbHandler["OAI"][setname].find_one({"status" : "indexed"})
    data=urllib.urlopen("http://services.kb.nl/mdo/oai?verb=GetRecord&identifier="+record["id"]+"&metadataPrefix=dcx+index").read()

    if total==0:
        os._exit(-1)

    for i in range(0,total):
        if (i%10 == 0):
            print("todo : " + str(total-i))

        doc=libxml2.parseDoc(data)
        result = style.applyStylesheet(doc, None)

        response=post_url(style.saveResultToString(result))
        libxslt.cleanup()

        if not (response["status"] == "200"):
            record["status"] = "done"
            mongoDB.dbHandler["OAI"][setname].save(record)
            print("update to solr failed, sleeping")
            print(response)
            time.sleep(10)
        else:
            record["status"] = "new"
            mongoDB.dbHandler["OAI"][setname].save(record)
            record=mongoDB.dbHandler["OAI"][setname].find_one({"status" : "indexed"})
            data=urllib.urlopen("http://services.kb.nl/mdo/oai?verb=GetRecord&identifier="+record["id"]+"&metadataPrefix=dcx+index").read() 
