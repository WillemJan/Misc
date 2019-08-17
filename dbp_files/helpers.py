#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.parse
import sys

if sys.version_info <= (3, 0):
    sys.stdout.write("Sorry, requires Python 3.0 or higher.\n")
    sys.exit(1)

def id_to_text(input_str):
    '''
    Convert dbpedia identifier into a (searchable) title.

    >>> id_to_text("Albert_Einstein")
    'Albert Einstein'
    '''

    input_str = input_str.split('/')[-1].replace('>', '')
    input_str = urllib.parse.unquote(input_str).replace('_', ' ')

    return input_str


def normalize(input_str):
    '''
    Normalize given input to lowercase, and remove . _–- tokens.

    >>> normalize("A. Bertols-Apenstaartje")
    'a bertols apenstaartje'
    '''

    if input_str.find('.') > -1:
        input_str = input_str.replace('.', ' ')
    if input_str.find('-') > -1:
        input_str = input_str.replace('-', ' ')
    if input_str.find('_') > -1:
        input_str = input_str.replace('_', ' ')
    if input_str.find('   ') > -1:
        input_str = input_str.replace('   ', '  ')
    if input_str.find('\u2013') > -1:
        input_str = input_str.replace('\u2013', ' ')

    if input_str.find('  ') > -1:
        input_str = input_str.replace('  ', ' ')

    input_str = input_str.strip()
    input_str = input_str.lower()

    return input_str

'''
if __name__ == "__main__":
    import doctest
    doctest.testmod()
'''

id_to_text('a aaap')
