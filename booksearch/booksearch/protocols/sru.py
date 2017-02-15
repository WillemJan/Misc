# -*- coding: utf-8 -*-

import requests


class SRU():
    """ Fetches SRU query's and returns the response in bytes """
    baseurl = False

    query_all = 'query=%(query)s&version=1.1&operation=searchRetrieve&maximumRecords=%(maximumrecords)i&recordSchema=%(recordschema)s'
    query_isbn = 'query=ISBN=%(query)s&version=1.1&operation=searchRetrieve&maximumRecords=%(maximumrecords)i&recordSchema=%(recordschema)s'

    error = True

    def __init__(self, host=False, path=False, port=False):
        if port:
            if type(port) == int:
                port = str(port)
        else:
            port = "80"

        # Setup the basurl in this form:
        # http://{hostname}:{port}/{path}
        if not self.baseurl:
            self.baseurl = 'http://%(host)s:%(port)s/%(path)s?' % {
                    'host' : host, 'port' : port, 'path' : path}

    def query(self, query, recordschema='dc', maximumrecords=1):
        if not self.baseurl:
            return(u'')
        
        url = self.baseurl
        url += self.query_all % {'query' : query, 'recordschema' : recordschema, 'maximumrecords' : maximumrecords}
        print ("* DEBUG : " + url)
        req = requests.get(url)

        if not req.status_code == 200:
            return u''

        self.error = False
        return bytes(bytearray(req.text, encoding='utf-8'))

    def explainrecord(self):
        if not self.baseurl:
            return

        url = self.baseurl + ''

    @property
    def failed(self):
        return self.error
