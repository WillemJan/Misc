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

import argparse
import datetime
import httplib
import logging
import pprint
import Queue
import re
import threading
import time

from bson.json_util import loads
from oai_client import OaiClient
from pymongo import MongoClient

KRANTEN_OAI_BASE_URL = "http://services.kb.nl/mdo/oai"

LINK_SERVICE_HOST = "145.100.58.33"
LINK_SERVICE_PORT = "80"

LINK_SERVICE_CONTEXT_PATH = "/link/"

LINK_SERVICE_BASE_URL = "http://" + LINK_SERVICE_HOST
LINK_SERVICE_BASE_URL += ":" + LINK_SERVICE_PORT + LINK_SERVICE_CONTEXT_PATH

# D(ebug): read existing records from production db, print to screen
# P(roduction): read existing records from production db, save to production db
# T(est): read exiting records from test db, save to test db
MODE = "P"

MONGO_HOST = "192.87.165.3"

NUM_THREADS = 220

if MODE == "D":
    NUM_THREADS = 1

URL_QUEUE_SIZE = 1000000

# Content of the reference field ("ls" for LinkService).
REFERENCE = "ls-2015-08-3"

ID_NAMESPACE = '{http://purl.org/dc/elements/1.1/}identifier'

# Setup a logging handler
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

if MODE == "D":
    hdlr = logging.FileHandler('out.log')
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)

if MODE == "D":
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.INFO)


def get_urls(url_queue, resumption_token=''):
    if resumption_token:
        client = OaiClient(KRANTEN_OAI_BASE_URL, resumption_token)
    else:
        client = OaiClient(KRANTEN_OAI_BASE_URL)

    while not client.is_done():
        try:
            records = client.harvest("DDD", "didl")
            log.info(client.resumption_token)
        except Exception as e:
            log.error("Exception while performing OAI-PMH request \
                    (exception: %s), sleeping %d seconds before \
                    retry" % (e, 6))
            time.sleep(6)
            continue

        if records:
            for r in records:
                # Get the URLs for the full-text files
                for i in r.iter('{info:srw/schema/1/dc-v1.1}dcx'):
                    url_node = i.find(ID_NAMESPACE)

                    if url_node is None:
                        log.debug("DCX does not contain identifier, skipping")
                        continue

                    if not url_node.text.split(':')[-1].startswith('a') or not url_node.text.startswith('http://'):
                        continue

                    url = url_node.text
                    url += ':ocr'

                    # Add the ocr url to the queue, to be pickup by the
                    # process_urls thread.
                    url_queue.put(url)
                    # log.debug("Adding url %s to queue" % url)

        # Take it easy if there are enough url's in the que
        while url_queue.qsize() > URL_QUEUE_SIZE:
            log.info("URL queue size > %i")
            time.sleep(0.1)


def process_urls(url_queue, nir_collection, ir_collection):
    '''
    Manage threads with request to link service.
    '''
    thread_list = []

    # if thread slots are available flag is set
    thread_available = threading.Event()
    for thread_num in range(NUM_THREADS):
        thread_list.append(threading.Thread(target=get_links,
                                            args=(url_queue, 
                                                  thread_num,
                                                  thread_available,
                                                  nir_collection,
                                                  ir_collection)))
        thread_list[thread_num].daemon = True
        thread_list[thread_num].start()

    thread_total_count = 0

    while True:
        thread_available.wait()
        thread_available.clear()
        for thread_num in range(NUM_THREADS):
            if not thread_list[thread_num].is_alive():
                log.debug("Replacing thread: %i" % thread_num)
                thread_list[thread_num].join(0.01)
                thread_list.pop(thread_num)
                thread_list.append(threading.Thread(target=get_links,
                                                    args=(url_queue,
                                                          thread_num,
                                                          thread_available,
                                                          nir_collection,
                                                          ir_collection)))
                thread_list[-1].daemon = True
                thread_list[-1].start()
                thread_total_count += 1
                log.debug("Replacing thread done: %i" % thread_num)
                log.info("Total done: %i" % thread_total_count)


def get_links(url_queue, i, thread_available, nir_collection, ir_collection):
    '''
    Get the links for the supplied URL from the link service.
    '''
    while url_queue.empty():
        time.sleep(1)
        log.debug("The get_links queue is empty, sleeping for 1 second(s)")

    url = url_queue.get()
    link_service_full_url = "%s?url=%s&context=false" % (LINK_SERVICE_BASE_URL, url)
    link_service_url = "%s?url=%s&context=false" % (LINK_SERVICE_CONTEXT_PATH, url)

    try:
        log.debug("Going to get URL %s" % link_service_full_url)

        conn = httplib.HTTPConnection(LINK_SERVICE_HOST)
        conn.request("GET", link_service_url)
        response = conn.getresponse().read()
        conn.close()

        log.debug("Got response from link service: %s" % response)
        result = loads(response)
        result["url"] = url

        # Store the links in the enrichment db.
        store_links(result["url"], result["linkedNEs"], ir_collection, nir_collection)
    except Exception as e:
        log.error("Error trying to get link for url %s (exception: %s)" % (url, e))
        # This sleep has the effect of throttling the number of requests (somewhat)
        # in case of a persistent error condition; mainly to protect the resolver from
        # being swamped by requests.
        time.sleep(2)
    finally:
        thread_available.set()


