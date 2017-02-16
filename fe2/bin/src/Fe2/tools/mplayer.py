# -*- coding: utf-8 -*-
"""
    The basic mplayer functionality.
    :class:`~Fe2.tools.mplayer`
"""

from pprint import pprint
from urllib import urlopen
import os
import threading
import subprocess

import Fe2.tools.log

__version__ = "1.1"


class Mplayer(threading.Thread):
    """
        Basic mplayer handler.
    """
    def __init__(self, target):
        threading.Thread.__init__(self)
        devnull = open('/dev/null', 'w')
        target = "/home/aloha/music/music/dj shadow/Asia Born/01-send_them-cms.mp3"
        self.mp = subprocess.Popen(['mplayer', '-slave', '-quiet', target],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=devnull)
    def run(self):
        while True:
            print self.mp.communicate("get_percent_pos\n")[0]
    
#mp = Mplayer("")
#mp.start()
#
#print("here")
#try:
#    mp.join()
#except KeyboardInterrupt:
##    print("ok")
