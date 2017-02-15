#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Copyright © 2013 Willem Jan Faber (http://www.fe2.nl) All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.
* Neither the name of “Fe2“ nor the names of its contributors may be used to
  endorse or promote products derived from this software without specific prior
  written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''


import os
import sys
import time
import urllib
import pickle
import hashlib
import datetime
import operator
import datetime
import feedparser
import simplejson as json

import ConfigParser
import optparse
import logging

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import xml.etree.ElementTree as etree

from django.utils.html import strip_tags
from pprint import pprint
from optparse import OptionParser

TWITTER_URL = 'http://twir.us/?MHTW2SESSID=h4f101kosn1eehq6qaqh7f9n43&category=nl&pagecode=tagrank&toplist=topics&freqtype=now'
WIKI_URL= "https://secure.wikimedia.org/wikipedia/%s/w/api.php?action=opensearch&search=%s&limit=1&namespace=0&format=xmlfm" 
TMP_PREFIX = '/tmp/newsfeeds'

stopwoorden = set(stopwords.words('dutch'))
removechar = "';:&()^%$#@!`[]"

for i in ["nederlandse","nederland","vanochtend", "vanavond", "tweede kamer", "het", "de", "een", 'amerikaanse', 'haagse','den haag', 'nrc handelsblad', 'amsterdam', 'nrc media', 'de stentor', "russische", 'verdachte', 'tweede', 'kamer', 'verenigde staten', 'china', 'rusland', 'italiaanse', 'eerste kamer', 'argos', 'rotterdam', 'rtl nieuws', 'volkskrant']:
    stopwoorden.add(u""+i)

def _get_image(query, size, lang="nl"):
    # Wrapper for getting an wikipeida image.
    if not os.path.isfile(TMP_PREFIX + os.sep + "wiki_images.dat"):
        images = {}
        fh = open(TMP_PREFIX + os.sep + "wiki_images.dat", 'wb')
        pickle.dump(images,fh)
        fh.close()
    else:
        fh = open(TMP_PREFIX + os.sep + "wiki_images.dat")
        images = pickle.load(fh)
        fh.close()
        if query in images.keys():
            return(images[query])
        
    img = False

    try:
        # Try to read the xml from the wikipeida query.
        q = urllib.quote(query.encode('utf-8'))
        data = etree.fromstring(urllib.urlopen(WIKI_URL % (lang,q)).read())
    except:
        image[query] = False
        fh = open(TMP_PREFIX + os.sep + "wiki_images.dat", 'wb')
        pickle.dump(images, fh)
        fh.close()
        return(img)
    
    for item in data.getiterator():
        if item.text:
            if item.text.find('upload') > -1:
                img=item.text
                break
    
    # Change the size of the thumbnail.
    if img:
        item = '/'.join(img.split('px')[0].split('/')[:-1])
        item += "/"+str(size)+"px"+"".join(img.split('px')[1:])
        images[query] = item 

        fh = open(TMP_PREFIX + os.sep + "wiki_images.dat", 'wb')
        pickle.dump(images, fh)
        fh.close()

    return(item)


def get_image(word, size=350):
    # Query wikipedia for an image for a topic.
    img = False
    img =  _get_image(word, size)
    if img: return(img)
    img = _get_image(word, size, "en")
    if img: return(img)
    return("")

def analyze(summary_list, title, count, weight=1):
    max_freq=0
    # Split the known entities, and count the freq.
    for i in range(0,len(summary_list)):
        for item in summary_list[i]["entries"]:
            print(item[title])
    return(max_freq, count)

def get_news_feed(feed):
    prefix = TMP_PREFIX
    if not os.path.isdir(prefix):
        os.mkdir(prefix)
    prefix += "/" + str(time.localtime()[0]) + "_" + str(time.localtime()[1]) + "_" + str(time.localtime()[2])

    if not os.path.isdir(prefix):
        os.mkdir(prefix)
    filename = prefix + "/" + feed.split('http://')[1].split('/')[0] + "_" \
               + hashlib.md5(feed).hexdigest() + str(time.localtime()[3]) + ":" + str(time.localtime()[4]%30/30)
    if os.path.isfile(filename):
        fh = open(filename, 'r')
        data = fh.read()
        fh.close()
    else:
        data = urllib.urlopen(feed).read()
        fh = open(filename, 'w')
        fh.write(data)
        fh.close()
    feed = feedparser.parse(data)
    return(feed)

def html_unquote(v):
    for ent, repl in [(u'&nbsp;', u' '), (u'&gt;', u'>'),
                      (u'&lt;', u'<'), (u'&quot;', u'"'),
                      (u'&amp;', u'&') , (u"'",u''), (u'’',u''),(':','')]:
        v = v.replace(ent, repl)
    return v

