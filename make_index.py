#!/usr/bin/python
"""The application's Globals object"""
import os, os.path, pickle, subprocess, hashlib, gzip, stat
from urllib2 import *

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """

    EBOOK_DIR="/shared_stuff/books/"
    ebook_files = {}

    print "Making new index file"

    directories = [EBOOK_DIR]
    count=0

    while len(directories)>0:
        directory = directories.pop()
        for name in os.listdir(directory):
            fullpath = os.path.join(directory,name)

            if os.path.isfile(fullpath):
                path=fullpath
                if fullpath.find("'") > -1:
                    p1=subprocess. Popen("/usr/bin/file" + (' "'+path+'" 2>/dev/null'),shell=True, stdout=subprocess.PIPE)
                else:
                    p1=subprocess. Popen("/usr/bin/file" + (" '"+path+"' 2>/dev/null"),shell=True, stdout=subprocess.PIPE)
                p2=subprocess.Popen("cut" + " -d ':' -f 2- ", stdin=p1.stdout,shell=True, stdout=subprocess.PIPE)
                type=p2.communicate()[0].strip()

                if type.lower().find("jpeg") > -1:
                    p1=subprocess. Popen("/usr/bin/identify" + (" \""+fullpath.replace('"','\"')+"\" 2>/dev/null"),shell=True, stdout=subprocess.PIPE)
                    type=p1.communicate()[0].strip()
                    type=type.replace(fullpath,"")

                sum=hashlib.md5(fullpath).hexdigest()

                f=open(fullpath)
                sum1=hashlib.md5(f.read()).hexdigest()
                f.close()

                size=os.stat(fullpath).st_size

                ebook_files[sum] = ({"path" : fullpath.replace(EBOOK_DIR,"/"), "type" : type, "sum" : sum1, "size" : size })

                count+=1
                if (count%2 == 0):
                    print count, ebook_files[sum]

            elif os.path.isdir(fullpath):
                directories.append(fullpath)  # It's a directory, store it.

    print "Index building done"

    output = gzip.GzipFile('/tmp/pruts_ebooks', 'wb')
    pickle.dump(ebook_files, output,  -1)
    output.close()

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the 'g'
        variable
        """
        pass
