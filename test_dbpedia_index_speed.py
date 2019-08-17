#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
from pprint import pprint

import fileinput
import json
import random
import re
import requests
import time

SOLR = 'http://localhost:4041/solr/dbpedia3/'
SOLR_UPDATE = SOLR + 'update/json'
SOLR_SELECT = SOLR + 'select'

INTERLANGUAGE_LINKS_NL = 'nl/interlanguage_links_nl.ttl'
JSON_HEADERS = {'content-type': 'application/json'}

DEBUG = False
DEBUG_MAX = 100 # NR of records for debugging

COMMIT_MAX = 10000

ES = Elasticsearch()
mapping = '''
{  
  "mappings":{  
    "dbpedia":{ 
        "properties": { 
        "id":    { "type": "integer"  }, 
        "id_nl":     { "type": "string"  }, 
        "id_en":      { "type": "string" }  
      }
    }
  }
}'''

#print (ES.indices.delete(index='dbpedia'))
#print (ES.indices.create(index='dbpedia', ignore=400, body=mapping))

def to_solr(docs, commit=False, solr_endpoint = SOLR_UPDATE):
    global i

    for doc in docs:
        i += 1
        res = ES.index(index="dbpedia", doc_type='dbpedia', id=i, body=doc)
        print(res, doc)
    return 1

    doc = json.dumps(doc)
    session = requests.session()

    if DEBUG:
        print(doc)

    params = {}
    if commit:
        params = {'commit' : 'true'}

    start = time.time()

    res = session.request('GET', solr_endpoint,
                          params=params,
                          data=doc,
                          headers = JSON_HEADERS)

    duration = time.time() - start

    print(res.status_code, duration)
    return duration


def fetch_by_id(id="Herman_Brood", method="es"):
    start = time.time()

    ids = [ 'Kunerad', 'Mauvages', '2011_MD', 'Derna_(stad)', 'Napo_(provincie)', 'Haironville', 'Stanley_Cup', 'Punerot', 'Eoin_Colfer', 'Odense_BK', 'Oshawa', 'East_Renfrewshire', 'Slough', 'Salpeterigzuur', 'Erythrodiplax_fulva', 'Timofey_Guzhenko_(schip,_2009)', 'Eiwitsynthese', 'Raon-sur-Plaine', 'Joelfeest', 'Blaymont', 'Moody_Blues', 'Troitse-Sergieva_Lavra', 'Dunfermline', 'UEFA_Europa_League_2011/12', 'Anchises', 'Das_wohltemperierte_Klavier', 'Ferroceen', 'Gloria_(mis)', 'East_Dunbartonshire', 'Tholen', 'Bof', 'Vest', '1_Mai', 'Super_Bowl_XXXIV', 'Timati', 'Hertensteen', 'Skrchov', 'Chemische_computer', 'Conn_Smythe_Trophy', 'Máire_Geoghegan-Quinn', 'Bahlinger_SC', 'Olimpio_Bizzi', 'Leemte_in_de_taal', 'Activia_(zuivel)', 'Pyrolyse', 'MIMO', 'Voetbal_op_de_Olympische_Zomerspelen_1980', 'Sully', 'International_Financial_Reporting_Standards', 'Stromatoliet', 'Quick_Step_(wielerploeg)/2011', 'Gifford', 'Donk_(landvorm)', 'Koltsovo', 'The_Last_King_of_Scotland', 'Interparlementaire_Unie', 'Bataven', 'Militaire_eenheid', 'Saissac', 'Villingili_(Kaafu-atol)', 'Upper_Lachlan_Shire_Council', 'Geheugenloosheid', 'Spital_am_Semmering', 'Stochastisch_proces', 'Cananea', 'Granite_City', 'Quierzy', 'Montfort-sur-Boulzane', 'Swiss', 'Slot_Ulriksdal', 'Chinese_frankolijn', 'Adler_(Sotsji)', 'Giandomenico_Basso', 'Renderen', 'Riols', 'Gewone_dwergvleermuis', 'Ljugarn', 'Oberrothenbach', 'Axien', 'Mulondo', 'Continue_functie_(analyse)', 'Ton_du_Chatinier', "Skuodas_District_Municipality", "Zomba,_Malawi", 'Biharkeresztes'] 

    '''
{'_type': 'dbpedia', 'created': True, '_shards': {'successful': 1, 'failed': 0, 'total': 2}, '_version': 1, '_index': 'dbpedia', '_id': '105662'} {'id_nl': 'A2', 'id_en': 'A2', 'id': '219337'}
{'_type': 'dbpedia', 'created': True, '_shards': {'successful': 1, 'failed': 0, 'total': 2}, '_version': 1, '_index': 'dbpedia', '_id': '105663'} {'id_nl': 'Ballista', 'id_en': 'Ballista', 'id': '219433'}
{'_type': 'dbpedia', 'created': True, '_shards': {'successful': 1, 'failed': 0, 'total': 2}, '_version': 1, '_index': 'dbpedia', '_id': '105664'} {'id_nl': 'DE', 'id_en': 'DE', 'id': '219328'}
{'_type': 'dbpedia', 'created': True, '_shards': {'successful': 1, 'failed': 0, 'total': 2}, '_version': 1, '_index': 'dbpedia', '_id': '105665'} {'id_nl': 'Durfkapitaal', 'id_en': 'Venture_capital', 'id': '219409'}
{'_type': 'dbpedia', 'created': True, '_shards': {'successful': 1, 'failed': 0, 'total': 2}, '_version': 1, '_index': 'dbpedia', '_id': '105666'} {'id_nl': 'Judith_Butler', 'id_en': 'Judith_Butler', 'id': '219368'}
{'_type': 'dbpedia', 'created': True, '_shards': {'successful': 1, 'failed': 0, 'total': 2}, '_version': 1, '_index': 'dbpedia', '_id': '105667'} {'id_nl': 'Bill_of_Rights_van_1689', 'id_en': 'Bill_of_Rights_1689', 'id': '219447'}
{'_type': 'dbpedia', 'created': True, '_shards': {'successful': 1, 'failed': 0, 'total': 2}, '_version': 1, '_index': 'dbpedia', '_id': '105668'} {'id_nl': 'Woedoe', 'id_en': 'Wudu', 'id': '219466'}
{'_type': 'dbpedia', 'created': True, '_shards': {'successful': 1, 'failed': 0, 'total': 2}, '_version': 1, '_index': 'dbpedia', '_id': '105669'} {'id_nl': 'United_Artists', 'id_en': 'United_Artists', 'id': '219400'}
{'_type': 'dbpedia', 'created': True, '_shards': {'successful': 1, 'failed': 0, 'total': 2}, '_version': 1, '_index': 'dbpedia', '_id': '105670'} {'id_nl': 'Missionaris', 'id_en': 'Missionary', 'id': '219477'}
{'_type': 'dbpedia', 'created': True, '_shards': {'successful': 1, 'failed': 0, 'total': 2}, '_version': 1, '_index': 'dbpedia', '_id': '105671'} {'id_nl': 'The_Hangover', 'id_en': 'The_Hangover', '

    '''

    id = random.choice(ids)

    if method == "solr":
        q = 'id_nl:"%s"' % id

        session = requests.session()

        params = {'q' : q,
                  'fl' : 'id',
                  'wt' : 'json'}

        res = session.request("GET", SOLR_SELECT, params=params)

        if res.status_code == 200:
            res = json.loads(res.content.decode('utf-8'))
        else:
            print("Error while talking to SOLR")
            duration = time.time() - start
            return (0, duration)

        if res.get('response'):
            if res.get('response').get('numFound'):
                if int(res.get('response').get('numFound')) >= 1:
                    duration = time.time() - start
                    return (res.get('response').get('docs')[0].get('id'), duration)

        duration = time.time() - start
        return (0, duration)
    

    if method == "es":
        try:
            res = ES.search(index="dbpedia", body={"query": {"match": {'id_nl':id}}})
        except:
            res = {}

        if res.get('hits') and res.get('hits').get('total') >= 1:
            duration = time.time() - start
            print(id, "HIT")
            return (res.get('hits').get('hits')[0].get('_source').get('id'), duration)
        else:
            print(id, "MISSS")
        duration = time.time() - start
        return (0, duration)

