#!/usr/bin/env python3

import os
import ast
import bz2
import time

import http.client

import urllib.error
import urllib.parse
import urllib.request

from xml.etree import ElementTree as etree
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import Element

LANG = "nl"
DBPEDIA_url = "http://downloads.dbpedia.org/3.6/"+LANG+"/"
DBPEDIA_filename = "labels_"+LANG+".nt.bz2"

SOLR_url = "/solr/dbpedia/update/"
SOLR_base = "localhost:8080"

def parse_dbpedia_resource(dbpedia_resource = '<http://dbpedia.org/resource/Anthony_Fokker>', prefLang = LANG):
    """
        input: <dbpedia_ariticle_url>
        optional: language

        output: label, url, abstract

        >>> parse_dbpedia_resource("<http://dbpedia.org/resource/Anthony_Fokker>",'nl')
        {'url': 'http://dbpedia.org/resource/Anthony_Fokker', 'abstract': 'Anton Herman Gerard (Anthony) Fokker was een Nederlandse luchtvaartpionier en vliegtuigbouwer. Het vliegtuigbedrijf Fokker is naar hem genoemd.', 'label': 'Anthony Fokker'}

    """

    resource = dbpedia_resource.split('<')[1].split('>')[0]
    resource_url = resource
    resource_name = urllib.parse.unquote(resource)

    label=False
    abstract=False

    try:
        dbpedia_object = ast.literal_eval(urllib.request.urlopen(resource.replace('resource', 'data')+'.json').read().decode('iso-8859-1'))
    except:
        print("Failed to get " + resource.replace('resource', 'data')+'.json')
        time.sleep(0.05)
        return({})

    if resource_name in dbpedia_object.keys():
        if 'http://www.w3.org/2000/01/rdf-schema#label' in dbpedia_object[resource_name].keys():
            for item in dbpedia_object[resource_name]['http://www.w3.org/2000/01/rdf-schema#label']:
                if item['lang'] == prefLang:
                    label = item['value']
            if not label:
                for item in dbpedia_object[resource_name]['http://www.w3.org/2000/01/rdf-schema#label']:
                    if item['lang'] == 'en':
                        label = item['value']
        if 'http://dbpedia.org/ontology/abstract' in dbpedia_object[resource_name].keys():
            for item in dbpedia_object[resource_name]['http://dbpedia.org/ontology/abstract']:
                if item['lang'] == prefLang:
                    abstract = item['value']
            if not abstract:
                for item in dbpedia_object[resource_name]['http://dbpedia.org/ontology/abstract']:
                    if item['lang'] == 'en':
                        abstract = item['value']

    if not label:
        label = "/".join(resource_name.split('/')[-1:])

    if abstract:
        return({"label" : label, "url" :  resource_url, "abstract" : abstract})
    else:
        return({"label" : label, "url" :  resource_url})

def get_dbpedia_data():
    """
        Download data from dbpedia, and test the .bz2 file
        returns filehandle

    """
    if not os.path.isfile(DBPEDIA_filename):
        print("Fetching " + DBPEDIA_url)
        fh=open(DBPEDIA_filename, "wb")
        try:
            data=urllib.request.urlopen(DBPEDIA_url+DBPEDIA_filename).read()
        except:
            print("Unable to read data from " + DBPEDIA_url)
            return(False)
        fh.write(data)
        fh.close()

    try:
        fh=bz2.BZ2File(DBPEDIA_filename)
        data=fh.readline()
        fh.close()
    except:
        print("Unable to read from " + DBPEDIA_filename + ", file is corrupt, remove the file and try again")
        return(False)

    fh=bz2.BZ2File(DBPEDIA_filename)
    return(fh)


def dbpedia_resource_to_solr(dbpedia_resource):
    doc = Element("add")
    add = SubElement(doc, "doc")

    if 'abstract'  in dbpedia_resource.keys():
        sub = SubElement(add, 'field', {"name" : "abstract_str" }) 
        sub.text=dbpedia_resource['abstract']

    sub = SubElement(add, 'field', {"name" : "prefLabel" }) 
    sub.text=dbpedia_resource['label']

    sub= SubElement(add, 'field', {"name" : "prefLabel_str" }) 
    sub.text=dbpedia_resource['label']

    sub = SubElement(add, 'field', {"name" : "id" }) 
    sub.text=dbpedia_resource['url']

    return(etree.tostring(doc))

def post_xml_to_solr(xml):
    done = False
    while not done:
        headers = {"Content-type" : "text/xml; charset=utf-8", "Accept": "text/plain"}
        conn = http.client.HTTPConnection(SOLR_base)
        conn.request("POST", SOLR_url, bytes(xml.encode('utf-8')), headers)
        response = conn.getresponse()
        if response.getcode() == 200:
            res = response.read()
            if not str(res).find("<int name=\"status\">0</int>") > -1:
                print(res)
        conn.close()
        done=True
    return()

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    resource = False
    dbpedia_data = get_dbpedia_data()

    if dbpedia_data:
        try:
            resource = dbpedia_data.readline().decode('iso-8859-1')
        except:
            resource=False

    while resource:
        resource_data = parse_dbpedia_resource(resource)

        if len(resource_data.keys()) > 0:
            print(resource_data['label'])
            xml=dbpedia_resource_to_solr(resource_data)
            post_xml_to_solr(xml)

        if dbpedia_data:
            try:
                resource = dbpedia_data.readline().decode('iso-8859-1')
            except:
                resource = False
