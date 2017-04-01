#!/usr/bin/env python

import os, sys
from xml.etree import ElementTree as etree


from httplib2 import Http
import urllib
import simplejson

def post_url(data):
    http = Http(timeout=10)
    headers, response = http.request("http://localhost:8983/solr/core0/update", method="POST",body=bytes(data.encode('utf-8')),  headers={'Content-type': 'text/xml', 'connection': 'close'})
    

with open("data/labels_nl", "r") as fh:
    line = fh.readline()
    i=0
    while line:
        i+=1
        solr_add = etree.Element("add")
        doc = etree.SubElement(solr_add, "doc")
        add=etree.SubElement(doc, 'field', {"name" : "id"})
        id=etree.SubElement(doc, 'field', {"name" : "id_str"})
        fullrecord=etree.SubElement(doc, 'field', {"name" : "fullrecord"})
        dbpedia_label = line.split('>')[0].split('<')[1].replace('http://dbpedia.org/resource/','')
        wikipedia_label = line.split('"')[1]
        line = fh.readline()
        add.text=dbpedia_label
        id.text=dbpedia_label
        add=etree.SubElement(doc, 'field', {"name" : "label_nl_str"})
        add.text = wikipedia_label
        fullrecord.text=dbpedia_label+'\n'+wikipedia_label

        try:
            d=simplejson.loads(urllib.urlopen('http://data.kbresearch.nl/dbp:%s?abstract_nl,comment_nl' % dbpedia_label).read())        
            if 'abstract_nl' in d:
                abstract=etree.SubElement(doc, 'field', {"name" : "abstract_nl"})
                abstract.text=d['abstract_nl']
                fullrecord.text+="\n"+abstract.text
            if 'comment_nl' in d:
                abstract=etree.SubElement(doc, 'field', {"name" : "comment_nl"})
                abstract.text=d['comment_nl']
                fullrecord.text+="\n"+abstract.text
        except:
            pass
        
        try:
            post_url(etree.tostring(solr_add))
        except:
            pass
