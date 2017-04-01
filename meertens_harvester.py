#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:author: Willem Jan Faber
:licence: LGPLv2 or LGPLv3.

This program is licensed under the LGPLv2 or LGPLv3 license,
for more info see <http://www.gnu.org/licenses/>.
"""

import os
import json

from lxml import etree
from StringIO import StringIO

from pprint import pprint
#from twitter import Twitter

import urllib
import string
import pickle
import logging
import random
import threading

class MeertensFirstname:
    def __init___(self):
        if os.path.isfile(self.CACHE):
            log.debug('Getting firstnames cache from %s' % self.CACHE)
            with open(self.CACHE) as fh:
                self.fmale = pickle.load(fh)



class MeertensFirstnameHarvester:
    """

        Harvester for the meertens names database.

        Creates two seperate pickle files for dutch names,
        that are either female or male and occurring more than four times.

        
        Source: http://www.meertens.knaw.nl

        Hint: Do not run this, download the results from http://data.fe2.nl/

    """

    BASEURL = 'http://www.meertens.knaw.nl/nvb/naam/bevat/%s'
    BASEURL1 = 'http://www.meertens.knaw.nl/nvb/naam/pagina%i/bevat/%s'

    CACHE_F = '/tmp/names_m'
    CACHE_M = '/tmp/names_f'

    male = {}
    female = {}

    klinkers = ['a','oe','o','i','e']

    def __init__(self):
        for k in self.klinkers:
            url = self.BASEURL % k
            self._fetch_page(url)

            log.debug('Writing %i firstnames to cache %s' % (len(self.female.keys()) + len(self.male.keys()), self.CACHE_M))

            with open(self.CACHE_F, 'wb') as fh:
                pickle.dump(self.male, fh)

            with open(self.CACHE_M, 'wb') as fh:
                pickle.dump(self.female, fh)

            for i in range(26665):
                url = self.BASEURL1 % (i,k)
                if not self._fetch_page(url):
                    break

                log.debug('Writing %i firstnames to cache %s' % (len(self.female.keys()) + len(self.male.keys()), self.CACHE_M))
                with open(self.CACHE_F, 'wb') as fh:
                    pickle.dump(self.female, fh)

                with open(self.CACHE_M, 'wb') as fh:
                    pickle.dump(self.male, fh)


    def _fetch_page(self,url):
        try:
            html = urllib.urlopen(url).read()
            log.debug('Reading %s' % url)
            parser = etree.HTMLParser()
            tree = etree.parse(StringIO(html), parser)
            self._parse_tds(tree.xpath('//td'))
            return True
        except:
            return False

    def _parse_tds(self,tds):
        """ Parse the meertens result page using xpath """
        for i in range(1, 16):
            nr = i * 3
            name = tds[nr].xpath('a')[0].text.encode('utf-8').replace('(','').replace(')','')
            male = tds[nr+1].text.split(' ')[-1]
            female = tds[nr+2].text.split(' ')[-1]

            if not name in [self.male.keys() + self.female.keys()]:
                if male == '-':
                    male = 0
                if female == '-':
                    female = 0

                if int(female) > int(male) and int(female) > 4:
                    self.female[name] = female
                elif int(female) > 1:
                    self.female[name] = female
                else:
                    if int(male) > int(female) and int(male) > 4:
                        self.male[name] = male
                    elif int(male) > 1:
                        self.male[name] = male


if __name__ == '__main__':
    logging.basicConfig()
    log = logging.getLogger("dutchnames")
    log.setLevel(logging.DEBUG)
    meertens = MeertensFirstnameHarvester()
