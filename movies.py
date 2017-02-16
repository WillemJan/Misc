#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
#   
# Atpmes - (C) Copyright 2006 Willem Jan, Faber
# Aloha's Triple Play Multimedia Entertainment System
#   
# vim options : sw=4, ts=4, expandtab
#
'''input.movies'''

import os,time, urllib2,sys
import twill
from BeautifulSoup import BeautifulSoup
import fnmatch

from cStringIO import StringIO

def lookup(sname,syear):
    imdb = twill.commands
    out= StringIO()
    twill.set_output(out)
    res=imdb.go("http://www.imdb.com/find?s=all&q=")
    res=imdb.formvalue(1,"q",sname)
    res=imdb.tidy_ok()
    res=imdb.submit(0)
    
    soep=BeautifulSoup(imdb.get_browser().get_html())
    u=unicode(sname+" (" + syear+")")

    if soep.title.contents[0] == u:
        print("superb!")
    links=soep.findAll('a')
    for l in links:
        line=str(l)
        if (line.find("directorlist")>-1):
            print "*************" + line
            print l.contents
    #links=soep.findAll('h5')
    #for l in links:
    #    print (l)
#            print((str(l).split("/")[5]),soep.title.contents[0])

#    s=soep.body.fetch("p")
#    print(s)

#soep=BeautifulSoup(urllib2.urlopen("http://www.imdb.com/title/"+title).read() )
#for link in soep.findAll('a'):
#    if not (str(link).find("poster")) == -1:
#        img=str(link)[str(link).find("src="):]
#        return(img.split('"')[1])

i=0
file=sys.argv[1]
remove_keywords = ( 'axxo', 'dvdrip' , '[]', '.avi')

for year in range(1800,2009):
    year=str(year)
    if (file.find(year) > -1):
        file=file.replace(year, "")
        break

for keyword in remove_keywords:
    if file.lower().find(keyword) > -1:
        file=file[:file.lower().find(keyword)] + file[file.lower().find(keyword)+len(keyword):]

while file.endswith('-'):
    file=file[:-1]

if (file.find('.') > -1):
    file=file.replace('.',' ')

print lookup(file, year)