def store_links(url, links, ir_collection, nir_collection):
    '''
    Store links returned by the link service in the enrichment db.
    '''
    json_ir_struct = {}
    json_ir_struct["resourceUri"] = url
    json_ir_struct["links"] = []

    for l in links:
        log.debug("Link to be stored: %s" % l)
        if "error" in l:
            log.info("Error getting NE from link service, message: %s" % l["error"])
            continue

        # First generate the NIR record.
        json_nir_struct = {}
        json_nir_struct["links"] = []
        json_nir_link_struct = {}
        json_nir_link_struct["status"] = "OK"
        json_nir_link_struct["linkType"] = "DBP"
        json_nir_link_struct["contentType"] = "application/json"
        json_nir_link_struct["reference"] = REFERENCE
        json_nir_link_struct["relType"] = "sameAs"
        json_nir_link_struct["altType"] = ""
        json_nir_link_struct["lang"] = get_dbpedia_lang(l["link"])
        json_nir_link_struct["datestamp"] = datetime.datetime.now()
        json_nir_link_struct["id"] = get_dbpedia_id(l["link"])
        json_nir_struct["links"].append(json_nir_link_struct)

        # Store the NIR record.
        add_nir(nir_collection, json_nir_struct)

        # Add the link to the IR record.
        json_ir_link_struct = {}
        json_ir_link_struct["status"] = "OK"
        json_ir_link_struct["linkType"] = "NIR"
        json_ir_link_struct["reference"] = REFERENCE
        json_ir_link_struct["objectName"] = l["name"]
        json_ir_link_struct["relType"] = "relation"
        json_ir_link_struct["altType"] = ""
        json_ir_link_struct["datestamp"] = datetime.datetime.now()
        json_ir_link_struct["id"] = "DBP:" + get_dbpedia_id(l["link"])
        json_ir_link_struct["neString"] = l["ne"]

        if l.get("p"):
            json_ir_link_struct["confidence"] = float(l["p"])

        json_ir_struct["links"].append(json_ir_link_struct)

    # Store the IR record, if any.
    if json_ir_struct["links"]:
        add_ir(ir_collection, json_ir_struct)
    else:
        log.info("Warning: Record empty " + url)


def add_ir(collection, doc):
    '''
    Store IR record if conditions are met.
    '''
    log.debug("Updating/Adding IR: %s" % doc)

    query = {'resourceUri': doc['resourceUri']}
    record = collection.find_one(query)

    if not record:
        if MODE == "D":
            debug.info("No existing IR entry found, adding %s" % doc)
        else:
            log.info("Writing to db for " + doc['resourceUri'])
            collection.insert(doc)
    else:
        to_remove = []
        for k in record['links']:
            if k['reference'].startswith('ls-') or k['reference'].startswith('kranten-'):
                #record['links'].remove(k)
                to_remove.append(k)
                log.debug("Removing link %s from record %s with old reference %s" % (k['id'], record['resourceUri'], k['reference']))

        for k in to_remove:
            record['links'].remove(k)

        for l in doc['links']:
            record['links'].append(l)

        if MODE == "D":
            log.debug("Add IR: %s" % record)
        else:
            if len(record['links']) > 0:
                collection.update(query, {"$set": {"links": record['links']}})
            else:
                log.info("Warning, nothing written to db for " + doc['resourceUri'])


def add_nir(collection, doc):
    '''
    Store NIR record if conditions are met.
    '''
    log.debug("NIR add check")

    disj = []
    for l in doc['links']:
        disj.append({'links.id': l['id']})

    query = {'$or': disj}
    record = collection.find_one(query)

    # log.debug("Current NIR record : %s" % record)

    if not record:
        if MODE == "D":
            debug.info("No existing NIR entry found, adding %s" % doc)
        else:
            collection.insert(doc)
    else:
        new_record = False
        for link in doc["links"]:
            # Check if the current 'id' is not allready in the record.
            if not link["id"] in [i["id"] for i in record["links"]]:
                link['datestamp'] = datetime.datetime.now()
                record['links'].append(link)
                new_record = True
            
        if new_record:
            if MODE == "D":
                log.debug("Add NIR: %s" % record)
            else:
                collection.update(query, {"$set": {"links": record['links']}})
        else:
            log.debug("NIR nothing to add")
        

def get_dbpedia_lang(url):
    '''
    Extract the language from the DBP URL
    '''
    if url.startswith("http://dbpedia"):
        return "en"
    else:
        lang_code_ind = 7
        return url[lang_code_ind:lang_code_ind+2]


def get_dbpedia_id(url):
    '''
    Extract DBP identifier from URL
    '''
    last_slash = url.rfind("/")
    return url[last_slash + 1:]


def get_mongo_collections(host):
    '''
    Get handles for the two MongoDb collections
    '''
    connection = MongoClient(host)

    if MODE == "P" or MODE == "D":
        db = connection.links
    else:
        db = connection.links_test

    return [db["nir"], db["ir"]]


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', required=False,
                        help='the OAI-PMH resumption token',
                        metavar='resumption token')

    args = parser.parse_args()
    resumption_token = vars(args)['r']
    [nir_collection, ir_collection] = get_mongo_collections(MONGO_HOST)
    url_queue = Queue.Queue()

    if resumption_token:
        oai_thread = threading.Thread(target=get_urls,
                                      args=(url_queue, resumption_token))
    else:
        oai_thread = threading.Thread(target=get_urls,
                                      args=(url_queue,))
    oai_thread.start()
    mongo_thread = threading.Thread(target=process_urls,
                                    args=(url_queue, nir_collection, ir_collection))
    mongo_thread.start()

if __name__ == "__main__":
    main()
