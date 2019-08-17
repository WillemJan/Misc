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

import sys
import json
import urllib, re
import urllib2
import datetime

from pprint import pprint
from bson.json_util import dumps
from pymongo import MongoClient

def fix_nir_collection(prefix, name, wdid):
    # Fetch the request parameters
    mongo_connection = MongoClient("192.87.165.3")
    db = mongo_connection.links
    collection = db.nir
    try:
        data = collection.find_one({"links.linkType" : prefix,
                                    "links.id" : name})
    except:
        mongo_connection.close()
        return

    lang = False
    seen_ids=[]
    new = []
    if data == None:
        mongo_connection.close()
        return False

    print("Found", name)

    for item in data["links"]:
        if not 'FB' in seen_ids and item.get('linkType') == 'FB':
            seen_ids.append('FB')
            new.append(item)
        if not 'DBP' in seen_ids and item.get('lang') and item.get('linkType') == 'DBP':
            seen_ids.append('DBP')
            new.append(item)
        if not 'VIAF' in seen_ids and item.get('linkType') == 'VIAF':
            seen_ids.append('VIAF')
            new.append(item)
        if not 'WD' in seen_ids and item.get('linkType') == 'WD':
            seen_ids.append('WD')
            new.append(item)
        if not 'GEO' in seen_ids and item.get('linkType') == 'GEO':
            seen_ids.append('GEO')
            new.append(item)
        if not 'PPN' in seen_ids and item.get('linkType') == 'PPN':
            seen_ids.append('PPN')
            new.append(item)

    if not 'WD' in seen_ids:
        record = {}
        record["altType"] = u''
        record["contentType"] = u'application/json'
        record["datestamp"] = datetime.datetime.now()
        record["id"] = wdid
        record["linkType"] = u'WD'
        record["reference"] = u'wikidata-2015-07-02'
        record["relType"] = u'sameAs'
        record["status"] = u'OK'
        new.append(record)
        print("** WIKIDATA ID NEW **", dbpedia_id)

    if len(new) >= 2:
        data["links"] = new
        print("Replaceing old with new!")
        #pprint(data)
        collection.save(data)

    mongo_connection.close()
    return True

if __name__ == "__main__":
    import codecs
    i = 0
    with codecs.open('interlanguage_links_nl.txt', 'r', 'utf-8') as fp:
        for line in fp:
            dbpedia_id = line.split(' ')[0].split('/')[-1][:-1]
            wd_id = line.strip().split('\t')[0].split('/')[-1][:-3]

            fix_nir_collection("DBP", dbpedia_id, wd_id)
