#!/usr/bin/env python3

from elasticsearch import Elasticsearch
#3from aioes import Elasticsearch


import os
import sys
from .log import logger


__all__ = ['ElasticsearchHelper']

ES_MAPPING_FILE = os.path.join(os.path.dirname(__file__),
                               'es_dbp_index_create.json')


class ElasticsearchHelper():
    '''Elastic search helper functions for indexing dbpedia dumps.'''

    INDEX_NAME = 'dbpedia'

    def __init__(self,
                 host='127.0.0.1',
                 port='9200',
                 # port='3030',
                 loghandler=None,
                 loglevel='warning'):
        """
        :arg host: Hostname or IP of the Elasticsearch server
        :arg port: Port number of the Elasticsearch server
        :arg loghandler: Log hanlder to use
        :arg loglevel: String representing the verboseness of logging
        """

        if loghandler is None:
            self.logger = logger(self.__class__.__name__, loglevel)
        else:
            self.logger = loghandler

        self.logger.info('file("%s").class("%s") Initialized.' %
                         (__file__, self.__class__.__name__))

        self.host = host
        self.port = port

        try:
            self.ES = Elasticsearch([{'host': host, 'port': port}])
        except ConnectionRefusedError:
            self.logger.fatal("Could not connect to host: %s port: %s" %
                              (host, port))
            sys.exit(-1)

        try:
            info = self.ES.info()
        except:
            self.logger.fatal("Could not connect to host: %s port: %s" %
                              (host, port))
            sys.exit(-1)

        for key in info:

            if not key == 'version':
                self.logger.info("%s %s" % (key, info.get(key)))
            else:
                self.logger.info("version: %s" % info.get(key).get('number'))
                self.logger.info("lucene_version: %s" %
                                 info.get(key).get('lucene_version'))

    def create_index(self,
                     es_mapping=ES_MAPPING_FILE,
                     delete_first=False,
                     force=False):
        """
        Create empty Elasticsearch index, from json file.

        :arg es_mapping: Path to Elasticsearch mapping file
        :arg delete_first: Boolean to express if you want to delete the index
                           if it allready exists.
        :arg force: Boolean to express if you want to force the operation
        """

        log = self.logger

        if not os.path.isfile(es_mapping):
            log.fatal("Unable to create index, file: %s missing." %
                      es_mapping)
            return False

        if self.ES.indices.exists(self.INDEX_NAME) and not (force or delete_first):
            log.info("Index: %s allready exits." % self.INDEX_NAME)
            return True

        with open(es_mapping, 'r') as fh:
            mapping = fh.read()

            if not self.INDEX_NAME == 'dbpedia':
                mapping = mapping.replace('"dbpedia":{', '"%s"' %
                                          self.INDEX_NAME)

        if force:
            delete_first = True

        if delete_first:
            try:
                response = self.ES.indices.delete(index=self.INDEX_NAME)
                log.info("Deleted index: %s host: %s port: %s" %
                         (self.INDEX_NAME, self.host, self.port))
            except:
                log.fatal("Could not delete index: %s" %
                          self.INDEX_NAME)
                sys.exit(-1)

        if not self.ES.indices.exists(self.INDEX_NAME) or force:
            if force:
                log.info("Creation of new index forced..")
            else:
                log.info("Index %s does not yet exists." %
                         self.INDEX_NAME)

            try:
                response = self.ES.indices.create(index=self.INDEX_NAME,
                                                  ignore=400,
                                                  body=mapping)
                if response.get('acknowledged'):
                    log.info("Successfully created index: %s" %
                             self.INDEX_NAME)
                    return True
                elif response.get('error'):
                    msg = ("Could not create index: %s host: %s port: %s" %
                           (self.INDEX_NAME, self.host, self.port))
                    log.fatal(msg)

                    error = response.get('error')
                    error = error.get('root_cause')[0]
                    reason = error.get('reason')
                    log.fatal("Reason: %s" % reason)
                    return False
                else:
                    msg = ("Could not create index: %s host: %s port: %s\n" %
                           (self.INDEX_NAME, self.host, self.port))
                    msg += "Unknown error accoured while creating index."
                    log.fatal(msg)
                    return False
            except:
                log.fatal("Could not create index. Error: %s" %
                          sys.exc_info()[0])
                return False

            return False


    def search(self, query):
        result = self.ES.search(index=self.INDEX_NAME, doc_type="dbpedia", q=query).get('hits')
        return result


    def id_to_id(self, id):
        '''
        Fetch a resource by one of it's secondary id's, return primary id.


        >>> id_to_id('http://resource.dbpedia.org/page/Albert_Einstein')
        'Q29832'

        >>> id_to_id('http://nl.dbpedia.org/page/Albert_Einstein')
        'Q29832'


        >>> id_to_id('Albert Einstein')
        'Q29832'
        '''
