#/usr/bin/python
# -*- coding: utf-8 -*-
#
# bl.py
#
# Copyright (c) 2014-2019 WillemJan Faber
#
# For licence information see LICENCE.txt,
# in the toplevel directory of this project.
#
# WARNING, in this code I'm calling os.remove,
# this is to cleanup any 'PyZ3950_parsetab.py'
# files, generated form importing PyZ3950.

# TODO: Move __del__ to protocols.z3950

import os

from booksearch.formats.marc import MARC
from booksearch.protocols.z3950 import Z3950


ENDPOINT_HOSTNAME = 'jsru.kb.nl'
ENDPOINT_PORT = 200
ENDPOINT_DBNAME = 'sru'

COUNTRY_CODE = 'GBR'


class BL():
    """ Interface to British Library catalog via Z39.50 """

    global ENDPOINT_HOSTNAME, \
           ENDPOINT_PORT, \
           ENDPOINT_DBNAME, \
           COUNTRY_CODE

    z3950 = False
    error = False

    countrycode = COUNTRY_CODE
    supported_formats = {"marc" : MARC()} 

    def __init__(self):
        self.z3950 = Z3950(ENDPOINT_HOSTNAME,
                ENDPOINT_PORT, ENDPOINT_DBNAME)

    def query(self, query):
        return ["not done yet"]
        '''
        if self.sru:
            response = self.sru.query(query)
            if self.sru.failed:
                return
        return
        '''

        def __del__(self):
            print 'died'

    @property
    def failed(self):
        return self.error

    @staticmethod
    def __del__():
        cleanup_z3959 = ['PyZ3950_parsetab.pyc',
                         'PyZ3950_parsetab.py']
        for fname in cleanup_z3959:
            if os.path.isfile(fname):
                try:
                    os.remove(fname)
                except:
                    pass
