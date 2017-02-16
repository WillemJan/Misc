#!/usr/bin/env python2.6

"""
    RiE is a Random Image Explorer built on top of the Europeana API.

    Copyright (C) 2011 Willem Jan Faber, Koninklijke Bibliotheek - National Library of the Netherlands

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

#
# This program is a somewhat polished up version, of a prototype developed at the Europeana Hackathon (http://version1.europeana.eu/web/api/hackathons),
# it was one of the price winning prototypes.
#
# It depends on a lot of python stuff, and is mainly built upon webpy // mako. The client does a request containing a query, the query is resolved via 
# the Europeana API. The client recieves a page containing ajax requests to the full objects (/get/). The program fetches the full object descriptions 
# and returns them in json format.
#

import os, web, time, urllib, hashlib , sys

# Required for apache mod_wsgi intergration.
sys.path.append(os.path.abspath(os.path.dirname(__file__)))  
sys.stdout = sys.stderr 
import cgitb; cgitb.enable()

import random
import urllib2
import simplejson

# Django and Mako for doing magic with web magic.
from mako.template import Template
from django.template.defaultfilters import escapejs

# Europeana api wrapper and template file.
from europeana.api import API
from europeana import template

DEBUG = False
BASEURL = "http://europeana.fe2.nl/static/" # Must be part of the domain running the webpy script. (For ajax sake.)

if DEBUG:
    web.config.debug = True

urls = ("/get/(.*)", "get",  # /get/  Get fullrecord.
        "/(.*)", "query")    # /*     Everything else is a query.


class get:
    def __init__(self):
        self.api= API()

    def __strclean__(self, strin):
        # Clean those evil strings.
        strout = ""
        for item in strin:
            if not item.find('http') > -1:
                if item.isalpha():
                    strout += item
                else:
                    strout += " "
        strout=strout.strip()
        return(strout.split(' ')) 

    def GET(self,path):
        try:
            # Get parsed Europeana fullrecord-data from url.
            if path.find('/www.europeana.eu/portal/') > -1:
                fullrecord=self.api.get_parse_europeana_object(escapejs(path))
        except:
            # Else return empty record.
            return({})

        words = []
        for item in fullrecord.keys():
            word_list = self.__strclean__(fullrecord[item])
            for word in word_list:
                if len(word) > 4:
                    words.append(word)
        fullrecord["word"] =  words
        referer = web.ctx.env.get('HTTP_REFERER')
        if referer:
            if referer.startswith('http://www.europeana.fe2.nl') or referer.startswith('http://europeana.fe2.nl'):
                return(simplejson.dumps(fullrecord))
            else:
                return('<a href="http://europeana.fe2.nl/">http://europeana.fe2.nl/</a>')
        return('<a href="http://europeana.fe2.nl/">http://europeana.fe2.nl/</a>')

class query:
    def __init__(self):
        pass

    def GET(self, path=None):
        web.header('Content-Type','text/html; charset=utf-8', unique=True) 
        self.api = API()
        i = web.input()
        if "q" in i.keys():
            path=i["q"]
        if not path:
            path = "Random OR Image OR Explorer"
        if len(path) < 4:
            path = "Random OR Image OR Explorer"
        if path:
            if not path.find('OR') > -1 and not path.find('AND') > -1:
                path=escapejs(path).replace(" ",' OR ')
            else:
                path=escapejs(path)
            now=time.time()
            self.api.query(path, False)
            done=time.time()
            return(Template(template.results, default_filters=['unicode'],input_encoding='utf-8').render_unicode(numfound=self.api.numfound, records=self.api.records, now=now,done=done , keyword=path, baseurl=BASEURL, api=self.api ))
        return 'Hello, world!'

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()
