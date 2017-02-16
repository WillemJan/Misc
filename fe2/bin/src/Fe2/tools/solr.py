# -*- coding: utf-8 -*-
"""
    Solr basic class

    supports uploading documents via json handler.

    :author: Willem Jan Faber.
             Testing..
    :class:`~Fe2.tools.solr`
"""

import os
import json

from httplib2 import Http
from urllib import quote

import Fe2.tools.log

__version__ = "1.1"

class Solr():
    """
        Basic solr handler.
    """
    def __init__(self, url = "http://localhost:8983/solr/core0/", log=None):
        if log:
            self.log = log
        else:
            self.log = Fe2.tools.log.create_logger(__name__)

        self.url = url
        self.log.info("Starting solrhandler using: %s" % url)

    def post_data(data):
        """
            Post data to solr in json format.

            >>> solr = Solr()
            >>> response = solr.query("*:*")
        """
        http = Http(timeout=10)
        url = self.url + "update/json"
        self.log.info("Posting data to url %s" % url)
        headers, response = http.request(data, url,
                                            method="POST",
                                            body=json.dumps(data),
                                            headers={'Content-type':
                                                     'application/json',
                                                     'connection': 'close'})
        return(response)

    def query(query=None):
        if not query:
            query = "*:*"
        url = self.url + "select/?q=%s&wt=json" % quote(query)
        self.log.info("Reading url %s" % url)
        http = Http(timeout=10)
        headers, response = http.request(url=url, method="GET")
        return(json.loads(response))
