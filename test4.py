#!/usr/bin/env python3.5

import asyncio
import logging
import sys
import time

from asyncio import Queue
from dbp_files import *
from elasticsearch_async import AsyncElasticsearch
from es_helpers import *
from pprint import pprint
       
logger = logger(__name__, 'info')
logger.info('file("%s").class("%s") Initialized.' % (__file__, __name__))

q = Queue()
op_dict = {"index": {"_index": 'dbpedia',
                     "_type": 'dbpedia',
                     "_id": ''}}

es = ElasticsearchHelper(port='9200',
                         loglevel='info')

es.create_index(delete_first=True)

COMMIT_SIZE = 100


PATH = './dbpedia_index/current/nl/' #'/opt/home/wfa011/code/create_dbpedia_index/3.0/current/nl/'
PATH = '/home/aloha/nobackup/dbp/'

disambiguations = Disambiguations()
disambiguations.PATH = PATH

labels = Labels()
labels.PATH = PATH

labels_en_uris = Labels_en_uris()
labels_en_uris.PATH = PATH

redirects = Redirects()
redirects.PATH = PATH

Interlanguage_links.FILENAME = 'interlanguage_links_nl_wikidata.ttl'
interlanguage_links = Interlanguage_links()
interlanguage_links.PATH = PATH


client = AsyncElasticsearch()



@asyncio.coroutine
def indexer_looper(q):
    bulk_data = []
    done = False
    doc = {}

    while not done:
        size = q.qsize
        if size:
            doc = yield from q.get()
        if isinstance(doc, str):
            yield from asyncio.sleep(0.001)
            done = True
        elif doc.get('id_wd'):
            op_dict['index']['_id'] = doc.get('id_wd')
            bulk_data.append(op_dict)
            bulk_data.append(doc)
            doc = {}

        if len(bulk_data) > COMMIT_SIZE:
            res = yield from client.bulk(index='dbpedia',
                          body=bulk_data,
                          refresh=False)
            if res.get('errors') == False:
                #print("added %i records" % COMMIT_SIZE)
                sys.stdout.flush()
                sys.stdout.write('#')
                bulk_data = []
                pass
        yield from asyncio.sleep(0.001)
        q.task_done()

    if bulk_data:
        res = yield from client.bulk(index='dbpedia',
                                         body=bulk_data,
                                         refresh=False)
    if res.get('errors') == False:
        sys.stdout.flush()
        sys.stdout.write('#')
        pass
    print("ClEAN EXIT")

@asyncio.coroutine
def object_looper(obj, q):
    for i, records in enumerate(obj.loop()):
        #time.sleep(1)
        #doc = interlanguage_links.prepare_es_doc(records)
        if records:
            obj = {}
            for record in records:
                for item in records[record]:
                    key = list(item.keys())[0]
                    value = item[key]
                    obj[key] = value
                if obj:
                    doc = interlanguage_links.prepare_es_doc(obj)
                    if i % COMMIT_SIZE == 0:
                        sys.stdout.flush()
                        sys.stdout.write('?')
                    yield from q.put(doc)
        yield from asyncio.sleep(0.0001)
    yield from q.put("STOP!")


loop = asyncio.get_event_loop()
#loop.set_debug(True)
tasks = [
    asyncio.ensure_future(object_looper(interlanguage_links, q)),
    #asyncio.ensure_future(object_looper(labels, q)),
    asyncio.ensure_future(indexer_looper(q)),
    #asyncio.ensure_future(object_looper(disambiguations))
    ]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
client.transport.close()
print('\n')

'''

loop = asyncio.get_event_loop()
#loop.set_debug(True)
tasks = [
    #asyncio.ensure_future(object_looper(interlanguage_links, q)),
    asyncio.ensure_future(object_looper(labels('nl'), q)),
    asyncio.ensure_future(object_looper(labels('en'), q)),
    asyncio.ensure_future(indexer_looper(q)),
    #asyncio.ensure_future(object_looper(disambiguations))
    ]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

'''
logger.info('file("%s").class("%s") Initialized.' % (__file__, __name__))

