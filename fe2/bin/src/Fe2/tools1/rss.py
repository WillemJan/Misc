# -*- coding: utf-8 -*-
"""
    The basic rss functionality, using speedparser for speed ;)

    :class:`~Fe2.tools.rss`
"""

from pprint import pprint
from speedparser import parse
from urllib import urlopen
import os

import Fe2.tools.log

__version__ = "1.1"


class Rss():
    """
        Basic rss handler.
    """
    def __init__(self):
        self.log = create_logger(__name__)

    @staticmethod
    def _test_speedparse():
        """
            >>> test_speedparse()
            ['feed', 'bozo', 'version', 'encoding', 'entries']
        """
        data = urlopen("http://pypi.python.org/pypi?%3Aaction=rss").read()
        print(parse(data).keys())
