#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (C) 2009 by Willem Jan Faber
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.
#


import os, sys
import hashlib
import urllib2, urllib
import pickle, gzip, BeautifulSoup

def read_cache(file):
    try:
        input=gzip.open(file, 'rb')
        data=pickle.load(input)
        input.close()
        return(data)
    except:
        return(False)

def write_cache(file, data):
    output=gzip.open(file, 'wb')
    pickle.dump(data, output)
    output.close()

class Helper(object):
    def __init__(self):
        pass

    def read_cache(self, file):
        try:
            input=gzip.open('/tmp/'+file, 'rb')
            data=pickle.load(input)
            input.close()
            return(data)
        except:
            return(False)

    def write_cache(self, file, data):
        output=gzip.open('/tmp/'+file, 'wb')
        pickle.dump(data, output)
        output.close()

    def get_url(self, url):
        data=urllib2.Request(url)
        data.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2; .NET CLR 1.1.4322)')
        data=urllib2.urlopen(data).read().decode("utf-8", "xmlcharrefreplace").encode('ascii', 'xmlcharrefreplace')
        return(data)

class Query(object):
    helper = Helper()
    baseURL = ""
    name = ""
    query=""
    def __init__(self, query):
        pass

    def get_result(self):
        url=self.baseURL+urllib.quote_plus(self.query)
        hash=hashlib.md5(self.name+self.query).hexdigest()
        self.data=self.helper.read_cache(hash)
        if not self.data:
            self.data=self.helper.get_url(url)
            self.helper.write_cache(hash, self.data)
            print url, hash
        self.soep=BeautifulSoup.BeautifulSoup(self.data)

class Google(Query):
    helper = Helper()
    name = 'google'
    baseURL = 'http://www.google.com/search?q='

    def __init__(self, query, targetsite=False, inurl=False):
        if targetsite:
            self.query='site:'+targetsite+' '
        if inurl:
            self.query+='inurl:'+inurl+' '
        self.query+=query
        pass

    def get_first_result(self):
        self.get_result()
        divs=self.soep.findAll('div')
        for div in divs:
            if str(div).find('Search Results') > -1:
                links=BeautifulSoup.BeautifulSoup(str(div.findAll('a'))).findAll('a')
                for link in links:
                    return(link.extract(), link.contents)

class Imdb_serie(Query):
    helper = Helper()
    name = 'imdb'
    baseURL = 'http://www.imdb.com/find?q='

    def __init__(self):
        pass

