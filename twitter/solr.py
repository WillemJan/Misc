#!/usr/bin/env python

##  solr.py - solr.py
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
##  Willem Jan Faber
##  willemjan \a(\t fe2 dot nl

import urllib, ast, sys

config = """graph_title Numer of records in SOLR
graph_args --base 1000 -l 0
graph_category solr
graph_vlabel records in SOLR
index_total.label Total number of records
index_total.draw LINE2

"""

def get_result(BaseUrl, query=False):
    try:
        if not query:
            BaseUrl+="/select/?q=*:*&wt=json"
        else:
            BaseUrl+="/select/?q=ispartof_str:"+query+"&wt=json"
        data=urllib.urlopen(BaseUrl).read()
        data=ast.literal_eval(data)
        sys.stdout.write(str(data["response"]['numFound'])+'\n')
    except:
        sys.stdout.write('0\n')

if __name__ == "__main__":

    if sys.argv[-1] == "config":
        for line in config.split('\n'):
            sys.stdout.write(line+"\n")
    else:
        sys.stdout.write("index_total.value ")
        BaseUrl="http://www.kbresearch.nl/solr"
        get_result(BaseUrl)
        sys.stdout.write("index_total.value ")
