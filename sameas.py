#!/usr/bin/env python
#-*- coding: utf-8 -*-

##
## sameas.py - LODproxy.
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

import LODproxy
from pprint import pprint

LODproxy.backend.DEBUG = True 

class SAMEas():
    def __init__(self, identifier = "http%3A%2F%2Fdbpedia.org%2Fresource%2FAlbert_Einstein"):
        self.data = LODproxy.get_data_record(identifier, baseurl = "http://sameas.org/json?uri=%s", name = "sameas")
        self.identifier = identifier

    def parse(self, *arg):
        return(self.data["data"][0]["duplicates"])

if __name__ == "__main__":
    if len(sys.argv) == 1:
        same = SAMEas()
        pprint(same.parse())
        same = SAMEas()
        pprint(same.parse())
        same = SAMEas()
        pprint(same.parse())
