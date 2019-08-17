#!/usr/bin/env pyhton3.5

import requests
from contextlib import closing
import bz2

DBPEDIA_BASEURL = 'http://downloads.dbpedia.org/current/core-i18n/'
LANG = 'nl'
WIKIDATA_FILE = DBPEDIA_BASEURL + 'wikidata/interlanguage_links_%s_wikidata.tql.bz2' % LANG


out = open('interlanguage_links','wb')
with closing(requests.get(WIKIDATA_FILE, stream=True)) as dbp_file:
    for data in dbp_file.iter_lines():
        out.write(data)
out.close()
