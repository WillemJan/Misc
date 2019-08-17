#!/usr/bin/env python

from .dbp_file import DBP_file

class Labels_en_uris(DBP_file):
    PATH = ''
    FILENAME = 'labels_en_uris_nl.ttl'

if __name__ == '__main__':
    labels_en_uris = Labels_en_uris()
    for v, p in labels_en_uris.loop():
        print(v, p)
