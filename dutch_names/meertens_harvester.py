#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyright © 2013 Willem Jan Faber (http://www.fe2.nl) All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.
* Neither the name of “Fe2“ nor the names of its contributors may be used to
  endorse or promote products derived from this software without specific prior
  written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import os
import json
import urllib
import string
import pickle
import logging
import random

from lxml import etree
from StringIO import StringIO
from pprint import pprint

class MeertensFirstname:
    def __init___(self):
        if os.path.isfile(self.CACHE):
            log.debug('Getting firstnames cache from %s' % self.CACHE)
            with open(self.CACHE) as fh:
                self.fmale = pickle.load(fh)



class MeertensFirstnameHarvester:
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

                print('M',k,sorted(self.female.keys())[-10:])
                print('F',k,sorted(self.male.keys())[-10:])

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
            
 

logging.basicConfig()
log = logging.getLogger("dutchnames")
log.setLevel(logging.DEBUG)
meertens = MeertensFirstnameHarvester()
