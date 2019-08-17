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

import datetime
import json
import re
import sys
import urllib

from bson.json_util import dumps
from pprint import pprint
from pymongo import MongoClient

def fix_nir_collection(prefix, name, viafid):
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
    new = []
    seen_ids=[]

    if data == None:
        print("Not found ", name)
        return

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
            if item.get("id") == viafid:
                print("** VIAF ID CORRECT **", dbpedia_id)
            else:
                print("** VIAD ID DIFFERS? got:", dbpedia_id, item.get('id'), viafid)

        if not 'WD' in seen_ids and item.get('linkType') == 'WD':
            seen_ids.append('WD')
            new.append(item)

        if not 'GEO' in seen_ids and item.get('linkType') == 'GEO':
            seen_ids.append('GEO')
            new.append(item)

    if not 'VIAF' in seen_ids:
        record = {}
        record["altType"] = u''
        record["contentType"] = u'application/json'
        record["datestamp"] = datetime.datetime.now()
        record["id"] = viafid
        record["linkType"] = u'VIAF'
        record["reference"] = u'viaf-2014-06-25'
        record["relType"] = u'sameAs'
        record["status"] = u'OK'
        new.append(record)
        print("** VIAF ID NEW **", dbpedia_id)

    if not 'DBP' in seen_ids:
        for item in data["links"]:
            if item.get('linkType') == 'DBP':
                seen_ids.append('DBP')
                new.append(item)
                break

    if len(new) >= 2:
        data["links"] = new
        print("Replaceing old with new!")
        collection.save(data)

    mongo_connection.close()

if __name__ == "__main__":
    with open('all_viaf_en.txt') as fp:
        for line in fp:
            viaf_id = (line.strip().split('\t')[0].split('/')[-1])
            dbpedia_id = (line.strip().split('\t')[1].split('/')[-1])
            fix_nir_collection("DBP", dbpedia_id, viaf_id)
