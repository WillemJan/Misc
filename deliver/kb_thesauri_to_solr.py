#!/usr/bin/env python3.1

import os

from xml.etree.ElementTree import Element
from xml.etree import ElementTree as etree
from xml.etree.ElementTree import SubElement


SAMPLE_DATA = "kb_thesauri"+os.sep+"thesauri_data_example.xml"

if __name__ == "__main__":
    raw_data = ""

    if os.path.isfile(SAMPLE_DATA):
        fh = open(SAMPLE_DATA, "r")
        raw_data = fh.read()
        fh.close()

    dat, req, records = etree.fromstring(raw_data)

    
    for element in records:
        if element.tag.endswith('record'):
            for item in element.getiterator():
                if len(item.attrib) == 1:
                    print(item.tag.split('}')[1])
                    #for key in item.attrib.keys():
                    #    print(key.split('}')[1])
                    print(list(item.attrib.values())[0])
                    if item.text: print(item.text)
                else:
                    if item.tag.endswith('identifier'):
                        print(item.text)
