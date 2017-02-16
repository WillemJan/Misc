#!/usr/bin/env python3

import os
import ast
import bz2
import sys
import time

import http.client

import urllib.error
import urllib.parse
import urllib.request

from xml.etree import ElementTree as etree
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import Element


class DBpedia(object):
    """

    DBpedia downloads the label.bz2 file, 
    and can be used to access the online version of DBpedia.

    It provides an iterator which enables iteration over dbpedia objects.

    >>> dbpedia = DBpedia('nl')
    
    """

    LANG = "nl"
    CACHE_DIR = '/tmp'

    DBPEDIA_url = "http://downloads.dbpedia.org/3.6/"+LANG+"/"
    DBPEDIA_filename = "labels_"+LANG+".nt.bz2"

    DEBUG = 1

    AUTOGET = True
 
    dbpedia_label = {'label' : 'http://www.w3.org/2000/01/rdf-schema#label',
                     'abstract' : 'http://dbpedia.org/ontology/abstract',
                     'comment' : 'http://www.w3.org/2000/01/rdf-schema#comment', 
                     'dob' : 'http://dbpedia.org/property/birthDate' }

    def __init__(self, prefLang = 'nl'):
        if not prefLang == self.LANG:
            self.LANG = prefLang
            self.DBPEDIA_filename = "labels_"+self.LANG+".nt.bz2"
            self.DBPEDIA_url = "http://downloads.dbpedia.org/3.6/"+self.LANG+"/"

        if not os.path.isfile(self.CACHE_DIR+os.sep+self.DBPEDIA_filename):
            if self.DEBUG > 0:
                sys.stdout.write("Could not open " + self.CACHE_DIR + os.sep + self.DBPEDIA_filename+ "\n")
            if not self.download_labels():
                sys.stderr.write("Error while downloading labels.\n")
                os._exit(-1)

        self.fh = bz2.BZ2File(self.CACHE_DIR + os.sep + self.DBPEDIA_filename)

    def __iter__(self):
        return(self)

    def next(self):
        self.resource=self.fh.readline().decode('iso-8859-1').strip()
        return(self.resource)

    def get_dbpedia_data(self, dbpedia_data_type = "json")
        if not dbpedia_data_type in ("json", "jsod", "ntriples"):
            dbpedia_data_type = "json"
        if dbpedia_data_type == "json":
            url = self.resource.replace('resource', 'data')+".json"
        if dbpedia_data_type == "jsod":
            url = self.resource.replace('resource', 'data')+".json"
        if dbpedia_data_type == "ntriples":
            url = self.resource.replace('resource', 'data')+".ntriples"
        return(self.get_data(resource))

    def parse_ntriples_data(self):
        pass

    def parse_json_data(self):
        pass

    def parse_jsod_data(self):
        pass


    def get_data(self, url):
        try:
            data = urllib.request.urlopen(url)
        except:
            return(False)
        if data.getcode() == 200:
            data=data.read().decode('iso-8859-1')
            return(data)
        else:
            sys.stdout.write("Error while reading " + url + " got error code " + str(data.getcode())+"\n")
        return(False)

    """
    def extract(self, labelname, lang='nl'):
        if not lang == self.LANG:
            lang = self.LANG
        for item in self.resource_json.values():
            print(item)
            
            if self.dbpedia_label[labelname] in item.keys():
                for val in item[self.dbpedia_label[labelname]]:
                    print(val)
                    if 'lang' in val.keys():
                        if val['lang'] == lang:
                            return(val['value'])
                        for val in item[self.dbpedia_label[labelname]]:
                            if val['lang'] == 'en':
                                return(val['value'])
                    if 'value' in val.keys():
                        return(val['value'])

    def download_labels(self):
        """
            Fetches .bz2 label file from the dbpedia download site
            (http://downloads.dbpedia.org/) and put it in the CACHE_DIR path
        """
        if self.DEBUG > 0:
            sys.stdout.write("Downloading labels from " + self.DBPEDIA_url+ "\n")
        fh=open(self.CACHE_DIR + os.sep + self.DBPEDIA_filename, "wb")
        try:
            data=urllib.request.urlopen(self.DBPEDIA_url+self.DBPEDIA_filename).read()
        except:
            if self.DEBUG > 0:
                sys.stdout.write("Unable to read data from " + self.DBPEDIA_url+"\n")
            return(False)
        fh.write(data)
        fh.close()
        try:
            fh=bz2.BZ2File(self.CACHE_DIR + os.sep + self.DBPEDIA_filename)
            data=fh.readline()
            fh.close()
        except:
            sys.stderr.write("Unable to read from " + DBPEDIA_filename + ", file is corrupt, remove the file and try again.\n")
            return(False)
        sys.stdout.write("Downloading finished file stored ("+ self.CACHE_DIR + os.sep + self.DBPEDIA_filename+")\n")
        return(True)

if __name__ == "__main__":
    dbpedia = DBpedia()
    resource = dbpedia.next()
    while resource:
        resource = dbpedia.next()
