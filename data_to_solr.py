#!/usr/bin/env python

import os
import sys
import json
import urllib
import simplejson

from httplib2 import Http
from xml.etree import ElementTree as etree

from pprint import pprint

def post_url(data):
    http = Http(timeout=10)
    headers, response = http.request("http://localhost:8983/solr/core0/update/json",
                                        method="POST",
                                        body=json.dumps(data),
                                        headers={'Content-type': 'application/json',
                                        'connection': 'close'})

with open("data/labels_nl", "r") as fh:
    line = fh.readline()
    i=0
    docs=[]
    while line:
        i+=1
        if i%100 == 0:
            post_url(docs)
            docs = []
        doc = {}
        
        doc["id"] = line.split('>')[0].split('<')[1].replace('http://dbpedia.org/resource/','')
        doc["label_nl_str"] = wikipedia_label = line.split('"')[1]
        try:
            d=simplejson.loads(urllib.urlopen('http://data.kbresearch.nl/dbp:%s?abstract_nl,comment_nl' % doc["id"]).read())
            if 'abstract_nl' in d:
                doc["abstract_nl_str"] = d["abstract_nl"]
            if 'comment_nl' in d:
                doc["comment_nl"] = d["comment_nl"]
        except:
            pass
        line = fh.readline()
        docs.append(doc)
        
        try:
            post_url(etree.tostring(solr_add))
        except:
            pass
