#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

import fileinput
import json
import re
import requests
import sys
import time


import threading

from elasticsearch import Elasticsearch
from pprint import pprint
from queue import Queue

DEBUG = True
DEBUG_MAX = 100 # NR of records for debugging

ES_HOST = '127.0.0.1'
ES_INDEX_NAME = 'dbpedia'
ES_THREADS = 50
ES = Elasticsearch(ES_HOST, timeout=1000, max_retries=100)

COMMIT_MAX = 10
INTERLANGUAGE_LINKS_NL = '../nobackup/dbp/interlanguage_links_nl.ttl'
LABELS_NL = 'current/nl/labels_nl.ttl'

JSON_HEADERS = {'content-type': 'application/json'}

LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'

REGEX_LIST = {
    'id_en' : ['.+<http://dbpedia.org/resource/(.+?)>+.*'],
    'id'    : ['.+<http://wikidata.dbpedia.org/resource/Q(.+?)>+',
               '.+<http://wikidata.org/entity/Q(.+?)>+'],
    'id_nl' : ['.*<http://nl.dbpedia.org/resource/(.+?)>',
               '<http://nl.dbpedia.org/resource/(.+?)>\s.+'],
    'label' : ['.*>\s\"(.+?)\"@nl.+']
}




'''
   <field name="inlinks" type="int" indexed="true" stored="true" />
   <field name="abstract_nl" type="text_en" indexed="true" stored="true"/>
   <field name="abstract_en" type="text_en" indexed="true" stored="true"/>
   <field name="schemaorgtype" type="string" indexed="true" stored="true" multiValued="true"/>
   <field name="lang" type="string" indexed="True" stored="true" multiValued="False"/>
   <field name="disambig" type="int" indexed="True" stored="true" multiValued="False"/>

   <field name="yob" type="int" indexed="True" stored="true" multiValued="False"/>
   <field name="yod" type="int" indexed="True" stored="true" multiValued="False"/>
   <field name="dob" type="string" indexed="True" stored="true" multiValued="False"/>
   <field name="dod" type="string" indexed="True" stored="true" multiValued="False"/>

   <field name="gender" type="string" indexed="True" stored="true" multiValued="False"/>
   <field name="wd_id" type="string" indexed="True" stored="true" multiValued="False"/>
'''

def normalize(input_str):
    '''
    Normalize given input to lowercase, and remove . _–- tokens.

    >>> normalize("A. Bertols-Apenstaartje")
    "a bertols apenstaartje"
    '''

    if input_str.find('.') > -1:
        input_str = input_str.replace('.', ' ')
    if input_str.find('-') > -1:
        input_str = input_str.replace('-', ' ')
    if input_str.find('_') > -1:
        input_str = input_str.replace('_', ' ')
    if input_str.find('   ') > -1:
        input_str = input_str.replace('   ', '  ')
    if input_str.find('  ') > -1:
        input_str = input_str.replace('  ', ' ')
    if input_str.find('\u2013') > -1:
        input_str = input_str.replace('\u2013', ' ')

    input_str = input_str.strip()
    input_str = input_str.lower()

    return input_str


def es_create_index(delete_first=True):
    mapping = '''
        {
          "mappings":{
            "dbpedia":{
                "properties": {
                    "id":    { "type": "string", "index": "not_analyzed"},
                    "id_nl": { "type": "string", "index": "not_analyzed"},
                    "id_en": { "type": "string", "index": "not_analyzed"},
                    "lastpart" : { "type" : "string"},
                    "lastpart_str" : { "type" : "string", "index": "not_analyzed" },
                    "pref_title" : {"type" : "string"},
                    "pref_title_str" : {"type" :"string", "index" : "not_analyzed"},
                    "title" : { "type" : "string"},
                    "title_str" : {"type" : "string", "index" : "not_analyzed" },
                    "org_title" : {"type" : "string"},
                    "org_title_str" : {"type" : "string", "index" : "not_analyzed"},
                    "inlinks" : {"type" : "integer", "index" : "not_analyzed"},
                    "disambig" : {"type" : "integer"}
              }
            }
          }
        }
    '''


    if delete_first:
        try:
            response = ES.indices.delete(index=ES_INDEX_NAME)
        except:
            pass

    response = ES.indices.create(index=ES_INDEX_NAME,
                                 ignore=400,
                                 body=mapping)

