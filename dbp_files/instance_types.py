#!/usr/bin/env python

import re

from .dbp_file import DBP_file

LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'

class Instance_types(DBP_file):
    FILENAME = 'disambiguations_nl.ttl'
    LINK_LINE_PATTERN = re.compile(r'<([^<]+?)> <([^<]+?)> <([^<]+?)> .\n')
    regex = re.compile(LINK_LINE_PATTERN)

if __name__ == '__main__':
    disambiguations = Disambiguations()
    for v, p in disambiguations.loop():
        print(v, p)
