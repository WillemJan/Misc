#!/usr/bin/env python3

"""
    Example code to index DBpedia into Solr, using python3
"""


import dbpedia

from pprint import pprint

from xml.etree.ElementTree import Element
from xml.etree import ElementTree as etree
from xml.etree.ElementTree import SubElement

if __name__ == "__main__":
    dbp = dbpedia.DBpedia(prefLang='nl')
    resource = dbp.next()
    i=0

    while resource:
        i+=1
        doc = Element("add")
        add = SubElement(doc, "doc")

        sub = SubElement(add, 'field', {"name" : "id" })
        sub.text = dbp.resource_id
        

        if dbp.extract('label'):
            sub = SubElement(add, 'field', {"name" : "prefLabel_str" })
            sub.text = dbp.extract('label')
        else:
            sub = SubElement(add, 'field', {"name" : "prefLabel_str" })
            sub.text = dbp.resource_id.split('/')[-1]

        if dbp.extract('abstract'):
            sub = SubElement(add, 'field', {"name" : "abstract" })
            sub.text = dbp.extract('abstract')

        if dbp.extract('comment'):
            if not dbp.extract('comment') == dbp.extract('abstract'):
                sub = SubElement(add, 'field', {"name" : "comment" })
                sub.text = dbp.extract('comment')

        print (etree.tostring(doc))
        resource = dbp.next()
        if i==1:
            break
