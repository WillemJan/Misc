# -*- coding: utf-8 -*-
"""
    The basic rss functionality, using speedparser for speed ;)

    :class:`~Fe2.tools.time`
"""

import os
from datetime import datetime, timedelta
import time

__version__ = "1.1"


class Time():
    """
        Misc time functions.
    """
    def __init__(self):
        pass

    def epoch(self):
        epoch = time.mktime(datetime.now().timetuple()) * 1000
        return(epoch)

    def epoch_to_human(self, epoch=None):
        if not epoch:
            epoch = datetime.now().time()
        time.strftime("%a, %d %b %Y %H:%M:%S +0000",
                      time.localtime(epoch))

    def later(self, hours=10, minutes=30):
        now = datetime.now().time()
        d1 = datetime(2000, 1, 1, now.hour, now.minute, now.second)
        d2 = d1 + timedelta(hours=hours, minutes=minutes)
        return(d2.time())
