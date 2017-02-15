# -*- coding: utf-8 -*-

from booksearch.protocols.sru import SRU
from booksearch.formats.dc import DC

ENDPOINT_HOSTNAME = 'sru.bibsys.no'
ENDPOINT_PATH = '/search/biblioholdings'

COUNTRY_CODE = 'NOR'


class NB():
    """ Interface to Nasjonalbiblioteket, National Library of Norway catalog via SRU """

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
                return
            return response
        return

    @property
    def failed(self):
        return self.error
