#!/usr/bin/env python

try:
    from .dbp_file import DBP_file
except:
    from dbp_file import DBP_file


from pprint import pprint

import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                os.pardir))
from es_helpers import *

es = ElasticsearchHelper()

class Redirects(DBP_file):
    FILENAME = 'redirects_nl.ttl'

    def prepare_es_doc(self, record):

        for item in record:
            print(item, record.get(item))

if __name__ == '__main__':
    redirects = Redirects()
    for i, p in enumerate(redirects.loop()):
        for item in redirects.prepare_es_doc(p):
            if i > 10:
                sys.exit(-1)
        pprint(p)
