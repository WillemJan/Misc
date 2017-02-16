#!/usr/bin/env python2.6
import re, string, os, ast, urllib
from pprint import pprint
from xml.etree import ElementTree as etree

def post_url(url,data):
    headers = {"Content-type" : "text/xml; charset=utf-8", "Accept": "text/plain"}
    conn = http.client.HTTPConnection("localhost:8080")
    conn.request("POST","/solr/update/", bytes(data.encode('utf-8')), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return()

def get_serie_info(name):
    try:
        file=open("/tmp/"+name.replace(" ", "_")+".xml", "r")
        data=file.read()
        file.close()
        data=etree.fromstring(data)
    except:
        try:
            data=urllib.urlopen("http://www.thetvdb.com/api/GetSeries.php?seriesname="+urllib.quote(name)).read()
            data=("\n".join(data.split("\n")[1:])).lower()
            file=open("/tmp/"+name.replace(" ", "_")+".xml", "w")
            file.write(data)
            file.close()
            data=etree.fromstring(data)
        except:
            data=""
    odata=[]
    name=True
    for item in data.getiterator():
        if len(item.text) >1:
            tagname=item.tag
            et = etree.Element("field",  name="serie_"+tagname)
            if tagname == "seriesname" and name and len(item.text) > 1:
                et.text = item.text
                name=False
                odata.append(etree.tostring(et))
                print(item.text)
            else:
                if not tagname == "seriesname":
                    et.text = item.text
                    odata.append(etree.tostring(et))
    return(odata)

media = {}
wierd = ("/" , ".", "-")
regexlist = ('(\d+)e(\d+)', '(\d+)x(\d+)' , '(\d+)\s(\d+)')
i=j=0

config={}
config['seriename_parse'] = [
    re.compile('''^.+?Season\s([0-9]+?).+?Episode\s([0-9]+?)\]?[^\\/]*$'''),
    re.compile('''^.+?[ \._\-]\[[Ss]([0-9]+?)\]_\[[Ee]([0-9]+?)\]?[^\\/]*$'''),
    re.compile('''^.+?[ \._\-]\[?([0-9]+)[xX]([0-9]+)[^\\/]*$'''),
    re.compile('''^.+?([0-9]+)of([0-9]+).+$'''),
    re.compile('''^.+?([0-9]+)[xX]([0-9]+).+$'''),
    re.compile('''^.+?[ \._\-][Ss]([0-9]+)[\.\- ]?[Ee]([0-9]+)[^\\/]*$'''),
    re.compile('''^.+?[ \._\-]([0-9]{1})([0-9]{2})[\._ -][^\\/]*$'''),
    re.compile('''^.+?[ \._\-]([0-9]{2})([0-9]{2,3})[\._ -][^\\/]*$'''),
]

config['magic_parse'] = [
    re.compile('''^.+?(AVI).*$'''),
    re.compile('''^.+?(Matroska).*$'''),
    re.compile('''^.+?(ISO Media, MPEG v4 system, version).*$'''),
]


try:
    f=open("all", "r")
except:
    data=os.popen("find . -exec file '{}' ';' | grep -vi derren > all").read()
    f=open("all", "r")
record=[]
record.append("<add>\n")

list=[]

fn=open("all.new", "r")
shows={}
list=[]
for line in fn:
    list.append(line.lower().split("|")[0].split('(')[0].replace("\n", "").strip())
    shows[line.lower().split("|")[0].split('(')[0].replace("\n", "").strip()]=line.split("|")[-1]

fn.close()

list=[]
shows1={}

for item in shows.keys():
    item=item.lower().strip()
    if len(item) > 1:
        whole=""
        for part in item.split(" "):
            if part.strip()[0].isalpha():
                if len(part)>1:
                    whole+=" "+part.replace(".", " ").strip()
    shows1[whole]=shows[item]
shows={}
 
for line in f:
    line=line.strip()
    magic=":".join(line.split(":")[1:])
    for r in config['magic_parse']:
        match = r.match(magic)
        if match:
            item=line.split(":")[0].split("/")[-1]
            item=".".join(item.lower().strip().split(".")[0:-1])
            if len(item) > 1:
                whole=""
                o=0
                for part in item.split(" "):
                    if part.strip()[0].isalpha():
                        if len(part)>1:
                            whole+=" "+part.replace(".", " ").strip()
                if len(whole)>3:
                    shows[whole]=line
for item in shows.keys():
    for r in config['seriename_parse']:
        if r.match(item):
            new=item[0:item.find(r.match(item).group(1))-1]
            print(item, new, r.match(item).group(2))
