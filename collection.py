#!/usr/bin/env python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.001"

try:
    import os, sys, magic, fnmatch, hashlib, threading, twill, urllib2, re, pickle, urllib
    from cStringIO import StringIO
    from xml.sax.saxutils import unescape
    from BeautifulSoup import BeautifulSoup
    from pprint import pprint

except:
    import os, sys
    print sys.argv[0][2:-3]+"-manager v"+__version__
    print "Failed to load essential modules, see README.txt"
    os._exit(-1)


class ShowList(object):
    def __init__(self):
        show_list = {
            
                     'http://www.imdb.com/title/tt0092379/episodes' : 'Inspector Morse',
                    'http://www.imdb.com/company/co0043801/'       : 'ShadowMachine',              
                     'http://www.imdb.com/company/co0043107/'       : 'BBC',
                     'http://www.imdb.com/company/co0135632/'       : 'Talkback Thames', 
                     'http://www.imdb.com/company/co0056555/'       : 'National Geogrpahic',
                     'http://www.imdb.com/company/co0139461/'       : 'National Geogrpahic',
                     'http://www.imdb.com/company/co0056447/'       : '20th Century Fox',
                     'http://www.imdb.com/company/co0103957/'       : 'BBC Worldwide',
                     'http://www.imdb.com/title/tt0318224/episodes' : 'BBC Horizon',
                     'http://www.imdb.com/title/tt0237123/episodes' : 'Coupling', 
                     'http://www.imdb.com/company/co0005861/'       : 'Home Box Office',
                     'http://www.imdb.com/company/co0209226/'       : 'ABC Studios',
                     'http://www.imdb.com/company/co0086397/'       : 'Sony Pictures', 
                     'http://www.imdb.com/company/co0073776/'       : 'Box TV [gb]', 
                     'http://www.imdb.com/company/co0007979/'       : 'Network Ten [au]',
                     'http://www.imdb.com/company/co0194193/'       : 'Flight 33 Productions',  
                     'http://www.imdb.com/company/co0231723/'       : 'Canvas Televisie [be]'
                     }
        self.list=[]
        self.items={}
        print "# showlist_init"
        for show in show_list.keys():
            self.get_showlist(show, show_list[show])
        for item in self.items.keys():
            print(item)

    def check(self, name):
        name=name.lower()
        tmp=""
        le=1000

        print "# showlist_lookup :", name

        for item in self.items.keys():
            if item.lower().find(name) > -1:
                if (len(item) == len(name)):
                    return(self.items[item])
                else:
                    if len(tmp)>4:
                        tmp=item
            word=""
            i=0

            for part in name.split(" "):
                if len(part) > 4:
                    word+=part+" "
                    i+=1
                    if i>1:
                        break

            if item.lower().find(word) > -1:
                if (len(item) == len(word)):
                    return(self.items[item])
                else:
                    if len(tmp)>4:
                        tmp=item
        if (len(tmp) > 5):
            return(self.items[tmp])



        print "# showlist_done :", name

        return(False)

    def get_and_cache(self, url):
        try:
            path = "/tmp/prutsgood_showlist.pickle."+hashlib.md5(url).hexdigest()
            input = open(path, 'rb')
            data = pickle.load(input)
            input.close()
        except:
            print(url)
            data = urllib2.urlopen(url).read()
            path = "/tmp/prutsgood_showlist.pickle."+hashlib.md5(url).hexdigest()
            output = open(path, 'wb')
            pickle.dump(data, output)
        return(data)

    def get_showlist(self, url, company):
        soep=BeautifulSoup(self.get_and_cache(url))
        links=soep.findAll('li')
        i=0
        #print "##",  i, url
        try:
            for l in links:
                title=l.contents[0].attrs[0][1].encode()
                if (title.startswith('/title/tt') and title.endswith('/')):
                    year=l.contents[1].split('(')[1].split(')')[0].encode('ascii')[:4]
                    name=unescape(l.contents[0].contents[0].decode(), {"&#x26;" : '&', "&#x27;" : "'"  , '&#x22;' : ''}).split(' (')[0].encode('ascii', 'replace')
                    if len(name) > 2:
                        if name.endswith(':'):
                            name=name[0:-1]
                        if name.find('(') > -1:
                            name=name[0:name.find('(')]
                        if len(name) > 1:
                            self.items[name]=[title,year,company]
                        i+=1
        except:
            pass
        try:
            soep=BeautifulSoup(self.get_and_cache(url))
            links=soep.findAll('a')

            for l in links:
                title=l.attrs[0][1].encode('ascii')
                if (title.startswith('/title/tt') and title.endswith('/')):
                    name=unescape(l.contents[0].encode(), {"&#x26;" : '&', "&#x27;" : "'"  , '&#x22;' : ''})
                    if len(name) > 2:
                        year="####"
                        if name.endswith(':'):
                            name=name[0:-1]
                        if name.find('(') > -1:
                            name=name[0:name.find('(')]
                        if len(name) > 1:
                            self.items[name]=[title,year,company]
                        i+=1
        except:
            pass
        #print "##",  i, url


