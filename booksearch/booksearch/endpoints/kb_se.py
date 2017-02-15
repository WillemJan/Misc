# -*- coding: utf-8 -*-

from booksearch.protocols.sru import SRU
from booksearch.formats.dc import DC

ENDPOINT_HOSTNAME = 'api.libris.kb.se'
ENDPOINT_PATH = '/sru/libris'

COUNTRY_CODE = 'SWE'


class KB_SE():
    """ Interface to Libris - Swedish university and research libraries via SRU """

    global ENDPOINT_HOSTNAME, \
           ENDPOINT_PATH, \
           COUNTRY_CODE

    sru = False
    error = False

    countrycode = COUNTRY_CODE
    supported_formats = {"dc": DC()}

    def __init__(self):
        self.sru = SRU(ENDPOINT_HOSTNAME, ENDPOINT_PATH)

    def query(self, query):
        if self.sru:
            response = self.sru.query(query)
            if self.sru.failed:
                returnA
            return response
        return

    @property
    def failed(self):
        return self.error
