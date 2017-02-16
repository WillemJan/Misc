#!/usr/bin/env python

from pprint import pprint
import sys
import urllib
from BeautifulSoup import BeautifulSoup
import xml, ast



def get_element(seriename):
    print(seriename)
    seriename=urllib.quote(seriename)
    try:
        file=open("/tmp/"+seriename+".wiki", "r")
        data=file.read()
        file.close()
    except:
        data=urllib.urlopen("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles="+seriename+"%20%28TV%20series%29&rvprop=content&format=json").read()
        file=open("/tmp/"+seriename+".wiki", "w")
        file.write(data)
        file.close()

    known_items=["format", "creator", "first_aired", "starring"]

    list={}
    data=ast.literal_eval(data)
    for name in known_items:
        key=data['query']['pages'].keys()[0]
        for line in data['query']['pages'][key]['revisions'][0]['*'].split('\n'):
            if line.startswith("|"):
                nline=line.split("=")[0].replace("|","").strip()
                if nline.startswith(name):
                    line=line.split("=")[1].strip()
                    for item in line.split("[["):
                        line=(item.replace("]]", "")).strip()
                        line=line.replace("<br \\/>", "")
                        line=line.replace(" with", "")
                        line=line.replace(" and", "")
                        line=line.replace("\\/", "/")
                        if len(line)>1:
                            try:
                                list[name].append(line)
                            except:
                                list[name]=[]
                                list[name].append(line)
                            #.encode('utf-8','xmlcharrefreplace'))
    return(list)

#print(sys.argv[1])
pprint(get_element(sys.argv[1].replace("-"," ")))



#opener = urllib2.build_opener()
#opener.addheaders = [('User-agent', 'Mozilla/5.0')]
#infile = opener.open('http://en.wikipedia.org/w/api.php?action=query&prop=extlinks&titles=Weeds_%28TV_series%29')
#page = infile.read()
#print(page)

