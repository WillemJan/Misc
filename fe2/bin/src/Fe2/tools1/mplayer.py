# -*- coding: utf-8 -*-
"""
    The basic rss functionality, using speedparser for speed ;)

    :class:`~Fe2.tools.mplayer`
"""

from pprint import pprint
from urllib import urlopen
import os
import threading

import Fe2.tools.log

__version__ = "1.1"


class Mplayer(threading.Thread):
    """
        Basic mplayer handler.
    """
    def __init__(self, target):
        threading.Thread.__init__(self)
        devnull = open('/dev/null', 'w')
        self.mp = subprocess.Popen(['mplayer', '-slave', '-quiet', target],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=devnull)

    def run(self):
        self.mp.read()
