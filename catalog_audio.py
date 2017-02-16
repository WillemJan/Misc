#!/usr/bin/env python2.6
import re, string, os, ast, urllib
import tvdb.tvdb_api as tvdb_api
import time, hashlib
from pprint import pprint, pformat
from xml.etree import ElementTree as etree




try:
    f=open("books.txt", "r")
    data=f.read()
    f.close()
except:
    data=os.popen("find /shared_stuff/books/ -name '.bookinfo' -exec echo {} \; -exec cat {} \;").read()
    f=open("books.txt", "w")
    f.write(data)
    f.close()

LOC_BASEURL = "http://z3950.loc.gov:7090/voyager"
LOC_PARAM   = "&startRecord=1&maximumRecords=1&recordSchema=dc&version=1.1&operation=searchRetrieve"
BL_BASEURL  = "http://herbie.bl.uk:9080/cgi-bin/blils.cgi?query="

def lookup_artist(artist, album):

    #url="http://ws.audioscrobbler.com/2.0/?method=artist.search&artist="+artist+"&api_key=b25b959554ed76058ac220b7b2e0a026format=json"
    artist=urllib.quote(artist)
    album=urllib.quote(album)
    url="http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist="+artist+"&api_key=b25b959554ed76058ac220b7b2e0a026&format=json"
    data=ast.literal_eval(urllib.urlopen(url).read())
    record=[]
    for item in data['artist']['bio']:
        for i in data['artist']['bio'][item].split("href="):
            print("href="+i+"\n")
    print("".join(record))
                


    url="http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=b25b959554ed76058ac220b7b2e0a026&artist="+artist+"&album="+album+"&format=json"
    data=ast.literal_eval(urllib.urlopen(url).read())
    pprint(data)
    
    '''
    try:
        file=open("/tmp/books/"+isbn, "r")
        data=file.read()
        file.close()
        try:
            data=etree.fromstring(data)
        except:
            pass
    except:
        try:
            data=urllib.urlopen(url).read()
            time.sleep(1.2)
            file=open("/tmp/books/"+isbn, "w")
            file.write(data)
            file.close()
            try:
                data=etree.fromstring(data)
            except:
                pass
        except:
            time.sleep(25*5)
            try:
                data=urllib.urlopen(url).read()
                file=open("/tmp/books/"+isbn, "w")
                file.write(data)
                file.close()
            except:
                pass
    return(data) 
    '''


lookup_artist("The Fiery Furnaces", "I'm Going Away")


'''
books={}
count=0

for line in data.split("\n"):
    if line.startswith("/shared_stuff/"):
        filename = line.replace("/shared_stuff/books/", "")
        if not (filename.startswith("no")):

            if len(books.keys()) > 0:
                print("<doc>\n")
                for item in (books[books.keys()[0]].keys()):
                    if (type(books[books.keys()[0]][item]) == type("")):
                        et = etree.Element("field",  name=item)
                        et.text = books[books.keys()[0]][item]
                        print(etree.tostring(et))
                    else:
                        for val in books[books.keys()[0]][item]:
                            et = etree.Element("field",  name=item)
                            et.text = val
                            print(etree.tostring(et))
                et = etree.Element("field",  name="media_type")
                et.text = "book"
                print(etree.tostring(et))

                et = etree.Element("field",  name="filename")
                et.text = books.keys()[0]
                print(etree.tostring(et))
                print("</doc>\n\n")

            books={}
            books[filename]={}
            count+=1
    else:
        if not  (filename.startswith("no")):
            if line.split(":")[0] == "image_url":
                for item in "".join(line.split(":")[1:]).split(","):
                    if len(item)>0:
                        name=hashlib.md5(item.strip()).hexdigest()
                        url="".join(item).strip()
                        url="http://"+url.split("//")[1]
                        try:
                            file=open("/home/aloha/prutsgood/data/books/covers/"+name+"."+url.split(".")[-1], "r")
                            file.close()
                            books[filename]["imgurl"]=name+"."+url.split(".")[-1]
                        except:
                            try:
                                data=urllib.urlopen(url).read()
                            except:
                                data="f"
                                pass
                            if len(data)>1:
                                file=open("/home/aloha/prutsgood/data/books/covers/"+name+"."+url.split(".")[-1], "w")
                                books[filename]["imgurl"]=name+"."+url.split(".")[-1]
                                file.write(data)
                                file.close()
                            if data=="f":
                                file=open("/home/aloha/prutsgood/data/books/covers/"+name+"."+url.split(".")[-1], "w")
                                file.write("fail")
                                file.close()

            if line.split(":")[0] == "rating":
                books[filename]["rating"]="".join(line.split(":")[1:]).strip()
            if line.split(":")[0] == "review":
                books[filename]["review"]="".join(line.split(":")[1:]).strip()
            if line.split(":")[0] == "title":
                title="".join(line.split(":")[1:]).strip()
                books[filename]["title"]=title
            if line.split(":")[0] == "isbn":
                data=lookup_isbn(line.split(":")[1].strip())
                books[filename]["isbn"]=line.split(":")[1].strip()
                if data:
                    for e in data.getiterator():
                        if e.tag.split("}")[1] == "creator":
                            try:
                                books[filename]["creator"].append(e.text.strip())
                            except:
                                books[filename]["creator"]=[]
                                books[filename]["creator"].append(e.text.strip())
                        if e.tag.split("}")[1] == "title":
                            books[filename]["title"]=e.text[0:-2].strip()
'''
