#/usr/bin/python
# -*- coding: utf-8 -*-
#
# response.py
#
# Copyright (c) 2014-2019 WillemJan Faber
#
# For licence information see LICENCE.txt,
# in the toplevel directory of this project.
#

class ResultSet():
    numberOfRecords = 0
    error = True

    raw_response = u""

    is_json = False
    is_xml = False

    def __init__(self):
        pass

    @property
    def hits(self):
        return self.hits
