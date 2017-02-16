b
#!/usr/bin/env python

##
##  book_metadata.py
##
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

import sys,urllib,string
import url_cache,os
import lxml_lib
import isbn
from pprint import pprint

__all__ = "SRU"

class SRU(object):
    """
        SRU, Search and Retrieve via URL is a common standard amongst library's to exchange metadata about written works.
        This module is intended to fetch information about books from national libraries all over the world.
        
        As input an ISBN is required, or the barcode on a book.
    """

    SRU_servers = { "http://jsru.kb.nl/sru?query=%s&version=1.1&operation=searchRetrieve&maximumRecords=1&recordSchema=%s&x-collection=GGC": ["dc","dcx"],
                    "http://z3950.loc.gov:7090/voyager?version=1.1&operation=searchRetrieve&maximumRecords=1&query=%s&recordSchema=%s" : ["dc","mods"] }
                      
    #"USA_alt" : "http://sru.biblios.net/bibliographic?version=1.1&operation=searchRetrieve&query=%s&startRecord=1&maximumRecords=1&recordSchema=dc"}

    worldcat_lookup = "http://xisbn.worldcat.org/webservices/xid/isbn/%s?method=getEditions&fl=*&format=python"
    openlibrary_lookup = "http://openlibrary.org/api/books?bibkeys=ISBN:%s&callback=processOLBooks&details=true"

    test_isbns = [ "906233506", "9781861002211"]

    def __init__(self, DEBUG=False):
        self.DEBUG=DEBUG
        url_cache.DEBUG=DEBUG

    def fix_isbn(self,cisbn):
        """
            Convert barcode to isbn number

        """
        cisbn=cisbn.strip()
        cisbn=cisbn.replace('\n','')
        if cisbn.startswith("978"):
            cisbn=cisbn.replace("978","")
            if len(cisbn) == 10:
                cisbn=cisbn[0:-1]+""
        if len(cisbn) == 9:
            cisbn=cisbn+str(isbn.check(cisbn))
        return(cisbn)

    def getSRUdata(self, cisbn):
        cisbn=self.fix_isbn(cisbn)
        if (isbn.isValid(cisbn)):
            for server in self.SRU_servers.keys():
                data=url_cache.getURLdata(server %(cisbn,"dc"))
                if data:
                    data=lxml_lib.fromstring(data)
                    for child in data.getchildren():
                        if (child.tag.endswith("numberOfRecords")):
                            if (string.atoi(child.text)) > 0:
                                return(self._parse_dc_awnser(data, cisbn))
                                break
        return(False)

    def _parse_dcx_awnser(self, data, cisbn):
        data=data.find("{http://www.loc.gov/zing/srw/}records").find("{http://www.loc.gov/zing/srw/}record").find("{http://www.loc.gov/zing/srw/}recordData")
        dc=data.find("{info:srw/schema/1/dc-v1.1}dc")
        result={"isbn" : cisbn }
        for item in dc.getchildren():
            for attr in item.attrib.keys():
                name=item.tag.split("}")[1]
                if item.get(attr).find(":") > -1:
                    if not item.get(attr).split(":")[1].isdigit():
                        name=item.get(attr).split(":")[1]
                if not name in result.keys():
                    result[name] = [item.text]
                else:
                    result[name].append(item.text)
        return(result)

    def _parse_dc_awnser(self, data, cisbn):
        data=data.find("{http://www.loc.gov/zing/srw/}records").find("{http://www.loc.gov/zing/srw/}record").find("{http://www.loc.gov/zing/srw/}recordData")
        dc=data.find("{info:srw/schema/1/dc-schema}dc")
        if dc is not None:
            data=dc
        else:
            dc=data.find("{info:srw/schema/1/dc-v1.1}dc")
            if dc is not None:
                data=dc

        result={"isbn" : cisbn }
        for item in data.getchildren():
            if not item.tag.split("}")[1] in result.keys():
                result[item.tag.split("}")[1]]=[item.text]
            else:
                result[item.tag.split("}")[1]].append(item.text)
        return(result)

    def test(self):
        ok={}
        data=[]
        for item in self.test_isbns:
            pprint(self.getSRUdata(item))
        return(data)

    def read_scanner(self):
        line=""
        for char in sys.stdin.readline():
            line+=char
        return(self.fix_isbn(line))

if __name__ == "__main__":
    sru=SRU()
    sru.test()