def main():
    config = ConfigParser.ConfigParser()
    config.read('/home/aloha/data/news/news.ini')

    news_sources = {}

    for item in config._sections:
        news_sources[item] = []
        for feed in config._sections[item]["feeds"].split(','):
            news_sources[item].append(feed)

    for i in range(0,len(news_sources)):
        news_source = sorted(news_sources.keys())[i]
        title_list = summary_list = data = []
        for feed in news_sources[news_source]:
            data.append(get_news_feed(feed.strip()))
        titles = []
        tags = {}
        for feed in data:
            for entry in feed["entries"]:
                titles.append(html_unquote(entry["title"]))
                words = nltk.ne_chunk(pos_tag(word_tokenize(entry["title"])))
                for word in words:
                    if type(word) == nltk.tree.Tree:
                        word = u' '.join(i[0] for i in word.leaves())
                        if not word in tags:
                            if word.find(u' ') > -1:
                                if word.lower() in stopwoorden:
                                    tags[word] = 0
                                else:
                                    tags[word] = 4 + len(word)
                            else:
                                if word.lower() in stopwoorden:
                                    tags[word] = -1
                                else:
                                    tags[word] = 1 + len(word)
                        else:
                            if word.find(u' ') > -1:
                                if word.lower() in stopwoorden:
                                    tags[word] += 0.05
                                else:
                                    tags[word] += 4 + len(word)
                            else:
                                if word.lower() in stopwoorden:
                                    tags[word] += 0.05
                                else:
                                    tags[word] += 1 + len(word)

        for feed in data:
            for entry in feed["entries"]:
                try:
                    titles.append(html_unquote(entry["summary"]))
                except:
                    break
                words = nltk.ne_chunk(pos_tag(word_tokenize(entry["summary"])))
                for word in words:
                    if type(word) == nltk.tree.Tree:
                        word = u' '.join(i[0] for i in word.leaves())
                        if not word in tags:
                            if word.lower() in stopwoorden:
                                tags[word] = 0
                            else:
                                tags[word] = 1
                        else:
                            if word.find(' ') > -1:
                                if word.lower() in stopwoorden:
                                    tags[word] += 0.01
                                else:
                                    tags[word] += 4
                            if len(word) > 5:
                                if word.lower() in stopwoorden:
                                    tags[word] += 0.01
                                else:
                                    tags[word] += 2
                            if word.lower() in stopwoorden:
                                tags[word] += 0.1
                            else:
                                tags[word] += 1

        i=0
        known = []
        print """
{% extends "main.html" %}
{% block body %}
<nav>
  <ul>
    <li><a href="http://www.fe2.nl">Here</a></li>
    <li class='selected'><a href="/news" target='_top'>News</a></li>
    <li><a href="/work" target='_top'>Work</a></li>
    <li><a href="https://github.com/WillemJan" target='_top'>Github</a></li>
    <li><a href="http://www.kbresearch.nl/" target='_top'>KBresearch</a></li>
    <li><a href="/raspberrypi" target='_top'>Raspberrypi</a></li>
    <li><a href="http://lod.fe2.nl">Linked Open Data</a></li>
  </ul>
</nav>
        """
        print("<h1>The news caught in common images</h1><br>")
        print("<article>")
        now = datetime.datetime.now()
        print "<h3>Generated at: <time datetime='%s'>" % now.strftime("%Y-%m-%dT%H:%MZ")
        print now.strftime("%Y-%m-%d %H:%M")
        print "</h3><br>"
        for key, value in sorted(tags.iteritems(), key=lambda (k,v): (v,k), reverse=True):
            if value > 10:
                quit = False
                for item in known:
                    if item.lower().find(key.lower()) > -1:
                        quit = True
                if not quit:
                    known.append(key)
                    if type(_get_image(key, 100)) == type('str'):
                        print "<div style='float: left;width: 200px; height: 150;border-width: 1px; border-style: solid; margin: 10px; padding: 10px;'><center><a href='http://www.google.nl/search?hl=nl&gl=nl&tbm=nws&q=" +\
                                key  +"&hl=nl&gl=nl&tbm=nws' target='_news'><img width=100 height=100 src=\"" + _get_image(key, (value+10)*5) + "\"></a><br>"
                        print "<font style='size:"+ str((10-i))+"px;'>" + key+"</font></center></div>"
                        i+=1
                        if i>20:
                            break
        print "<br style='clear: both;'><hr><br><h1>Word on the street:</h1><br><br>"
        i=0
        for key, value in sorted(tags.iteritems(), key=lambda (k,v): (v,k), reverse=True):
            if value>10:
                print "<a href='http://www.google.nl/search?hl=nl&gl=nl&tbm=nws&q=" + key.replace(' ','%20') + "'>"
                print key+"</a>"
            i+=1
            if i % 5 == 0:
                print ("<br>")
            if i>50:
                break
        print("</article>")
        print """

<script>
  $(function(){var f="&ww="+$(window).width()+"&wh="+$(window).height();var e="&dw="+$(document).width()+"&dh="+$(document).height();var c="&br="+navigator.userAgent;var d="&lm="+document.lastModified;var a="&ep="+new Date().getTime()/1000;var b="/ip/?{{ ip1 }}{{ ip }}&hn={{ hna }}"+f+e+c+d+a;$.getJSON(b,function(g){});$(window).resize(function(){var l="&ww="+$(window).width()+"&wh="+$(window).height();var k="&dw="+$(document).width()+"&dh="+$(document).height();var i="&br="+navigator.userAgent;var j="&lm="+document.lastModified;var g="&ep="+new Date().getTime()/1000;var h="/ip/?{{ ip1 }}{{ ip }}&hn={{ hna }}"+l+k+i+j+g;$.getJSON(h,function(m){})});$(document).mousemove(function(h){var g="/mouse/{{ ip }}/"+h.pageX+"/"+h.pageY;$.getJSON(g,function(i){})})});
function timerMethod() {
  var g="/ip/?{{ ip1 }}{{ ip }}?wl=" + window.location + '&ep=' + new Date().getTime()/1000;
  $.getJSON(g,function(i){});
};
$(window).load(function() {timerMethod();var timerId = setInterval(timerMethod, 10000); });
</script>
{% endblock %}                                                                                                                                                           
                                                                                                                                                       
        """

if __name__ == "__main__":
    main()
