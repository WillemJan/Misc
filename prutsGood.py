#!/usr/bin/env python
import os, threading, fnmatch, hashlib
from utils import Log, Ramdrive

class Walk:
    def __init__(self, directory, pattern="*"):
        self.stack = [directory]
        self.pattern = pattern
        self.files = []
        self.index = 0
        self.list = {}
        self.__getitem__(self.index)

    def __getitem__(self, index):
        while 1:
            try:
                file = self.files[self.index]
                self.index = self.index + 1
            except IndexError:
                try:
                    self.directory = self.stack.pop()
                except:
                    return(self.list)
                self.files = os.listdir(self.directory)
                self.index = 0
            else:
                fullname = os.path.join(self.directory, file)
                if os.path.isdir(fullname) and not os.path.islink(fullname):
                    self.stack.append(fullname)
                if fnmatch.fnmatch(file, self.pattern) and not os.path.isdir(fullname):
                    fstat=os.stat(fullname)
                    hash=hashlib.md5(str(fullname)).hexdigest()
                    self.list[hash]=(fstat.st_size, fullname)

class collection(object):

    log=Log()

    path=[]
    files=[]

    type=False

    AUDIO = 0
    VIDEO = 1

    collection_index ={} 

    collection_type=["audio", "video", "text"]


    def __init__(self, type):
        """ Initialize all collections, by collecting files, and writing a db of files to a ramdrive """
        self.log.msg("Initializing new "+self.collection_type[type] +" collection")
        self.type=type
        #if len(self.path.keys()) == 0:
        #    print "No collection paths defined, user collection.add() to add them."
    def add_path(self, path):
        self.path.append(path)

    def status(self):
        stat=("Nr of path's in collection "+self.collection_type[self.type] + " : " +str(len(self.path))+"\n")
        stat+=("Nr of files in collection "+self.collection_type[self.type] + " : " +str(len(self.files))+"\n")
        return(stat)

    def show(self):
        pass

    def collect_metadata(self):
        self.collection_index=Walk(self.path[0])
        print self.collection.items()

    def what_is(self, filename):
        return()

    def indexer_is_running(self):
        pass
