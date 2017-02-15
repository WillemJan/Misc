# -*- coding: utf-8 -*-

from booksearch.formats.dc import DC
from booksearch.formats.mods import MODS
from booksearch.protocols.sru import SRU

ENDPOINT_HOSTNAME = 'z3950.loc.gov'
ENDPOINT_PATH = 'voyager'
ENDPOINT_PORT = '7090'

COUNTRY_CODE = 'USA'


class LOC():
    """ Interface to Library of Congress catalog via SRU """

    global ENDPOINT_HOSTNAME, \
           ENDPOINT_PATH, \
           ENDPOINT_PORT, \
           COUNTRY_CODE

    sru = False
    error = False

    countrycode = COUNTRY_CODE
    supported_formats = {"dc": DC(), "mods": MODS()}

    def __init__(self):
        self.sru = SRU(ENDPOINT_HOSTNAME,
                       ENDPOINT_PATH,
                       ENDPOINT_PORT)

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