class Imdb(object):

    name=False
    show_list = {}


    def __init__(self, name):
        print "IMDB"
        self.name=name
        self.year=False
        self.eps=False
        for item in self.show_list.keys():
             print item
        print(name)
        known={}

    def imdb_lookup(self):
        imdb = twill.commands
        out= StringIO()
        twill.set_output(out)
        res=imdb.go("http://www.imdb.com/find?s=all&q=")
        res=imdb.formvalue(1,"q",self.new_name)
        res=imdb.tidy_ok()
        res=imdb.submit(0)
        data=(imdb.get_browser().get_html())
        out = open('tmp', 'w')
        i=0
        for line in data.split('\n'):
            if len(line.strip()) > 1:
                out.write(line.strip()+'\n')
                if line.find('/title/tt') > -1:
                    if i<10:
                        i+=1
                        soup=BeautifulSoup(line)
                        imdb_name=soup.findAll('a')[0]
                        try:
                            return(unescape(imdb_name.contents.decode(), {"&#x26;" : '&', "&#x27;" : "'"  , '&#x22;' : ''} ))
                        except:
                            pass
                        soup=BeautifulSoup(line)
                        imdb_name=soup.findAll('td')
                        try:
                            return(unescape(imdb_name.contents, {"&#x26;" : '&', "&#x27;" : "'"  , '&#x22;' : ''} ))
                        except:
                            return(False)
        out.close()

    def wiki_lookup(self):
        wiki = twill.commands
        out= StringIO()
        twill.set_output(out)
        res=wiki.go('http://en.wikipedia.org/wiki/Main_Page')
        res=wiki.formvalue(1,"searchInput",self.name)
        res=wiki.tidy_ok()
        res=wiki.submit(0)
        data=(wiki.get_browser().get_html())

        out = open('tmp', 'a')
        i=0
        go=False
        for line in data.split('\n'):
            soep=BeautifulSoup(line)
            for line in soep.popTag():
                try:
                    for div in line.findAll('div').pop():
                        if (div.encode().strip().startswith('may refer to:')):
                            desc=str(line.findAll('div')[0]).split('>')[13].split('<')[0].strip()
                            link=str(line.findAll('a')[0]).replace('/wiki/', 'http://en.wikipedia.org/wiki/')
                            return(desc, link)
                except:
                    pass
        return(False)
        
    def correct_filename(self, name):
        old_name = name

        name1=""
        eps=False
        year=False

        if name.lower().find('lectures') > -1:
            return(['lecture'],year,eps)

        if name.lower().find('sample') > -1:
            return(['sample'],year,eps)

        if name.find('.avi') > -1:
            name=name[0:name.lower().find('.avi')]
        name=name.replace('*', '')

        for year in range(1800,2030):
            year=str(year)
            if (old_name.lower().find(year) > -1):
                name=name.replace(year, "")
                break
            year=False

        tname=name.replace('.',' ')    
        try:
            eps=re.search('(\s*s\d+\s*e\s*\d+\s*)', tname.lower()).group(0)
            name1=name[name.lower().find(eps)+len(eps):len(name)].replace("-","").strip()
            name=name[0:name.lower().find(eps)].strip()
        except:
            pass

        if not eps:
            try:
                eps=re.search('(\s+Season\s*\d+\s*)', tname.lower()).group(0)
                name1=name[name.lower().find(eps)+len(eps):len(name)].replace("-","").strip()
                name=name[0:name.lower().find(eps)].strip()
            except:
                pass


        if not eps:
            try:
                eps=re.search('(\s*s\d+\s*ep\s*\d+\s*)', tname.lower()).group(0)
                name1=name[name.lower().find(eps)+len(eps):len(name)].replace("-","").strip()
                name=name[0:name.lower().find(eps)].strip()
            except:
                pass


        if not eps:
            try:
                eps=re.search('(\s*s\d+\s*)', tname.lower()).group(0)
                name1=name[name.lower().find(eps)+len(eps):len(name)].replace("-","").strip()
                name=name[0:name.lower().find(eps)].strip()
            except:
                pass


        if not eps:
            try:
                eps=re.search('(\s*e\d+\s*)', tname.lower()).group(0)
                name1=name[name.lower().find(eps)+len(eps):len(name)].replace("-","").strip()
                name=name[0:name.lower().find(eps)].strip()
            except:
                pass

        if not eps:
            try:
                eps=re.search('(\s*\d+\s*x\s*\d+\s*)', tname.lower()).group(0)
                name1=name[name.lower().find(eps)+len(eps):len(name)].replace("-","").strip()
                name=name[0:name.lower().find(eps)].strip()
            except:
                pass


        if not eps:
            try:
                eps=re.search('(\s*\d+\s*of\s*\d+\s*)', tname.lower()).group(0)
                name1=name[name.lower().find(eps)+len(eps):len(name)].replace("-","").strip()
                name=name[0:name.lower().find(eps)]
            except:
                pass
        if eps: 
            name=name.lower().replace(eps," ").strip()
            name1=name1.lower().replace(eps," ").strip()

        name2=""

        if name.find('..') > -1:
            if name.find('..') > 4:
                if len(name1) > 1:
                    name2=name[0:name.find('..')]
                else:
                    name1=name.replace('..', ' ')
            else:
                name=name.replace('..', ' ')

        if name.find("&") > -1:
            if len(name1) > 1:
                name=name[0:name.find("&")]
                name2=name[name.find("&")+1:len(name)]
            else:
                name=name[0:name.find("&")]
                name1=name[name.find("&")+1:len(name)]

        name=name.replace('-', ' ') .strip()
        name=name.replace('_', ' ') .strip()
        name=name.replace('.', ' ') .strip()
        name=name.replace('   ', ' ').strip()
        name=name.replace('  ', ' ').strip()

        done=False
        found=False

        while not done:
            for item in ('()[]._-1234567890'):
                if name.endswith(item):
                    name=name[0:-1]
                    found=True
                elif name.startswith(item):
                    name=name[1:]
                    found=True
                else:
                    done=True
            if found:
                done=False            
                found=False

        '''
        if eps:
            if show:
                show="http://www.imdb.com"+show[0]+" "+show[1]
                print "#", name, " Y:"+ str(year), " E:"+ str(eps), str(show), str(self.show_list[name])
            else:
                print "#", name, " Y:"+ str(year), str(eps)
        else:
            if year and show:
                print "#", name, " Y:"+ str(year), "http://www.imdb.com"+show[0]+" "+show[1]
            elif year:
                print "#", name, " Y:"+str(year)
            else:
                print "#"
        '''
        return((name, name1, name2),year,eps)

    
