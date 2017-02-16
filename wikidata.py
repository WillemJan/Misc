#!/usr/bin/env python3

import sys

name=sys.argv[1]
req =request.Request('http://en.wikipedia.org/wiki/' + name )

try:
    print(request.urlopen(req))
except error.URLError as e:
    print((e.code))

