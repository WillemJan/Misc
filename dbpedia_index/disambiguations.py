#!/usr/bin/env python

import fileinput
import os
import sys
import re

DATA_PATH = 'current/nl/'
FILENAME = 'disambiguations_nl.ttl'
LINK_LINE_PATTERN = re.compile(r'<([^<]+?)> <([^<]+?)> <([^<]+?)> .\n')
fname = DATA_PATH + FILENAME

regex = re.compile(LINK_LINE_PATTERN)


__all__ = ['disambiguations']


def disambiguations():
    for line in fileinput.input(files=[fname],
                                openhook=fileinput.hook_encoded("utf-8")):
        result = regex.match(line)
        if result:
            value, value1, value2 = result.group(0),\
                                    result.group(1),\
                                    result.group(3)
            yield(value1, value2)


if __name__ == '__main__':
    for v, p in disambiguations():
        print(v, p)
