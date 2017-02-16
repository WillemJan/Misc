#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.001"

try:
    import os, sys, magic, fnmatch, hashlib, threading, twill, urllib2
    from BeautifulSoup import BeautifulSoup
    from xml.sax.saxutils import unescape
    import pickle

except:
    import os, sys
    print sys.argv[0][2:-3]+" v"+__version__
    print "Failed to load essential modules, see README.txt"
    os._exit(-1)


class ShowList(object):
    def __init__(self):
        show_list = ('http://www.imdb.com/company/co0056555/',       # National_geographic
                     'http://www.imdb.com/company/co0139461/',       # National_geographic
                     'http://www.imdb.com/company/co0103957/',       # BBC Worldwide
                     'http://www.imdb.com/title/tt0318224/episodes', # BBC Horizon
                     'http://www.imdb.com/company/co0005861/',       # HBO
                     'http://www.imdb.com/company/co0086397/')       # Sony pictures
        self.list=[]
        self.items={}

        for show in show_list:
            current = self.get_showlist(show)

    def check(self, name):
        name=name.lower()
        for item in self.items.keys():
            if item.lower() == (name):
                return(self.items[item])
        return(False)

    def get_and_cache(self, url):
        try:
            path = "/tmp/prutsgood_showlist.pickle."+hashlib.md5(url).hexdigest()
            input = open(path, 'rb')
            data = pickle.load(input)
            input.close()
        except:
            data = urllib2.urlopen(url).read()
            path = "/tmp/prutsgood_showlist.pickle."+hashlib.md5(url).hexdigest()
            output = open(path, 'wb')
            pickle.dump(data, output)
        return(data)

    def get_showlist(self, url):
        soep=BeautifulSoup(self.get_and_cache(url))
        links=soep.findAll('li')
        i=0
        for l in links:
            title=l.contents[0].attrs[0][1].encode()
            if (title.startswith('/title/tt') and title.endswith('/')):
                year=l.contents[1].split('(')[1].split(')')[0].encode('ascii')[:4]
                name=unescape(l.contents[0].contents[0].decode(), {"&#x26;" : '&', "&#x27;" : "'"  , '&#x22;' : ''}).split(' (')[0].encode('ascii', 'replace')
                if len(name) > 6:
                    self.items[name]=[title, year]
                    i+=1

        if i < 1:
            soep=BeautifulSoup(self.get_and_cache(url))
            links=soep.findAll('a')

            for l in links:
                title=l.attrs[0][1].encode('ascii')
                if (title.startswith('/title/tt') and title.endswith('/')):
                    name=unescape(l.contents[0].encode(), {"&#x26;" : '&', "&#x27;" : "'"  , '&#x22;' : ''})
                    if len(name) > 6:
                        self.items[name]=[title, "####"]

#.startswith('/title/tt'), l.content
    