def es_worker(q, i, type_op):
    errors = 0
    done = False

    docs = []
    bulk_data = []

    for i in range(int(COMMIT_MAX / ES_THREADS)):
        if q.not_empty:
            #lock.acquire()
            doc = q.get()
            ##lock.release()
            if doc:
                docs.append(doc)
            q.task_done()

    for doc in docs:
        if type_op == "index":
            op_dict =  {"index" : {"_index" : ES_INDEX_NAME, "_type": ES_INDEX_NAME, "_id" : doc.get('id')}}
        elif type_op == "update":
            op_dict =  {"update" : {"_index" : ES_INDEX_NAME, "_type": ES_INDEX_NAME, "_id" : doc.get('id')}}
        #bulk_data.append(op_dict)
        #bulk_data.append(doc)
        print(doc)

    if docs:
        done = False
        while not done:
            #try:
            res = ES.bulk(index=ES_INDEX_NAME, body=bulk_data, refresh=False) #, timeout=600)
            print(res.get('errors'))
            '''
            if res.get('errors') == False:
                    done = True
                    print("Committed: %i" % len(docs))
                else:
                    errors+=1
                    print("ERROR1", errors, res)
                    time.sleep(1)
            except:
                errors += 1
                e = sys.exc_info()[0]
                print("ERROR2", errors, e)
                time.sleep(1)
            '''
    return

def fetch_by_id(id="Albert_Einstein"):
    start = time.time()

    q = 'id_nl:"%s"' % id

    session = requests.session()

    params = {'q' : q,
              'wt' : 'json'}

    res = session.request("GET", SOLR_SELECT, params=params)

    if res.status_code == 200:
        res = json.loads(res.content.decode('utf-8'))
    else:
        print("Error while talking to SOLR")
        return ""

    if res.get('response'):
        if res.get('response').get('numFound'):
            if int(res.get('response').get('numFound')) >= 1:
                duration = time.time() - start
                return (res.get('response').get('docs')[0].get('id'), duration)