class Walk(object):
    def __init__(self, directory, pattern = "*"):
        self.stack = [directory]
        self.pattern = pattern
        self.files = []
        self.index = 0
        self.error = 0
        self.list = {}
        self.names = []
        self.i=0
        self.minlen = 1000
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
                if fnmatch.fnmatch(file, self.pattern):
                    name=os.path.realpath(fullname)
                    if ( len(name.split('/'))  < self.minlen):
                        self.minlen=len(name.split('/'))
                    self.names.append(name)

class CouchDB(object):

    def __init__(self, couch_name="prutsgood_files"):
        self.couch_name = couch_name
        self.conn = self.get_db()

    def get_db(self):
        COUCH_BASEURL = "http://127.0.0.1:5984/"
        server=Server(COUCH_BASEURL)
        if self.couch_name not in server:
            conn=server.create(self.couch_name)
        else:
            conn = server[self.couch_name]
        return(conn)  

class Analyze(object):
    hashlist={}

    def __init__(self, walk, db):
        self.ms = magic.open(magic.MAGIC_NONE)
        self.ms.load()
        self.walk=walk

        #self.db=db
        #self.path()

    def magic_info(self, filename): 
        return(self.ms.file(filename))

    def path(self):
        indb=0
        tot_file=0
        tot_video=0
        for i in range(len(self.walk.names)):
            filename=self.walk.names[i]
            try:
                file=open(filename, "rb")
                data=file.read(65536)
                hash=hashlib.md5(data).hexdigest()
                file.close()
            except:
                hash=hashlib.md5(filename).hexdigest()

            hash1=hashlib.md5(filename).hexdigest()
            hash=hashlib.md5(hash+hash1).hexdigest()

            try:
                print self.db.conn[hash].values()
            except client.ResourceNotFound as e:
                try:
                    magic=self.magic_info(filename)
                    if (magic.find('video') > -1):
                        print str(i)+" "+hash+" : "+filename
                        #try:
                        #    data={"_id" : hash, "filename" : urllib2.quote(filename), "magic" : magic, "wiki_data" : "wiki_data" }
                        #    self.db.conn.update([data]).close()
                        #except:
                        #    print "Wierd" + filename
                        #    pass
                except client.PreconditionFailed as e:
                    print(e)


