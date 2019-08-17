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


# Link service
#
# Expects ocr-text from supplied url or text parameters,
# reads data from url and calls named entity recognizer with the data,
# subsequently calls the disambiguation service


import json
import re
import urllib

from flask import Flask, request, Response
from lxml import etree

_author = ["WillemJan Faber", ]

NER_URL_URL = 'http://tptahost/tpta2/analyse?lang=nl&url='
NER_URL_TXT = 'http://localhost:8080/tpta2/analyse?lang=nl&text='

DA_URL_NL = 'http://disambig.kbresearch.nl/link?ne='

application = Flask(__name__)
application.debug = True


def query_da(query, debug, seen, url='', text='', data=''):
    '''
    Query the disambiguation service/url,
    start with the dutch if it fails,
    continue to the english one.
    '''
    query = query.replace(' &amp', '')
    query = query.replace(' quot ;', '')
    query = query.encode('utf-8')

    da_url = DA_URL_NL
    da_url += urllib.quote(query)

    if debug:
        da_url += "&debug=True"
    
    if url:
	da_url += "&url=" + url
    else:
	da_url += "&text=" + text 
        
    if data:
	data = data.replace(' &amp', '')
	data = data.replace(' quot ;', '')
	data = data.encode('utf-8')
	da_url += "&data" + data
    
    data = urllib.urlopen(da_url).read()
    result = json.loads(data.encode('utf-8'))

    if result and result.get('link'):
        if result["link"] not in seen:
            seen.append(result["link"])
            return [data, seen]
        else:
            return [data, seen]
    else:
        return [data, seen]


@application.route('/')
def index():
    url = request.args.get('url')
    if not url:
        text = request.args.get('text')
        if not text:
            return "Envoke with ?url= or ?text="

    debug = request.args.get('debug')
    callback = request.args.get('callback')
    context = request.args.get('context') 

    if url:
        ner_url = NER_URL_URL + url
        data = urllib.urlopen(ner_url).read()
    else:
        ner_url = NER_URL_TXT + text
        data = urllib.urlopen(ner_url).read()
    xml = etree.fromstring(data)
    
    done = []  # Prevent same strings to be lookup twice
    seen = []  # Make sure only one link of the same kind is in the result
    lookup = [] # Final results

    # Loop over all named entities,
    # and query the disambiguation service.

    for item in xml.iter():
        if item.text and len(item.text) > 1:
            if not item.text in done:
		if context == 'true': 
		    if url:
			lookup_result, seen = query_da(item.text, debug, seen, url, '', data)
			lookup.append(lookup_result)
		    else:
			lookup_result, seen = query_da(item.text, debug, seen, '', text, data)
			lookup.append(lookup_result)
		else:
		    lookup_result, seen = query_da(item.text, debug, seen)
		    lookup.append(lookup_result)

    # Create a results array for further use.
    if callback:
        result = callback + '({ "linkedNEs": ['
    else:
        result = '{"linkedNEs": ['

    for item in lookup:
        if len(item) > 0:
            if not item == "{}":
                result += item + ","
            else:
                if debug:
                    result += item + ","
    if len(result) > 1:
        if callback:
            result = result[:-1] + "]});"
        else:
            result = result[:-1] + "]}"
    else:
        if callback:
            result += "])"
        else:
            result += "]}"

    if result == '{"linkedNEs": ]}':
        result = '{"linkedNEs": []}'

    return Response(response=result, status=200, mimetype="application/json")
