#!/usr/bin/env python

import book_metadata
import pymongo
from pprint import pprint

##  db.py
##  Copyright (C) 2010 Willem Jan Faber
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##


sru=book_metadata.SRU()

cisbn=sru.read_scanner()
connection = pymongo.Connection("example.com", 27017)

db = connection.library.catalog
record=db.find_one({"isbn" : cisbn})

if record:
    print("in db")
    pprint(record)
else:
    print("fresh store")
    pprint(record)
    data=sru.getSRUdata(cisbn)
    db = connection.library
    db.catalog.save(data)
connection.disconnect()
