#!/usr/bin/env python3

import fileinput
import requests
import re
import time
import json
import threading
from elasticsearch import Elasticsearch


#26737

ES = Elasticsearch()
print(dir(ES))
print(ES.get(index="dbpedia", doc_type="dbpedia", id='Q1868')['_source'])
print(ES.search(index="dbpedia", doc_type="dbpedia", q='id_wd:"Q1868"')['hits'])

#get(index="my-index", doc_type="test-type", id=42)['_source']

def interlanguage_links_nl(fname = "test.txt"):
    INPUT_RE_STR = {
        'id_nl' : ".*<http://nl.dbpedia.org/resource/(.+?)>",
        'id_en' : ".+<http://dbpedia.org/resource/(.+?)>+.*",
        'id'   : ".+<http://wikidata.org/entity/Q(.+?)>+",
        'id'   : ".+<http://wikidata.dbpedia.org/resource/Q(.+?)>+",
    }

    input_re = {}
    commit_buffer = []

    for regex in INPUT_RE_STR:
        input_re[regex] = re.compile(INPUT_RE_STR[regex])

    dbpedia_obj = {}

    prev_dbpedia_id_nl = ''

    time_total = 0
    commit = 0 # doc_to_commit
    commit_total = 0 # total_docs_committted

    with open('test.txt', encoding='utf-8') as f:
        for line in f:
            print(line)

    for line in fileinput.input(files=[fname],
                                openhook=fileinput.hook_encoded("utf-8")):
        print((line), line)


if __name__ == '__main__':
    interlanguage_links_nl()
