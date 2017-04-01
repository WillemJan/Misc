#!/usr/bin/env python

from xml.etree import ElementTree
import requests


def get_text():
    more_xml = []
    url = 'http://resources2.kb.nl/010425000/articletext/010427206/DDD_010427206_0013_articletext.xml'
    req = requests.get(url)
    if req.status_code == 200:
        xml = ElementTree.fromstring(req.text.encode('utf-8'))
        more_xml.append(xml)

    url = 'http://resources2.kb.nl/010425000/articletext/010427204/DDD_010427204_0011_articletext.xml'
    req = requests.get(url)
    if req.status_code == 200:
        xml = ElementTree.fromstring(req.text.encode('utf-8'))
        more_xml.append(xml)

    #NOISE
    url = 'http://resources2.kb.nl/010425000/articletext/010427202/DDD_010427202_0001_articletext.xml'
    req = requests.get(url)
    if req.status_code == 200:
        xml = ElementTree.fromstring(req.text.encode('utf-8'))
        more_xml.append(xml)

    url = 'http://resources2.kb.nl/010425000/articletext/010427206/DDD_010427206_0002_articletext.xml'
    req = requests.get(url)
    if req.status_code == 200:
        xml = ElementTree.fromstring(req.text.encode('utf-8'))
        more_xml.append(xml)

    url = 'http://resources2.kb.nl/010425000/articletext/010427206/DDD_010427206_0001_articletext.xml'
    req = requests.get(url)
    if req.status_code == 200:
        xml = ElementTree.fromstring(req.text.encode('utf-8'))
        more_xml.append(xml)
    url = 'http://resources2.kb.nl/010425000/articletext/010427206/DDD_010427206_0006_articletext.xml'
    req = requests.get(url)
    if req.status_code == 200:
        xml = ElementTree.fromstring(req.text.encode('utf-8'))
        more_xml.append(xml)


    return more_xml