class Collection(object):
    __usage__ = "PrutsGood-"+sys.argv[0][2:-3]+"-manager v"+__version__+"""

Usage : collection [add [path]] [stats] [version]
                    add 'add files to collection' 
                    delete 'delete files from collection'
                    stats'shows stat about scollection'
                    version 'shows version and exit'

Available collection_types:
    Books 'E-books, PDF documents, ect'
    Films 'Moving images'
    Music 'Audio, Sound'
    Mixed 'Mixed content, files will not be put in to any catagory, can be fixed later.
    """

    def __init__(self):
        #self.analyze = None
        #self.db = CouchDB()
        #self.artifacts = Artifacts(CouchDB("prutsgood_artifacts"))

        if len(sys.argv) < 2:
            print (self.__usage__)
            os._exit(-1)

        if len(sys.argv) == 2:
            if (sys.argv[1] == "stats"):
                print "Total files/dirs in collection : "+ str(self.db.conn.info()['doc_count'])
                os._exit(-1)

            print (self.__usage__)
            print ("\nPath not valid : " + sys.argv[1]+"\n")
            os._exit(-1)
            
        if sys.argv[1] == 'add':
            try:
                print("#!/bin/bash")
                print(os.stat(os.path.realpath(sys.argv[2])))
            except:
                print (self.__usage__)
                print ("\nPath not valid : " + sys.argv[2]+"\n")
                os._exit(-1)
            
            self.walk = Walk(os.path.realpath(sys.argv[2]))
            #serie=ShowList()
            print sys.argv[2]
            for item in range(0, len(self.walk.names)):
                self.walk.names[item]=self.walk.names[item].split('/')[self.walk.minlen-1:]
                if self.walk.names[item][0].find('serie') > -1:
                    name=self.walk.names[item][1:]
                    if len(name) == 1:
                        for item in name:
                            serie_name=(item.replace('-', ' '))
                        print serie_name
                        print urllib2.urlopen('http://www.google.nl/search?q="episode+list+for"+'+urllib.quote_plus(serie_name)).read()
            
            #self.analyze= Analyze(self.walk, self.db)
            #except:
            #    print (self.__usage__)
            #    print ("\nPath not valid : " + sys.argv[2]+"\n")
            #    os._exit(-1)
            
if __name__ == "__main__":
    collection = ShowList()


'''
class WorkingThread(threading.Thread):
"""
Thread that performs the copy operation for one machine
"""
def __init__(self, machine, orig_file, orig_md5):
threading.Thread.__init__(self)

self.machine = machine
self.file = orig_file
self.orig_md5 = orig_md5
self.handle = PySTAF.STAFHandle("%s:%s" % (__file__, self.getName()))

def run(self):
# Copy file to remote machine
copy_file(self.handle, self.file, self.machine)

# Calculate md5 sum of the file copied at the remote machine
dest_md5 = run_process_command(self.handle, self.machine, "md5sum /tmp/%s" 
% os.path.basename(self.file)).split()[0]
assert self.orig_md5 == dest_md5
self.handle.unregister()
'''
