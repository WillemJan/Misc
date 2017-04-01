#!/usr/bin/env python

import os, sys

import urllib
from pprint import pprint
import xml.etree.ElementTree as etree


def get_image(word, size=100):
    url='https://secure.wikimedia.org/wikipedia/en/w/api.php?action=opensearch&search=%s&limit=2&namespace=0&format=xmlfm' % urllib.quote(word.encode('utf-8'))
    data=etree.fromstring(urllib.urlopen(url).read())
    for item in data.getiterator():
        if item.text:
            if item.text.find('upload') > -1:
                img=item.text
                break
    try:
        item='/'.join(img.split('px')[0].split('/')[:-1])
        item+="/"+str(size)+"px"+"".join(img.split('px')[1:])
        return(item)
    except:
        return(False)


image = get_image("Tramweg_Maatschappij_De_Graafschap")
