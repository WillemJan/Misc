#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 by Willem Jan Faber
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.
#
#

'''

'''

__version__ = "0.001"

import os, sys, platform, string, subprocess, codecs
import hashlib, threading, pprint
import urllib, urllib2, re

from cStringIO import StringIO
from BeautifulSoup import BeautifulSoup
from xml.sax.saxutils import unescape
from pprint import pprint

class Query(object):
    helper = None
    baseURL = ""
    name = ""
    query=""
    def __init__(self, query):
        pass

    def get_result(self):
        url=self.baseURL+urllib.quote_plus(self.query)
        hash=hashlib.md5(self.name+self.query).hexdigest()
        data=self.helper.read_cache(hash+"_"+self.name)
        if not data:
            print ("getting fresh data", self.name, url)
            data=self.helper.get_url(url)
            self.helper.write_cache(hash+"_"+self.name, data)
        self.soep=BeautifulSoup.BeautifulSoup(data)

class Import(object):
    __doc__= """
    import new files and try to identify.
    to do this each file is given an unique md5sum. 
    this md5sum will correspond to the metadata in the couchdb database.
    """

    def __init__(self):
        directory="/shared_stuff"
        self.artifact_category = { 'series' : {}, 'documentary' :  {} }
        self.stack = [directory]
        self.__walk_dir__(directory)
        pprint(self.artifact_category)
        pass

    def __compare_names__(self, dirname, filename):
        wierd = ("-" , ".", "_", ",")
        for item in wierd:
            ndirname=dirname.replace(item, ' ').lower()
            nfilename=filename.replace(item, ' ').lower()
        j=p=0

        name=""
        for item in nfilename.split(" "):
            if ndirname.find(item)>-1:
                name+=item+" "
        print(name, filename, dirname)


    def __walk_dir__(self, directory):
        self.file=[directory]
        self.directory=directory
        self.file_index=0
        self.index=0

        while 1:
            try:
                file = self.file[self.index]
                self.index = self.index + 1
            except IndexError:
                try:
                    self.directory = self.stack.pop()
                except:
                    return()
                try:
                    self.file = os.listdir(self.directory)
                except:
                   try:
                        self.directory = self.stack.pop()
                   except:
                        return()
                   try:
                        self.file = os.listdir(self.directory)
                   except:
                        return()
                self.index = 0
            else:
                fullname = os.path.join(self.directory, file)
                if os.path.isdir(fullname) and not os.path.islink(fullname):
                    self.stack.append(fullname)
                if os.path.isdir(os.path.realpath(fullname)):
                    path=os.path.realpath(fullname)
                    for key in self.artifact_category.keys():
                        if path.find(key) > -1:
                            short_dirname=path[path.find(key)+len(key)+1:]
                            if short_dirname.find("/") > -1:
                                short_filename=short_dirname.split("/")[-1]
                                short_dirname=short_dirname.split("/")[0]
                                self.__compare_names__(short_dirname, short_filename)
                                self.artifact_category[key][path]={'short_dirname' : short_dirname, 'short_filename' : short_filename ,  'dirname'  : path }
                            else:
                                break
                elif not os.path.islink(fullname):
                    self.file_index+=1
                    path=str(os.path.realpath(fullname))
                    for key in self.artifact_category.keys():
                        if path.find(key) > -1:
                            short_dirname=path[path.find(key)+len(key)+1:]
                            if short_dirname.find("/") > -1:
                                short_filename=short_dirname.split("/")[-1]
                                short_dirname="/".join(short_dirname.split("/")[0:-1])
                                self.__compare_names__(short_dirname, short_filename)
                                self.artifact_category[key][path]={'short_dirname' : short_dirname, 'short_filename' : short_filename ,  'path'  : path }
                            else:
                                break



if __name__ == "__main__":
    imp = Import()
