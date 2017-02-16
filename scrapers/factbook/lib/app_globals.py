import webhelpers.constants as c
import os.path
import urllib2
from pprint import pprint
import magickpy
from home.model import get_db, Factsheet
import couchdb



"""The application's Globals object"""
#http://dev.gafol.net/t/magickpy
"""
{
   "by_code": {
       "map": "function (doc) {emit(doc.name, doc);}"
   }
}
"""

BASEURL="http://localhost:5000"

#CIA_FACTBOOK_URL="https://www.cia.gov/library/publications/the-world-factbook/index.html"
CIA_BASE="https://www.cia.gov/library/publications/the-world-factbook/geos/"
CIA_FACTBOOK_URL=os.getcwd()+"/home/public/facts.html"

FLAG_URL="/country_flags/"
FLAG_DIR=os.getcwd()+"/home/public"+FLAG_URL

class URLgrab(object):
    def __init__(self):
        pass
    def url(self, url):
        try:
            response=urllib2.urlopen(url)
        except urllib2.HTTPError, err:
            print(err)
            return(False)
        return(response.read())

    def pop(self, code):
        #l=(CIA_BASE+code+".html") 
        f=self.url(url).encode("utf-8")
        go=False
        for l in f.split("\n"):
            if (go):
                i=0
                l=l.strip("\n")
                l=l.strip()
                if len(l)>1:
                    if not l.startswith("<"):
                        l=l.split(" ")[0]
                        break
                if (l.find('</td>') > -1) and (i>1):
                    go=False
            if (l.find('<div align="right">Population:</div>') > -1):
                go=True
        return(l)

class Globals(object):
    __grab__ = URLgrab()
    """Globals acts as a container for objects available throughout the
    life of the application

    """
    factbook={}
    flags={}

    def __init__(self):
        if (CIA_FACTBOOK_URL.startswith("https://")):
            cia_factbook_data = (self.__grab__.url(CIA_FACTBOOK_URL))
        else:
            try:
                cia_factbook_data=open(CIA_FACTBOOK_URL, "r").read()
            except:
                cia_factbook_data=False
        
        if (cia_factbook_data):
            for line in cia_factbook_data.split("\n"):
                if (line.find("<option value=\"geos/") > -1):
                    line="".join(line.split("/")[1:])
                    country_code=line.split(".")[0].upper()
                    country_name=line.split(">")[1].split("<")[0]
                    self.factbook[country_code]={}
                    self.factbook[country_code]["image"]= BASEURL+FLAG_URL+country_code.lower()+".gif"
                    self.factbook[country_code]["fullname"] = country_name

        country_list=[]
        for code in self.factbook.keys():
            if not (os.path.isfile(FLAG_DIR+code.lower()+".gif")):
                if CIA_FACTBOOK_URL.startswith("https://"):
                    self.__getff__(code.lower())
            country_list.append( (self.factbook[code]["fullname"], code))
        docs=[]
        db=get_db()
        for (name,code) in sorted(country_list):
            flag_url=(BASEURL+FLAG_URL+code.lower()+".gif")
            sheet_url = (CIA_BASE+code.lower()+".html") 
        
            try:
                sheet_data = self.__grab__.url(sheet_url)
            except:
                sheet_data = "none"
            print(sheet_url)
            docs.append( {'_id' : code, 'name': name, 'flag_img' : flag_url, 'sheet_data' : sheet_data.encode("utf-8")} )
            db.update(docs)
        pass
   
    def __getff__(self, country_code):
                    url="https://www.cia.gov/library/publications/the-world-factbook/flags/"+country_code.lower()+"-flag.gif"
                    flag=(self.__grab__.url(url))
                    if (flag):
                        file=open(FLAG_DIR+country_code.lower()+".gif", "wb")
                        file.write(flag)
                        file.close()
