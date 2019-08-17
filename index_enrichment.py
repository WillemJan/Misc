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
import sys
import urllib
import urllib2
import pprint

import  django.utils.encoding


IR_URL = "http://kbresearch.nl/get_ir?identifier=http://resolver.kb.nl/resolve?urn="

oai.DEBUG=True
done = False

j=0
unwanted_entities = ['kranten-entities-3', 'kranten-entities-2', 'kranten-entities-1', 'kranten-entities-4']

while not done:
    OAI = oai.list_records("DDD")

    if len(OAI.identifiers) == 0:
        done = True

    for identifier in OAI.identifiers:
        nr_of_le = 0
        url = IR_URL + identifier + ":ocr"

        try:
            ir = json.loads(urllib.urlopen(url).read())
        except:
            ir = {}

        named_entities = []
        places = []

        references = []

        fb_id = []
        wd_id = []
        geo_id = []
        viaf_id = []
        ppn_id = []

        if ir.get('links'):
            for item in ir.get('links'):
                if item.get('linkType') == "street":
                    place = item.get('place')
                    street = item.get('street')
                    latlong = item.get('latlong')
                    places.append({"place" : place, "street" : street, "latlong" : latlong})

                if item.get('linkType') == "NIR":
                    if not item.get('reference') in unwanted_entities:
                        url = 'http://kbresearch.nl/get_nir/?identifier=' + item.get('id')
                        try:
                            nir = json.loads(urllib.urlopen(django.utils.encoding.iri_to_uri(url)).read())
                        except:
                            nr = {"error" : "unknown"}
                        if nir.get('error'):
                            continue

                        fb = ""
                        geo = ""
                        ppn = ""
                        viaf = ""
                        wd = ""

                        nr_of_le += 1
                        if nir.get('enrich'):
                            fb = [i for i in nir.get('enrich') if i.get('linkType') == 'FB']
                            geo = [i for i in nir.get('enrich') if i.get('linkType') == 'GEO']
                            ppn = [i for i in nir.get('enrich') if i.get('linkType') == 'PPN']
                            viaf = [i for i in nir.get('enrich') if i.get('linkType') == 'VIAF']
                            wd = [i for i in nir.get('enrich') if i.get('linkType') == 'WD']

                        if fb:
                            fb = ".".join(fb[0].get('sameAs').split('/')[-2:])
                        else:
                            fb = ""

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
                            #urllib.unquote(item.get('name')))
                            #.encode('utf-8'))

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
                j+=1
                # Load_string is a json object that can directly be loaded by Solr5
                load_string = u'[{"uniqueKey":"' + identifier + u'",'
                load_string += u'"reference":{"set":["' + u'","'.join(references) + u'"]},'
                load_string += u'"name":{"set":["' + u'","'.join(named_entities) + u'"]},'

                if places:
                    #load_string += u'"latlong":{"set" :["'+ ",".join(item.get('latlong')) + '"]},'
                    #load_string += u'"street":{"set" :"'+ ",".join(item.get('street')) + '"},'
                    #load_string += u'"place":{"set" :"'+ ",".join(item.get('place')) + '"},'
                    latlong = '","'.join([i.get('latlong') for i in places])
                    street = '","'.join([i.get('street') for i in places])
                    place = '","'.join([i.get('place') for i in places])
                    load_string += u'"latlong":{"set" :["'+ latlong + '"]},'
                    load_string += u'"street":{"set" :["'+ street +'"]},'
                    load_string += u'"place":{"set" :["'+ place + '"]},'

                if wd_id:
                    load_string += u'"wd_id":{"set":["' + u'","'.join(wd_id) + u'"]},'

                if geo_id:
                    load_string += u'"geo_id":{"set":["' + u'","'.join(geo_id) + u'"]},'

                if viaf_id:
                    load_string += u'"viaf_id":{"set":["' + u'","'.join(viaf_id) + u'"]},'
                else:
                    load_string += u'"viaf_id":{"set":""},'

                if ppn_id:
                    load_string += u'"ppn_id":{"set":["' + u'","'.join(ppn_id) + u'"]},'
                else:
                    load_string += u'"ppn_id":{"set":""},'


                if fb_id:
                    load_string += u'"fb_id":{"set":["' + u'","'.join(fb_id) + u'"]}'

                if load_string.endswith(','):
                    load_string = load_string[:-1]

                load_string += u'}]'
                #print load_string

                # Sometimes a singe record can fail,
                # ignore this for now.
                if j > 1:
                    #pprint.pprint(json.loads(load_string))
                    req = urllib2.Request('http://localhost:8983/solr/DDD_artikel_research/update?commit=true')
                    req.add_header('Content-Type', 'application/json; charset=utf-8')
                    response = urllib2.urlopen(req, load_string.encode('utf-8'))
