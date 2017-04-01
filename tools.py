#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import urllib
import simplejson
import feedparser
import operator
from django.utils.html import strip_tags

from pprint import pprint

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords

rep = u"’':'\":;"
words = {}
names = {}

urls = ("http://www.nu.nl/feeds/rss/algemeen.rss", "http://www.nrc.nl/nieuws/categorie/nieuws/rss.php", "http://www.volkskrant.nl/rss.xml","http://feeds.webwereld.nl/webwereld", "http://feeds.nos.nl/nosjournaal?format=xml","http://rss.fok.nl/feeds/nieuws","http://www.telegraaf.nl/rss/index.xml", "http://www.demorgen.be/rss.xml", "http://www.pzc.nl/?service=rss", "http://feeds.nieuwsblad.be/nieuws/snelnieuws?format=xml", "http://www.spitsnieuws.nl/rss/all/rss.xml", "http://www.nieuws.nl/rss/algemeen", "http://feeds.bbci.co.uk/news/rss.xml")

'''
class cache_feed(object):
    def __init__(self, url, cache_time=60, cache_path="/tmp/news", cache_autodel=True):
        import hashlib
        self.cache_filename=cache_path+os.sep+hashlib.md5(url).hexdigest()
        if not os.path.isfile(cache_filename):
            print("No cache for %s, getting fresh data" % url)
            self.get_update(url)
        else:
            import os.path, time
            print "last modified: %s" % time.ctime(os.path.getmtime(file))
            print "created: %s" % time.ctime(os.path.getctime(file))


    def get_update(self, url):
        data = urllib.urlopen(url).read()
        with open(self.cache_filename,"rw") as fh:
            fh.write(data)

'''

for url in urls:
    data=urllib.urlopen(url).read()
    feed=feedparser.parse(data)
    stopwoorden = set(stopwords.words('dutch'))
    for w in ("novum", "jaar", "maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "jaar", "een", "twee", "drie", "vier", "hollandse", "nederlandse", "gaat", "dood", "meldt", "mensen", "jaar", "geld", "lees", "vandaag", "mannen", "vrouwen", "gaan", "week"):
        stopwoorden.add(w)
    for item in feed['entries']:
        title=unicode(strip_tags(item['summary']))
        for word in word_tokenize(title):
            if word.lower() not in stopwoorden:
                if len(word)>3:
                    if not word in words:
                        words[word]={}
                        words[word]["title"] = [title]
                        words[word]["count"] = 0
                    else:
                        words[word]["count"] += 1
                        words[word]["title"].append(title)

        title=unicode(item['title'])
        for word in word_tokenize(title):
            if word.lower() not in stopwoorden:
                if len(word)>3:
                    if not word in words:
                        words[word]={}
                        words[word]["title"] = [title]
                        words[word]["count"] = 1
                    else:
                        words[word]["count"] += 2
                        words[word]["title"].append(title)


        w=(nltk.ne_chunk(pos_tag(word_tokenize(title))))
        #print(title)
        for key in w:
            if type(key) == nltk.tree.Tree:
                if str(key).find('PERSON') > -1 or str(key).find('ORGANIZATION') > -1:
                    name = ' '.join(i[0] for i in key.leaves())
                    if not name.lower() in stopwoorden:
                        if len(name) > 3:
                            if not name in words:
                                if name.find(' ')>-1:
                                    words[name]={}
                                    words[name]["title"] = [title]
                                    words[name]["count"]=8
                                else:
                                    words[name]={}
                                    words[name]["title"] = [title]
                                    words[name]["count"] = 5
                            else:
                                if name.find(' ')>-1:
                                    words[name]["count"]+=8
                                    words[name]["title"].append(title)
                                else:
                                    words[name]["count"] +=5
                                    words[name]["title"].append(title)

        title=unicode(strip_tags(item['summary']))
        w=(nltk.ne_chunk(pos_tag(word_tokenize(title))))
        #print(title)
        for item in w:
            if type(item) == nltk.tree.Tree:
                if str(item).find('PERSON') > -1 or str(item).find('ORGANIZATION') > -1:
                    name = ' '.join(i[0] for i in item.leaves())
                    if not name.lower() in stopwoorden:
                        if len(name) > 3:
                            if not name in words:
                                if name.find(' ') > -1:
                                    words[name]={}
                                    words[name]["title"] = [title]
                                    words[name]["count"] = 5
                                else:
                                    words[name]={}
                                    words[name]["title"] = [title]
                                    words[name]["count"] = 3
                            else:
                                if name.find(' ')>-1:
                                    words[name]["count"] += 5
                                    words[name]["title"].append(title)
                                else:
                                    words[name]["count"] += 3
                                    words[name]["title"].append(title)

#dbp = open('words','r')
#data=dbp.read()
#res={}
#for line in data.split('\n'):
#    try:
#        l=line.split("'")[1]
#    except:
#        pass
#    for item in words:
#        if len(item) > 10:
#            if item.lower() == l.lower() and len(l) > 3:
#                url=(line.split(',')[1].split('<')[1].split('>')[0])
#                d=urllib.urlopen("http://data.kbresearch.nl/DBP:"+url+"?depiction").read()
#                img=d.replace('commons','en')
#                res[item] = {"url" : url, "img" : img}
#                break

sorted_words = sorted(words.iteritems(), key=operator.itemgetter(1))
for item in sorted_words:
    print(item[0])
    pprint(item[1])
