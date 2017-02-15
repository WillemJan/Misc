#!/usr/bin/env python

from booksearch.endpoints import endpoints

for endpoint in endpoints:
    print endpoints[endpoint].countrycode
    print dir(endpoints[endpoint])
    e = endpoints[endpoint]()
    print dir(e)
