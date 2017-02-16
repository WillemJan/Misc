#!/usr/bin/python3

import os, subprocess, codecs, hashlib

from urllib import request, error
from urllib.parse import quote_plus

class Harvest():
    files = {}
    dir_count=0
    file_count=0

    def __init__(self):
        for file in files.read():
            if (file.find('"') > -1):
                file="'"+file+"'"
                self.files[file]="ok"
            elif (file.find("'") > -1):
                file='"'+file+'"'
                self.files[file]="ok"
            else:
                file="'"+file+"'"
                self.files[file]="ok"
            if (file.split('/')[-1].find('.') > -1):
                self.file_count+=1
            else:
                p1=subprocess. Popen("/usr/bin/file " +file,shell=True, stdout=subprocess.PIPE)
                file_info=(str(p1.communicate()[0].strip()))
                if not ( (file_info.rsplit(':')[-1][1:-1]) == "directory") :
                    print(file,file_info) 
                self.dir_count+=1


if __name__ == "__main__":
    harvest = Harvest()
    print (harvest.dir_count)
    print (harvest.file_count)
#        i+=1
#        for key in harvest.known_file_extentions.keys():
#            if item[1:-1].endswith(key):
#                p1=subprocess. Popen("/usr/bin/file " +item ,shell=True, stdout=subprocess.PIPE)
#                curr_file=str(p1.communicate()[0].strip())
#                for ftype in harvest.ftype.keys():
#                    if ( curr_file.lower().find(ftype) > -1 ):
#                        print (item, harvest.ftype[ftype](item, curr_file))
#                        j+=1
#                        break
#            else:
#                if (item.split('/')[-1].find('.') < 0):
#                    j+=1
#                    break
#                else:
#                    print(item)
#        if i>10:
#            print(i,j)
##            break
#    for artist in sorted(harvest.artist.keys()):
#        print(artist)
#        print(harvest.get_wiki_reference(str(artist)))
