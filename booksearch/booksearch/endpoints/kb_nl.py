# -*- coding: utf-8 -*-

from booksearch.formats.dc import DC
from booksearch.formats.dcx import DCX
from booksearch.protocols.sru import SRU

ENDPOINT_HOSTNAME = 'jsru.kb.nl'
ENDPOINT_PATH = 'sru'

COUNTRY_CODE = 'NLD'


class KB_NL():
    """ Interface to GGC - National Library of the Netherlands catalog via SRU 
        Current supported recordSchema/format dc, dcx
    """

    global ENDPOINT_HOSTNAME, \
           ENDPOINT_PATH, \
           COUNTRY_CODE

    sru = False
    error = False

    countrycode = COUNTRY_CODE

    supported_formats = {"dc" : DC(),
                         "dcx" : DCX()}

    def __init__(self):
        self.sru = SRU(ENDPOINT_HOSTNAME, ENDPOINT_PATH)

    def query(self, query):
        if self.sru:
            response = self.sru.query(query)
            if self.sru.failed:
                return
            return response
        return

    @property
    def failed(self):
        return self.error
