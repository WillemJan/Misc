#!/usr/bin/env python3

from  disambiguations import disambiguations
#from .labels_en_uris import *
#from .labels_nl import *
#from .redirects import *

import asyncio

     
@asyncio.coroutine
def disambig():
    return (yield from disambiguations())


loop = asyncio.get_event_loop()
loop.run_until_complete(disambig())
#await asyncio.ensure_future(disambig(), loop=loop)



