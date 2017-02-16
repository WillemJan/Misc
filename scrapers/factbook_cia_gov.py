"""Factbook parser"""

import urllib2, couchdb
from couchdb import schema
from couchdb import Server


class URLgrab(object):
    def __init__(self):
        pass
    def url(self, url):
        try:
            response=urllib2.urlopen(url)
        except urllib2.HTTPError, err:
            print(err)
            return(False)
        return(str(unicode(response.read(), errors='ignore').encode("utf-8")))

class LoungeDataCouch(object):
    def __init__(self):
        self.db=self.get_db()
        pass
    def get_db(self):
        try:
            server=Server("http://127.0.0.1:5984/")
            if 'cia_factbook' not in server:
                server.create('cia_factbook')
            db = server['cia_factbook']
        except:
            print ("DB_ERROR")
            os._exit(-1)
        return(db)
        

class FactBook(object):
    baseurl="https://www.cia.gov/library/publications/the-world-factbook/geos/"
    tmp_dir="/tmp/facts/"

    def __init__(self,grab,db):
        self.grab=grab
        for name,code in self._parse_factbook_country_index():
            docs=[]
            docs.append(self._parse_factbook_page(code))
            try:
                db.update(docs)
            except:
                pass
    def _parse_factbook_country_index(self):
        try:    
            file = open(self.tmp_dir+"xx","r")
            content=file.read()
            file.close()
        except:
            file = open(self.tmp_dir+"xx","w")
            content = self.grab(self.baseurl+"xx"+".html")
            file.write(content)
            file.close()

        list=[]
        for line in content.split("\n"):
            if (line.find("<option value=\"") > -1):
                line="".join(line.split("/")[0])   
                country_code=line.split("\"")[1].upper().replace(".HTML","")
                country_name=line.split(">")[1].split("<")[0]
                list.append((country_name,country_code))
                #self.factbook[country_code]["image"]= BASEURL+FLAG_URL+country_code.lower()+".gif"                
        return(list)

    def _parse_factbook_page(self,code):
        try:    
            file = open(self.tmp_dir+code.lower(),"r")
            content=file.read()
            file.close()
        except:
            file = open(self.tmp_dir+code.lower(),"w")
            content = self.grab(self.baseurl+code.lower()+".html")
            file.write(content)
            file.close()
        country_info=""
        go=False
        country_info=( {"_id" : code})
        for l in content.split("\n"):
            l=l.strip()
            if (l.find('<div align="right">') > -1):
                go=True
            else:
                if (l.find('<title>') > -1):
                    t=l.replace("<title>","")
                    t=t.replace("</title>","")
                    t=t.replace("\r","")
                    t="".join(t.split("-- ")[1:])
                    country_info["fullname"]= t
            if (len(l)>0):
                if (go):
                    if not l.startswith("<"):
                        try:
                            l=country_info[label]+" "+l
                        except:
                            pass
                        country_info[label]=l
                    else:
                        if l.startswith("<div align=\"right\">"):
                            label="".join(l.rsplit("<")[1].split(">")[1:]).lower().replace(":","")
                            label=label.replace("-","")
                            label=label.replace(" ","_")
                            label=label.replace("__","_")
        return(country_info)

grab=URLgrab()
data=LoungeDataCouch()
FactBook(grab.url, data.db)
