#!/usr/bin/env python

##  catalog.py
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

import os
import cgi
import pymongo
from pprint import pprint


connection = pymongo.Connection("42.42.0.24", 27017)
db = connection.library.catalog


#find_one({"isbn" : %s"})

print "Content-Type: text/html"
print
for item in db.find():
    for key in item.keys():
        if (type(item[key]) == type(u'')):
            print(key + " : " + item["isbn"] + "<br>")
        if (type(item[key]) == type([])):
            for val in item[key]:
                print(key + " : " + val + "<br>")
    print("<hr>")
