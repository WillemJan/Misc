#!/usr/bin/env python
import os, threading, fnmatch, hashlib, sys, os.path, subprocess
import magic


class Analyze:
    def __init__(self, directory, pattern="*"):
        self.ms = magic.open(magic.MAGIC_NONE)
        self.ms.load()
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
                try:
                    self.files = os.listdir(self.directory) 
                except:
                    pass
                self.index = 0
            else:
                fullname = os.path.join(self.directory, file)
                if os.path.isdir(fullname) and not os.path.islink(fullname):
                    self.stack.append(fullname)
                if fnmatch.fnmatch(file, self.pattern) and not os.path.isdir(fullname):
                    fullname=os.path.abspath(fullname)
                    if not fullname.find("'") > -1:
                        fullname="'"+fullname+"'"
                    else:
                        fullname='"'+fullname+'"'

                    print(fullname)
                    type =  self.ms.file(fullname)
                    f = file(fullname, "r")
                    buffer = f.read(4096)
                    f.close()

                    type = ms.buffer(buffer)
                    print (type)
                    self.ms.close()
                
                     

#                    hash=hashlib.md5(str(fullname.encode('ascii', 'replace').decode('ascii'))).hexdigest()
#                    self.list[hash]=(fstat.st_size, fullname)



class Artifacts:
    def __init__(self):
        print ("Artifacts initialized")
        if len(sys.argv) == 2:
            walk = Analyze(sys.argv[1])
        pass

if __name__ == "__main__":
    artifacts=Artifacts()
