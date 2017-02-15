#/usr/bin/python
# -*- coding: utf-8 -*-
#
# api.py
#
# Copyright (c) 2014-2019 WillemJan Faber
#
# For licence information see LICENCE.txt,
# in the toplevel directory of this project.
#

import threading
import Queue

from .endpoints import endpoints
from .queryparser import isISBN


DEBUG = True
DEBUG_LEVEL = ""


class SearcherThread(threading.Thread):
    def __init__(self, endpoint, search_queue, result_queue):
        super(SearcherThread, self).__init__()
        self.endpoint = endpoint
        self.search_queue = search_queue
        self.result_queue = result_queue
        self.stoprequest = threading.Event()
        self.done = False
        self.setDaemon(True)

    def run(self):
        while not self.stoprequest.isSet():
            # Loop keeps checking for new
            # search querys to send to endpoint.
            query = False
            try:
                query = self.search_queue.get(True, 0.05)
            except:
                continue
            if query:
                self.result_queue.put(self.endpoint.query(query))
                self.done = True

    def join(self, timeout=2):
        self.stoprequest.set()
        super(SearcherThread, self).join(timeout)


class BookSearch():
    result_queue = Queue.Queue()
    pool = False
    search_endpoints = {}

    def __init__(self):
        pass

    def query(self, input_query):
        # 1. Small query analysis // query expansion.
        # 2. Initialize endpoints and search queue (if needed).
        if len(self.search_endpoints) == 0:
            for ep in endpoints:
                self.search_endpoints[ep] = {}
                self.search_endpoints[ep]["endpoint"] = endpoints[ep]()
                self.search_endpoints[ep]["queue"] = Queue.Queue()

        if DEBUG and DEBUG_LEVEL == 'verbose':
            for item in self.search_endpoints:
                print item, self.search_endpoints[item].query(input_query)

        # 3. Initialize search workers (if needed), and fire them up.
        if not self.pool:
            self.pool = [SearcherThread(
                        self.search_endpoints[i]["endpoint"],
                        self.search_endpoints[i]["queue"],
                        self.result_queue) for i in self.search_endpoints]

        # 4. Start all initialized search threads.
        for thread in self.pool:
            thread.start()

        # 5. Add the query to the search queue.
        for endpoint in endpoints:
            self.search_endpoints[endpoint]["queue"].put(input_query)

        # 6. Wait for results.
        done = False
        while not done:
            total_threads = 0
            for thread in self.pool:
                if thread.done:
                    total_threads += 1
                    thread.join()
                    if total_threads == len(self.search_endpoints):
                        done = True

        for endpoint in endpoints:
            result = self.result_queue.get(True)
            print "====================="
            print result
            print "====================="
