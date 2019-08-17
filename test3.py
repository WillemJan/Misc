#!/usr/bin/env python3.5

import sys
import time
import asyncio
import logging
import time
from asyncio import Queue
from elasticsearch_async import AsyncElasticsearch

from dbp_files import *
from es_helpers import *

from pprint import pprint

       
logger = logger(__name__, 'debug')
logger.info('file("%s").class("%s") Initialized.' % (__file__, __name__))

q = Queue()


# ES
es = ElasticsearchHelper(port='9200',
                         loglevel='critical')
es.create_index(delete_first=True)
#es.create_index(delete_first=True)
COMMIT_SIZE = 500
# /ES


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

interlanguage_links = Interlanguage_links()
interlanguage_links.PATH = PATH

client = AsyncElasticsearch()

@asyncio.coroutine
def indexer_looper(q):
    bulk_data = []
    done = False
    doc = {}
    done_counter = 0

    while not done:
        size = q.qsize
        doc = ''
        if size:
            doc = yield from q.get()
        if isinstance(doc, str):
            yield from asyncio.sleep(0.0001)
            done_counter += 1
            if done_counter == 2:
                done = True
        elif doc and doc.get('id_wd'):
            bulk_data.append({"index": {"_index": 'dbpedia', "_type": 'dbpedia', '_id' : doc.get('id_wd')}})
            bulk_data.append(doc)
            doc = {}
        else:
            bulk_data.append({"index": {"_index": 'dbpedia', "_type": 'dbpedia', '_id' : doc.get('id')}})
            bulk_data.append(doc)
        if int(len(bulk_data) / 2) >= COMMIT_SIZE:
            res = yield from client.bulk(index='dbpedia',
                          body=bulk_data,
                          refresh=True)
            if res.get('errors') == False:
                sys.stdout.flush()
                sys.stdout.write('#')
                bulk_data = []
            else:
                logger.info("Error while indexing %i records" % len(bulk_data))
        if size:
            q.task_done()

    if bulk_data:
        res = yield from client.bulk(index='dbpedia',
                                         body=bulk_data,
                                         refresh=False)
    if res.get('errors') == False:
        pass
    print("ClEAN EXIT")


@asyncio.coroutine
def object_looper(obj, q):
    for i, records in enumerate(obj.loop(nr_of_records=COMMIT_SIZE)):
        for j, doc in enumerate(obj.prepare_es_doc(records)):
            if doc:
                sys.stdout.flush()
                sys.stdout.write('?')
                yield from q.put(doc)
        yield from asyncio.sleep(0.0001)
    yield from q.put("STOP!")


loop = asyncio.get_event_loop()
tasks = [
    asyncio.ensure_future(object_looper(labels, q)),
    asyncio.ensure_future(object_looper(interlanguage_links, q)),
    asyncio.ensure_future(indexer_looper(q)),
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

logger.info('file("%s").class("%s") Initialized.' % (__file__, __name__))
'''
