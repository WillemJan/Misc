# -*- coding: utf-8 -*-
#
# uc.py
#
# Copyright (c) 2014-2019 WillemJan Faber
#
# For licence information see LICENCE.txt in the toplevel directory of this project.
#




from booksearch.protocols.sru import SRU
from booksearch.formats.dc import DC

ENDPOINT_HOSTNAME = 'www.unicat.be'
ENDPOINT_PATH = 'sru'

COUNTRY_CODE = 'BEL'


class UC():
    """ Interface to UniCat - Belgian university libraries and the Royal Library catalog via SRU """

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
