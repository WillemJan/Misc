#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

"""
    This file is part of Europeana Random Image Explorer.

    Copyright (C) 2011 Willem Jan Faber, Koninklijke Bibliotheek - National Library of the Netherlands

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from urllib import quote
import random
import urllib
import os

from xml.etree import ElementTree as etree
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import Element

KEY = ""


class API(object):
    BASEURL = "http://api.europeana.eu/api/opensearch.rss?searchTerms=%s&startPage=%s&wskey="+KEY
    numfound = 0
    records=[]
    page = 1

    def __init__(self):
        pass
 
    def randomize(self):
        ''' Returns a differerent startPage '''

        if int(self.numfound) > 100:
            i=int(random.randrange((int(self.numfound)-2)/12))
            i+=1
            while i>20: #
                i=i/20 # lols
            self.data = urllib.urlopen(self.url.replace('startPage=1' ,'startPage='+str(i))).read()
            self.__parse__(False)

 
    def query(self, query, fetch=True):
        self.url = self.BASEURL % (quote(query.encode('utf-8')), self.page)
        # query the API.
        self.data = urllib.urlopen(self.url).read() 
        # full self.records[] with brief record infromation.
        self.__parse__(fetch)

    def __parse__(self, fetch=True):
        try:
            data = etree.fromstring(self.data)
        except:
            self.records=[]
            self.numfound=0
            return()

        counter = 0
        self.records=[]

        self.numfound = data.find('channel').find('{http://a9.com/-/spec/opensearch/1.1/}totalResults').text
        for item in data.findall('.//item'):
           self.records.append({})
           for name in item.getchildren():
                if name.tag == "link":
                    name.text=name.text.replace(KEY,'')
                    if fetch:
                        self.records[counter]["data"]={}
                        self.get_parse_europeana_object(name.text, counter)
                    else:
                        if name.text:
                            self.records[counter][name.tag] = name.text
                else:
                    if name.text:
                        self.records[counter][name.tag] = name.text
           self.records[counter]["counter"] = counter
           if "object" in self.records[counter].keys():
                self.records[counter]["object"] = urllib.urlencode(self.records[counter]["object"]) 
           counter += 1
           if counter == 7:
               break

    def get_parse_europeana_object(self, url, counter = None):
        if counter:
            data = etree.fromstring(urllib.urlopen(url).read())
            records=data.find("{http://www.loc.gov/zing/srw/}records").find("{http://www.loc.gov/zing/srw/}record").find("{http://www.loc.gov/zing/srw/}recordData")
            dc = records.find("{http://purl.org/dc/elements/1.1/}dc")
            for item in dc.getchildren():
                self.records[counter]["data"][item.tag.split('}')[1]]=item.text
        else:
            record={}
            fh=open('/tmp/debug','a')
            fh.write(url.replace('http:/', 'http://')+'?wskey='+KEY+'\n')
            fh.close()
            data = etree.fromstring(urllib.urlopen(url.replace('http:/', 'http://')+'?wskey='+KEY).read())
            records=data.find("{http://www.loc.gov/zing/srw/}records").find("{http://www.loc.gov/zing/srw/}record").find("{http://www.loc.gov/zing/srw/}recordData")
            dc = records.find("{http://purl.org/dc/elements/1.1/}dc")
            for item in dc.getchildren():
                record[item.tag.split('}')[1]]=item.text
            return(record)

            
if __name__ == "__main__":
    api = API()
    api.query("einstein", fetch=False)
    if len(api.records) > 0:
        print("API ok")
        print(api.records)
    else:
        print("API not happy")
    

