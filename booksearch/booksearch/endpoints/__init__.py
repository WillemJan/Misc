#/usr/bin/python
# -*- coding: utf-8 -*-
#
# endpoint.py
#
# Copyright (c) 2014-2019 WillemJan Faber.
#
# For licence information see LICENCE.txt,
# in the toplevel directory of this project.
#


import os

from .bl import BL
from .kb_nl import KB_NL
from .kb_se import KB_SE
from .loc import LOC
from .nb import NB
from .uc import UC

endpoints = { 'bl': BL, 
              'kb_nl': KB_NL,
              'kb_se': KB_SE,
              'loc': LOC,
              'nb': NB,
              'uc': UC
             }


'''
'http://services.d-nb.de/sru/zdb',
'http://api.libris.kb.se/sru/libris

    WORLDCAT_KEY = "YOUR_KEY_HERE"
    URL_WORLDCAT = "http://www.worldcat.org/webservices/catalog/search/opensearch?q=%s&wskey=%s"

    ISBNDB_KEY = "YOUR KEY HERE"
    URL_ISBNDB = "http://isbndb.com/api/books.xml?access_key=%s&index1=isbn&value1=%s"

    URL_OPENLIBRARY = "http://openlibrary.org/api/books?bibkeys=ISBN:%s&callback=mycallback&jscmd=data"

    URL_RYERSON = "http://news.library.ryerson.ca/api/isbnsearch.php?isbn=%s"

    URL_GOOGLE = "http://books.google.com/books/feeds/volumes?q=%s"

    URL_THING = "http://www.librarything.com/api/thingISBN/%s"
'''
