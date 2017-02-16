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
import lxml_lib

DEBUG = True

class harvest_identifiers():

    mongoDB = ""

    fromDate = ""
    metadataPrefix = "INDEXING"
    serverURL = "http://services.kb.nl/mdo/oai"
    setName = "GGC"

    resumptionToken = False

    def __init__(self, mongoDB=False, serverURL=False, setName=False, fromDate=False, metadataPrefix=False, resumptionToken=False):
        if serverURL:
            self.serverURL = serverURL
        if setName:
            self.setName = setName
        if fromDate:
            self.fromDate = fromDate
        if metadataPrefix:
            self.metadataPrefix = metadataPrefix

        if mongoDB:
            self.mongoDB = mongoDB
        else:
            sys.stdout.write("No database, no data, move along now.\n")

        if resumptionToken:
            self.resumptionToken = resumptionToken
        else:
            record = self.mongoDB[self.setName].find_one({"_id" : "from"})
            if record:
                self.fromDate = record["from"]
            record = self.mongoDB[self.setName].find_one({"_id" : "resumptionToken"})
            if record:
                self.resumptionToken = self.mongoDB[self.setName].find_one({"_id" : "resumptionToken"})["resumptionToken"]
        self.loop_once()

    def loop_once(self):
        if self.resumptionToken:
            url = self.serverURL + "?verb=ListIdentifiers&resumptionToken=" + self.resumptionToken
        else:
            if self.fromDate:
                url = self.serverURL + "?verb=ListIdentifiers&metadataPrefix=" + self.metadataPrefix + "&from=" + self.fromDate + "&set=" + self.setName
            else:
                url = self.serverURL + "?verb=ListIdentifiers&metadataPrefix=" + self.metadataPrefix + "&set=" + self.setName

        if DEBUG:
            print(url)

        try:
            data = urllib.urlopen(url).read()
        except:
            sys.stdout.write("Could not read data from " + url)
            os._exit(-1)

        data = lxml_lib.fromstring(data)

        add = True
        deleted = 0
        added = 0

        for item in data.iter():
            if item.tag.find("resumptionToken") > -1 and item.text and (added > 0 or deleted > 0):
                self.resumptionToken = item.text
                self.mongoDB[self.setName].save({"_id" : "resumptionToken", "resumptionToken" : item.text})
                if DEBUG:
                    print(added, deleted)
                return()
            if "status" in item.attrib:
                if item.attrib["status"] == "deleted":
                    add = False
            if item.tag.find("identifier") > -1:
                if add:
                    """ toMongo """
                    doc = {}
                    doc = { "id" : item.text, 
                            "status" : "new",
                            "_id" : hashlib.md5(item.text).hexdigest() } 
                    record = self.mongoDB[self.setName].find_one({"_id" : hashlib.md5(item.text).hexdigest()})
                    if record:
                        """record is allready there so don't mess with it"""
                        pass
                    else:
                        self.mongoDB[self.setName].insert(doc)
                    added+=1
                else:
                    """ deletefromMongo """
                    delete = self.mongoDB[self.setName].find_one({"_id" : hashlib.md5(item.text).hexdigest()})

                    if delete:
                        if delete["status"] == "new" or delete["status"] == "done":
                            self.mongoDB[self.setName].delete({"_id" : hashlib.md5(item.text).hexdigest()})
                    add = True
                    deleted += 1

        self.mongoDB[self.setName].save({"_id" : "resumptionToken", "resumptionToken" : False})
        self.mongoDB[self.setName].save({"_id" : "from", "from" : datetime.datetime.now().strftime("%Y-%m-%d") })
        self.resumptionToken = False

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
    print("todo : " + str(count.count()))
    total=count.count()

    for i in range(0,total):
        if (i%10 == 0):
            print("todo : " + str(total-i))
        record=mongoDB.dbHandler["OAI"][setname].find_one({"status" : "new"})
        record["status"] = "fetching"
        mongoDB.dbHandler["OAI"][setname].save(record)

        try:
            data=urllib.urlopen("http://services.kb.nl/mdo/oai?verb=GetRecord&identifier="+record["id"]+"&metadataPrefix=dcx+index").read()
            #data=urllib.urlopen("http://services.kb.nl/mdo/oai?verb=GetRecord&identifier="+record["id"]+"&metadataPrefix=dcx+index+admin").read()
            record["status"] = "done"
            record["data"] = data
            mongoDB.dbHandler["OAI"][setname].save(record)
        except:
            record["status"] = "failed"
            mongoDB.dbHandler["OAI"][setname].save(record)
            
    os._exit(-1)

