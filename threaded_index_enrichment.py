#!/usr/bin/env python

#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from kb.nl.api import oai

import json
import pprint
import Queue
import sys
import threading
import time
import urllib
import urllib2

import  django.utils.encoding
import socket

socket.setdefaulttimeout(10) # timeout in seconds 

GET_IR = "http://localhost:81/get_ir/?identifier="
GET_NIR = "http://localhost:81/get_nir/?identifier="
RESOLVER_PREFIX = "http://resolver.kb.nl/resolve?urn="
WORKERS = 25

done = False

unwanted_entities = ['kranten-entities-3', 'kranten-entities-2', 'kranten-entities-1', 'kranten-entities-4']

class ir_thread(threading.Thread):
    def __init__(self, ir_que, solr_que):
        threading.Thread.__init__(self)
        self.ir_que = ir_que
        self.solr_que = solr_que
        self.done = False
        self.daemon = True

    def  run(self):
        while not self.done:
            while self.ir_que.empty():
                print("IR nothing to do")
                time.sleep(10)
            while not self.ir_que.empty():
                identifier = self.ir_que.get()
                data = self.get_ir_data(identifier)
                if data:
                    self.solr_que.put(data)

    def get_ir_data(self, identifier):
        url = GET_IR + RESOLVER_PREFIX + identifier + ":ocr"

        try:
            ir = json.loads(urllib.urlopen(url).read())
        except:
            self.ir_que.put(identifier)
            return False

        if not ir.get('links'):
            return False
        
        places = self.parse_ir_data_places(ir.get('links'))
        identifiers = self.parse_ir_data_identifiers(ir.get('links'))

        load_string = ""
        if places or identifiers:
            load_string = u'[{"uniqueKey":"' + identifier + u'",'
            load_string += places
            load_string += identifiers
            load_string += u'}]'
        return load_string


    def parse_ir_data_places(self, links):
        places = []
        load_string = ""

        for item in links:
            if item.get("linkType") == "street":
                place = item.get("place")
                street = item.get("street")
                latlong = item.get("latlong")
                places.append({"place" : place, "street" : street, "latlong" : latlong})

        if places:
            latlong = '","'.join([i.get('latlong') for i in places])
            place = '","'.join([i.get('place') for i in places])
            street = '","'.join([i.get('street') for i in places])

            load_string += u'"latlong":{"set" :["'+ latlong + '"]},'
            load_string += u'"street":{"set" :["'+ street +'"]},'
            load_string += u'"place":{"set" :["'+ place + '"]},'

        return load_string

    def parse_ir_data_identifiers(self, links):
        named_entities = []
        load_string = ""
        nir = {}

        for item in links:
            if item.get("linkType") == "NIR" and not item.get("reference") in unwanted_entities:
                if nir.get("error") and nir.get("error").startswith(GET_NIR):
                    url = nir.get("error")
                else:
                    url = GET_NIR + item.get("id")
                try:
                    nir = json.loads(urllib.urlopen(django.utils.encoding.iri_to_uri(url)).read())
                except:
                    nir = {"error" : url}

                if nir.get("error"):
                    continue

                references = []
                fb_id = []
                geo_id = []
                ppn_id = []
                viaf_id = []
                wd_id = []

                fb = geo = ppn = viaf = wd = ""

                if nir.get('enrich'):
                    fb = [i for i in nir.get('enrich') if i.get('linkType') == 'FB']
                    geo = [i for i in nir.get('enrich') if i.get('linkType') == 'GEO']
                    ppn = [i for i in nir.get('enrich') if i.get('linkType') == 'PPN']
                    viaf = [i for i in nir.get('enrich') if i.get('linkType') == 'VIAF']
                    wd = [i for i in nir.get('enrich') if i.get('linkType') == 'WD']

                if fb:
                    fb = ".".join(fb[0].get('sameAs').split('/')[-2:])
                if geo:
                    geo = ".".join(geo[0].get('sameAs').split('/')[-1:])
                if wd:
                    wd = ".".join(wd[0].get('sameAs').split('/')[-1:])
                if viaf:
                    viaf = ".".join(viaf[0].get('sameAs').split('/')[-1:])
                if ppn:
                    ppn = ".".join(ppn[0].get('sameAs').split('/')[-1:])

                if not item.get('objectName') in named_entities:
                    named_entities.append(item.get('objectName'))
                if not item.get('reference') in references:
                    references.append(item.get('reference'))

                if fb and not fb in fb_id:
                    fb_id.append(fb)
                if geo and not geo in geo_id:
                    geo_id.append(geo)
                if viaf and not viaf in viaf_id:
                    viaf_id.append(viaf)
                if wd and not wd in wd_id:
                    wd_id.append(wd)
                if ppn and not wd in ppn_id:
                    ppn_id.append(ppn)

        if named_entities:
            load_string += u'"reference":{"set":["' + u'","'.join(references) + u'"]},'
            load_string += u'"name":{"set":["' + u'","'.join(named_entities) + u'"]},'

            if wd_id:
                load_string += u'"wd_id":{"set":["' + u'","'.join(wd_id) + u'"]},'

            if geo_id:
                load_string += u'"geo_id":{"set":["' + u'","'.join(geo_id) + u'"]},'

            if viaf_id:
                load_string += u'"viaf_id":{"set":["' + u'","'.join(viaf_id) + u'"]},'
            #else:
            #    load_string += u'"viaf_id":{"set":""},'

            if ppn_id:
                load_string += u'"ppn_id":{"set":["' + u'","'.join(ppn_id) + u'"]},'
            #else:
            #    load_string += u'"ppn_id":{"set":""},'

            if fb_id:
                load_string += u'"fb_id":{"set":["' + u'","'.join(fb_id) + u'"]}'

        if load_string.endswith(','):
            load_string = load_string[:-1]

        return load_string

class solr_thread(threading.Thread):
    def __init__(self, solr_que):
        threading.Thread.__init__(self)
        self.solr_que = solr_que
        self.daemon  = True
        self.done = False

    def run(self):
        while not self.done:
            while self.solr_que.empty():
                print ("Solr nothing todo")
                time.sleep(10)
            load_string = self.solr_que.get()


            done = False
            while not done:
                try:
                    req = urllib2.Request('http://localhost:8983/solr/DDD_artikel_research/update?commit=true')
                    req.add_header('Content-Type', 'application/json; charset=utf-8')
                    response = urllib2.urlopen(req, load_string.encode('utf-8'))
                    print response.code
                    done = True
                except:
                    done = False


ir_que = Queue.Queue()
solr_que = Queue.Queue()

ir_workers = []
solr_workers = []

for i in range(WORKERS):
    worker = ir_thread(ir_que, solr_que)
    worker.start()
    ir_workers.append(worker)

for i in range(WORKERS * 4):
    worker = solr_thread(solr_que)
    worker.start()
    solr_workers.append(worker)

while not done:
    OAI = oai.list_records("DDD")

    if len(OAI.identifiers) == 0:
        done = True
        break

    print("Starting fill loop")
    for identifier in OAI.identifiers:
        ir_que.put(identifier)
    print("Ending fill loop")

    while ir_que.qsize() > 24000:
        print("Main tread sleep")
        time.sleep(10)

for i in ir_workers:
    i.join()

for i in solr_workers:
    i.join()
