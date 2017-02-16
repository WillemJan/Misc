#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
import urllib
import os

from xml.etree import ElementTree as etree
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import Element

KEY = "ATVPVJJCUA"

class API(object):
    BASEURL = "http://api.europeana.eu/api/opensearch.rss?searchTerms=%s&wskey="+KEY
    numfound = 0
    records=[]

    def __init__(self):
        pass

    def query(self, query, fetch=True):
        url = self.BASEURL % (query)
        self.data = urllib.urlopen(url).read()
        self.__parse__(fetch)

    def __parse__(self, fetch=True):
        data = etree.fromstring(self.data)
        counter = 0
        self.records=[]

        self.numfound = data.find('channel').find('{http://a9.com/-/spec/opensearch/1.1/}totalResults').text

        for item in data.findall('.//item'):
           self.records.append({})
           for name in item.getchildren():
                if name.tag == "link":
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
           counter += 1

    def get_parse_europeana_object(self, url, counter = None):
        if counter:
            data = etree.fromstring(urllib.urlopen(url).read(), encoding='iso-8859-1')
            records=data.find("{http://www.loc.gov/zing/srw/}records").find("{http://www.loc.gov/zing/srw/}record").find("{http://www.loc.gov/zing/srw/}recordData")
            dc = records.find("{http://purl.org/dc/elements/1.1/}dc")
            for item in dc.getchildren():
                self.records[counter]["data"][item.tag.split('}')[1]]=item.text
        else:
            record={}
            url=url.replace('http:/', 'http://')
            data = etree.fromstring(urllib.urlopen(url).read())

            records=data.find("{http://www.loc.gov/zing/srw/}records").find("{http://www.loc.gov/zing/srw/}record").find("{http://www.loc.gov/zing/srw/}recordData")
            dc = records.find("{http://purl.org/dc/elements/1.1/}dc")
            for item in dc.getchildren():
                record[item.tag.split('}')[1]]=item.text
            return(record)

            
if __name__ == "__main__":
    api = API()
    print (api.query("description:albert+einstein%20AND%20title:albert+einstein"))
    pprint(api.records[0])
