#!/usr/bin/env python

from .dbp_file import DBP_file

class Disambiguations(DBP_file):
    FILENAME = 'disambiguations_nl.ttl'



'''
if __name__ == '__main__':
    disambiguations = Disambiguations()
    for v, p in disambiguations.loop():
        print(v, p)
'''
