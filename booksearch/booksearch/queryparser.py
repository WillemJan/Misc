#/usr/bin/python
# -*- coding: utf-8 -*-
#
# queryparser.py
#
# Copyright (c) 2014-2019 WillemJan Faber
#
# For licence information see LICENCE.txt,
# in the toplevel directory of this project.
#

import isbnlib


def isISBN(input_str):
    ''' Checks if the given string is an ISBN number. '''

    if isbnlib.is_isbn10(input_str):
        return True
    if isbnlib.is_isbn13(input_str):
        return True

    input_str_clean = isbnlib.clean(input_str)

    if isbnlib.is_isbn10(input_str_clean):
        return True
    if isbnlib.is_isbn13(input_str_clean):
        return True

    return False