def interlanguage_links_nl(fname = INTERLANGUAGE_LINKS_NL):
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
    commit = 0
    commit_total = 0

    for line in fileinput.input(files=[fname],
                                openhook=fileinput.hook_encoded("utf-8")):

        if DEBUG and commit_total > 10 and (commit_total % DEBUG_MAX == 0):
            break

        if commit > COMMIT_MAX:
            commit = 0
            commit_total += 1
            to_solr(commit_buffer)
            commit_buffer = []

        for regex in input_re:
            key = value = None
            match_obj = (input_re[regex].match(line))

            if not match_obj:
                continue

            key = regex
            value = match_obj.group(1)

            if key == 'id_nl':
                if not value == prev_dbpedia_id_nl:
                    prev_dbpedia_id_nl = value
                    if dbpedia_obj and not dbpedia_obj in commit_buffer:
                        #time_total += to_solr(dbpedia_obj)
                        commit_buffer.append(dbpedia_obj)
                        commit += 1
                    dbpedia_obj = {key : value}

            dbpedia_obj[key] = value

    to_solr(commit_buffer)


def solr_commit(solr_endpoint = SOLR_UPDATE):
    session = requests.session()

    params = {'commit' : 'true'}

    res = session.request('GET', solr_endpoint,
                          params=params,
                          headers = JSON_HEADERS)

if __name__ == '__main__':
    #interlanguage_links_nl()
    #solr_commit()
    TEST_BATCH_SIZE = 10000

    duration_solr = 0
    for _ in range(TEST_BATCH_SIZE):
        (id, t) = fetch_by_id("aap", "solr")
        duration_solr += t
    print("Solr, total time: %i Per record: %2f" % (duration_solr, duration_solr/TEST_BATCH_SIZE))
 
    duration_es = 0
    for _ in range(TEST_BATCH_SIZE):
        (id, t) = fetch_by_id()
        duration_es += t

    print("ElasticSearch, total time: %s Per record: %2f" %(duration_es, duration_es/TEST_BATCH_SIZE))
    print("SOLR - Elasticsearch", duration_solr-duration_es)
