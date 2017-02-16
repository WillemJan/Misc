#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.001"

import os, sys,  fnmatch, hashlib, threading, urllib2, re, pickle, magic, urllib, urllib2

from cStringIO import StringIO

from BeautifulSoup import BeautifulSoup
from xml.sax.saxutils import unescape

class Artifact(object):
    __usage__ = "PrutsGood-"+sys.argv[0][2:-3]+"_manager v"+__version__+"""

    Usage : artifacet_manager[add [path]] [version]
                          add, mark path as collection of pruts-artifacts.

    """

    def __init__(self, directory):

        self.directory=os.path.realpath(directory)
        self.stack = [directory]
        self.files = []

        self.dir_names= []
        self.file_names= []

        self.fingerprints = {}

        self.index=0
        self.error=0

        self.__walk_dir__(self.index)

        print "Working on path \t : \t" + directory
        print "Total nr of files \t : \t" + str(len(self.file_names))
        print "Total nr of directorys \t : \t" + str(len(self.dir_names))

        self.__fingerprint_files__()


    def __fingerprint_files__(self):
        for i in range(0, len(self.file_names)):
            filename=self.file_names[i]
            size=False
            try:
                file=open(filename, "rb")
                size=(os.stat(filename).st_size)
            except:
                pass

            if size:
                if size>1024:
                    data=file.read(1024)
                else:
                    data=file.read()
                hash=hashlib.md5(data).hexdigest()
                hash=hashlib.md5(filename+hash).hexdigest()
                file.close()
                try:
                    print self.fingerprints[hash]  # here i have seen the finger print and have to do something clever.
                    os._exit(-1)
                except:
                    self.fingerprints[hash]=hash
                    print(filename, hash)

    def __walk_dir__(self, index):
        while 1:
            try:
                file = self.files[self.index]
                self.index = self.index + 1
            except IndexError:
                try:
                    self.directory = self.stack.pop()
                except:
                    return()
                try:
                    self.files = os.listdir(self.directory)
                except:
                   try:
                        self.directory = self.stack.pop()
                   except:
                        return()
                   try:
                        self.files = os.listdir(self.directory)
                   except:
                        return()
                   self.error += 1
                self.index = 0
            else:
                fullname = os.path.join(self.directory, file)
                if os.path.isdir(fullname) and not os.path.islink(fullname):
                    self.stack.append(fullname)
                if fnmatch.fnmatch(file, '*'):
                    if os.path.isdir(os.path.realpath(fullname)):
                        self.dir_names.append(os.path.realpath(fullname).replace(self.directory, ''))
                    else:
                        self.file_names.append(os.path.realpath(fullname))


'''

class Collection(object):
    ms = magic.open(magic.MAGIC_NONE)
    ms.load()



    def __init__(self):

        if len(sys.argv) < 2:
            print (self.__usage__)
            os._exit(-1)

        if sys.argv[1] == 'add':

            try:
                stat=(os.stat(os.path.realpath(sys.argv[2])))
                path=os.path.realpath(sys.argv[2])
            except:
                print (self.__usage__)
                try:
                    print ("\nPath not valid : " + sys.argv[2]+"\n")
                except:
                    pass
                os._exit(-1)

            self.walk = Walk(path)
            start_path_len=len(path.split('/'))

            dir_names={}
            file_names={}
            i=j=0
            serie_list={}
            video=0
            video_data={}

            for item in range(0,len(self.walk.names)):
                if len(self.walk.names[item].split('/')[start_path_len:]) == 1:
                    # the directory name must contain the serie name, more or less, else no google result, no fun, no imdb 
                    if self.ms.file(self.walk.names[item]).strip() == 'directory':  
                        dir_name=self.walk.names[item] 
                        name='"episode list for" '
                        name+=self.walk.names[item].replace(path.replace('-',' ').lower().strip()
                        serie_name=self.walk.names[item].replace(path.replace('-',' ').lower().strip()[1:].capitalize()
                        url="http://google.com/search?q="+urllib.quote_plus(name)

                        try:
                            path='/tmp/prutsgood_'+hashlib.md5(url).hexdigest()
                            output=open(path, 'rb')
                            google_data=BeautifulSoup(pickle.load(output))
                            output.close()
                        except:
                            print "Getting showlist from" + url
                            data=urllib2.Request(url)
                            data.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2; .NET CLR 1.1.4322)')
                            path='/tmp/prutsgood_'+hashlib.md5(url).hexdigest()
                            google_data=urllib2.urlopen(data).read().decode('ascii', 'replace')
                            output=open(path, 'wb')
                            pickle.dump(google_data,output)
                            google_data=BeautifulSoup(google_data)
                            output.close()

                        for item in google_data.findAll('a'):
                            if str(item).find('http://www.imdb.com/title/tt')>-1:
                                year=re.search('\(\d\d\d\d\)\s-', str(item)).group(0)
                                startpos=str(item).find('http://www.imdb.com/title/tt')
                                endpos=str(item).find('/episodes')
                                imdb_title=str(item)[startpos:endpos]
                                imdb_year=year[1:5]
                                serie_list[dir_name]=serie_name, imdb_year, imdb_title
                                break
                elif self.ms.file(self.walk.names[item]).strip().find('video') > -1:
                    video+=1
                    found=False
                    for serie in serie_list.keys():
                        if str(self.walk.names[item]).startswith(serie):
                            name=str(self.walk.names[item].replace(serie, '')).lower()
                            name=name.replace('/', ' ')
                            name=name.replace('.', ' ')
                            name=name.replace('-', ' ')
                            name=name.replace('season  ', ' s')
                            name=name.replace('series ', 's')
                            try:
                                episode = re.search('s\s*(\d+)\s*e\s*(\d+)', name).group(2)
                                season  = re.search('s\s*(\d+)\s*e\s*(\d+)', name).group(1)
                                found=True 
                                break
                            except:
                                pass
                            try:
                                episode = re.search('s\s*(\d+)\s*(\d+)', name).group(2)
                                season  = re.search('s\s*(\d+)\s*(\d+)', name).group(1)
                                found=True 
                                break
                            except:
                                pass
                            try:
                                episode = re.search('\s*(\d+)\s*x\s*(\d+)', name).group(2)
                                season  = re.search('\s*(\d+)\s*x\s*(\d+)', name).group(1)
                                found=True
                                break
                            except:
                                pass
                    if not found:
                        print(video, 'not found !!')
                    else:
                        if episode.startswith('0'):
                            episode=episode[1:]
                        if season.startswith('0'):
                            season=season[1:]
                        video_data[self.walk.names[item]]=(serie_list[serie], season, episode)

            path="series_data.pickle"
            output=open(path, 'wb')
            pickle.dump(video_data,output)
            output.close()
'''
if __name__ == "__main__":


    if len(sys.argv) < 2:
        print (Artifact.__usage__)
        os._exit(-1)

    if sys.argv[1] == 'add':
        try:
            path=os.path.realpath(sys.argv[2])
        except:
            path="\nfatal : No path in command line\n"
        try:
            stat=os.stat(path)
        except:
            print (path)
            print (Artifact.__usage__)
            os._exit(-1)

        artifact = Artifact(path)
