#!/usr/bin/env python

from hashlib import md5
import codecs
import os
import urllib
import socket

##  url_cache.py
##  copyright (c) 2010 willem jan faber
##
##  this program is free software: you can redistribute it and/or modify
##  it under the terms of the gnu general public license as published by
##  the free software foundation, either version 3 of the license, or
##  (at your option) any later version.
##
##  this program is distributed in the hope that it will be useful,
##  but without any warranty; without even the implied warranty of
##  merchantability or fitness for a particular purpose.  see the
##  gnu general public license for more details.
##
##  you should have received a copy of the gnu general public license
##  along with this program.  if not, see <http://www.gnu.org/licenses/>.
##


DEBUG = False
TMP_PATH = "/tmp"
socket.setdefaulttimeout(4)

def _getURLdataFromInetOrCache(url):
    urlhash=md5(url).hexdigest()
    filename=TMP_PATH+os.sep+urlhash+".xml"

    if not os.path.isfile(filename):
        if DEBUG:
            print("Fetching %s"% url)
        data=_getURLdatafromINET(url).decode('utf-8')
        if len(data) > 0:
            fh = codecs.open(filename, "w", "utf-8")
            fh.write(data)
            if DEBUG:
                print("Wrote %i bytes to %s"% (len(data), filename))
            fh.close()
            return(data.encode('ascii', 'xmlcharrefreplace'))
    else:
        file=open(filename, "r")
        if DEBUG:
            print("Reading %s from disk %s"% (url, filename))
        fh = codecs.open(filename, "r", "utf-8")
        data=fh.read()
        if DEBUG:
            print("Read %i bytes from disk" %len(data))
        fh.close()
        return(data.encode('ascii', 'xmlcharrefreplace'))
    return(False)

def _getURLdatafromINET(url):
    try:
        data=urllib.urlopen(url).read()
        return(data)
    except:
        if DEBUG:
            print("Failed to fetch data, internetz is broken or server is not up..")
        return("")

def getURLdata(url):
    return(_getURLdataFromInetOrCache(url))
