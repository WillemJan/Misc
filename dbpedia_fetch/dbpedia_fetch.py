#!/usr/bin/env python3.5

import requests

DBPEDIA_BASEURL = 'http://downloads.dbpedia.org/current/core-i18n/'
LANG = 'nl'
WIKIDATA_FILE = DBPEDIA_BASEURL + 'wikidata/interlanguage_links_%s_wikidata.tql.bz2' % LANG

print(WIKIDATA_FILE)