class index_dbpedia_dump():
    no_id_found = 0

    def __init__(self):

        # Setup logging handler
        self.logger = logging.getLogger()
        handler = logging.StreamHandler()
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        #if DEBUG:
        #self.logger.setLevel(logging.DEBUG)
        print("Whoooow")

    def interlanguage_links_nl(self, fname = INTERLANGUAGE_LINKS_NL):
        INPUT_RE_STR = {
            'id'    : REGEX_LIST['id'],
            'id_nl' : REGEX_LIST['id_nl'],
            'id_en' : REGEX_LIST['id_en']
        }

        input_re = {}

        for regex in INPUT_RE_STR:
            input_re[regex] = []
            for reg in INPUT_RE_STR[regex]:
                input_re[regex].append(re.compile(reg))

        self.commit_buffer = []
        self.type_op = "index" # Type of operation for ES

        prev_dbpedia_id_nl = ''

        time_total = 0

        self.commit = 0 # doc_to_commit
        self.commit_total = 0 # total_docs_committted

        obj = {}
        print("Wait?")
        for line in fileinput.input(files=[fname],
                                    openhook=fileinput.hook_encoded("utf-8")):

            for key in INPUT_RE_STR:
                for reg in input_re[key]:
                    match_obj = reg.match(line)

                    if not match_obj:
                        continue

                    value = match_obj.group(1)

                    if key == 'id_nl' and key in obj and not obj[key] == value:
                        if obj:
                            print("Buffer len: %i " % len(self.commit_buffer))
                            if self._check_commit():
                                break
                            self.commit_buffer.append(obj)
                            self.commit += 1
                            self.commit_total += 1
                            obj = {}
                        obj[key] = value
                    obj[key] = value
        fileinput.close()
        return


    def labels_nl(self, fname = LABELS_NL):
        '''
            <http://nl.dbpedia.org/resource/Aannemer> <http://www.w3.org/2000/01/rdf-schema#label> "Aannemer"@nl .
            "lastpart" : { "type" : "string"},
            "lastpart_str" : { "type" : "string", "index": "not_analyzed" },
            "pref_title" : {"type" : "string"},
            "pref_title_str" : {"type" :"string", "index" : "not_analyzed"},
            "title" : { "type" : "string"},
            "title_str" : {"type" : "string", "index" : "not_analyzed" },
            "org_title" : {"type" : "string"},
            "org_title_str" : {"type" : "string", "index" : "not_analyzed"},
        '''

        INPUT_RE_STR = {
            'id_nl' : REGEX_LIST['id_nl'],
            'label' : REGEX_LIST['label'],
        }

        DISAMBIG = ['doorverwijspagina', 'disambiguation']

        self.type_op = "update" # Type of operation for ES
        input_re = {}
        dbpedia_obj = {}

        total_found = 0
        total_not_found = 0

        for regex in INPUT_RE_STR:
            input_re[regex] = []
            for rule in INPUT_RE_STR[regex]:
                input_re[regex].append(re.compile(rule))

        self.commit_buffer = []
        self.commit_total = 0
        self.commit = 0

        for line in fileinput.input(files=[fname],
                                    openhook=fileinput.hook_encoded("utf-8")):
            obj = {}
            for regex in input_re:
                for reg in input_re[regex]:
                    key = value = None
                    match_obj = reg.match(line)

                    if not match_obj:
                        continue

                    key = regex
                    value = match_obj.group(1)

                    obj[key] = value

            '''
            for item in DISAMBIG:
                if value and value.find(item) > -1:
                    continue
            
            disambig = 0
            if value and value.find('(') > -1:
                disambig = 1
            '''

            if obj:
                res = ES.search(index=ES_INDEX_NAME, q='id_nl:"%s"' % obj['id_nl'])

                if not res.get('hits').get('total') == 1:
                    self.no_id_found += 1
                    print(res.get('hits').get('total'))
                elif res.get('hits').get('total') == 1:
                    obj['id'] = res.get('hits').get('hits')[0].get('_id')
                    obj['lastpart'] = obj['lastpart_str'] = normalize(value).split('(')[0].strip().split(' ')[-1]
                    obj['pref_title'] = obj['pref_title_str'] = value
                    obj['title'] = obj['title_str'] = normalize(value)
                    obj['org_title'] = obj['org_title_str'] = value
                    self.commit_buffer.append(obj)
                    self.commit += 1

            if self._check_commit():
                break

    def _to_es(self, docs):
        q = Queue()
        threads = []

        self.logger.debug("Starting es threads..")

        for i in range(len(docs)):
            q.put(docs[i])

        for i in range(ES_THREADS):
            print("start %i " %i)
            p = threading.Thread(name='es_worker_%i' %i, target=es_worker, args=(q,i,self.type_op))
            threads.append(p)
            threads[i].deamon = True
            threads[i].start()

        self.logger.debug("Waiting for join..")
        #q.join()
        for i in range(ES_THREADS):
            print("Stopping ", i)
            threads[i].join()
        self.logger.debug("Join finished..")

    def _check_commit(self):
        if self.commit > COMMIT_MAX:
            self.commit = 0
            self.commit_total += 1
            self.logger.debug("commit_total %i " %( self.commit_total * COMMIT_MAX))
            #pprint(self.commit_buffer)
            self._to_es(self.commit_buffer)
            self.commit_buffer = []

        if DEBUG and (self.commit_total > DEBUG_MAX):
            return True
        return

if __name__ == '__main__':
    es_create_index()
    dbp = index_dbpedia_dump()
    dbp.interlanguage_links_nl()
    dbp.labels_nl()
