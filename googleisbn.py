#!/usr/bin/env python
#-*- coding: utf-8 -*-

##
## google_isbn.py - LODproxy.
##
## Copyright (c) 2010-2012 Koninklijke Bibliotheek - National library of the Netherlands.
##
## this program is free software: you can redistribute it and/or modify
## it under the terms of the gnu general public license as published by
## the free software foundation, either version 3 of the license, or
## (at your option) any later version.
##
## this program is distributed in the hope that it will be useful,
## but without any warranty; without even the implied warranty of
## merchantability or fitness for a particular purpose. see the
## gnu general public license for more details.
##
## you should have received a copy of the gnu general public license
## along with this program. if not, see <http://www.gnu.org/licenses/>.
##

__author__ = "Willem Jan Faber"

import sys

from LODproxy import *
from urllib2 import quote
from pprint import pprint

#backend.DEBUG = True 

class GOOGLEisbn():
    def __init__(self, isbn = "9051609639"):
        self.data = get_data_record(isbn,
                baseurl = "http://www.google.com/books/feeds/volumes/?q=ISBN<%s>",
                name = "google_isbn",
                force_type="feed")
        self.isbn = isbn

    def parse(self, record=0, *arg):
        if len(arg) > 0:
            ret = {}
            for item in arg:
                if item in data["data"]["entries"][record].keys():
                     ret[item] = self.data["data"]["entries"][0][item]
            if len(arg) == 1:
                return(ret[arg[0]])
            else:
                return(ret)
        else:
            try:
               return(self.data["data"]["entries"][record])
            except:
                self.data["error"] = "Could not retrieve " + quote(self.isbn)
                return(self.data)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        gi = GOOGLEisbn()
        pprint(gi.parse())
