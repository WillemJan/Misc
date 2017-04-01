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

from lxml import etree
from StringIO import StringIO

from twitter import Twitter

import urllib
import string
import pickle
import logging
import random
import threading
class TwitterParse(threading.Thread):
    TWEET_PATH = 'tweets'
    IMG_PATH = 'fmale'

    def __init__(self, name_list, nr):
        threading.Thread.__init__(self)
        self.nr = nr
        alpha = [letter.upper() for letter in string.letters if letter.islower()]

        if not os.path.isdir(self.TWEET_PATH):
            os.makedirs(self.TWEET_PATH)
            for dirname in alpha:
                os.makedirs(self.TWEET_PATH+os.sep+dirname)

        if not os.path.isdir(self.IMG_PATH):
            os.makedirs(self.IMG_PATH)

        self.name_list = name_list
        self.setDaemon(True)

    def run(self):
        while not self.name_list.empty():
            name = self.name_list.get()
            data = urllib.urlopen('http://twitter.com/%s' % name).read()
            tw = Twitter(name, data)
            print tw.json
            #fh = open(self.TWEET_PATH + os.sep + name[0] + os.sep + name, 'w')
            #    fh.write(data)
            #    fh.close()
            #    return data
            #except:
            #    log.debug('Twitter error!')
            #    return False
            #else:
            #    return False


class SurName():
    current_page = 1
    nr_of_pages = 2
    name_list = []

    CACHE = '/tmp/surnames'
    URL = 'http://nl.geneanet.org/genealogie/%s/Familienaam.php'

    def __init__(self):
        if os.path.isfile(self.CACHE):
            log.debug('Getting surnames cache from %s' % self.CACHE)
            fh = open(self.CACHE)
            self.name_list = pickle.load(fh)
            fh.close()
        else:
            self.get_surnames()
            for self.current_page in range(2, int(self.nr_of_pages)):
                self.get_surnames()
            log.debug('Writing %i surnames to cache %s' % (len(self.name_list), self.CACHE))
            fh = open(self.CACHE, 'w')
            pickle.dump(self.name_list, fh)
            fh.close()

    def random(self):
        return(random.sample(self.name_list, 1)[0])

    def get_surnames(self):
        url = self.URL % str(self.current_page)
        log.debug('getting surnames from %s' % url)
        html = urllib.urlopen(url).read()
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(html),parser)

        for link in tree.xpath('//a'):
            if link.get('class'):
                if link.get('class') == 'see-more':
                    self.name_list.append(link.text.lower())
            else:
                if link.text and link.text.isdigit() and int(link.text) > self.nr_of_pages:
                    self.nr_of_pages = int(link.text)

class FirstName:
    current_page = 0
    name_list = []
    alpha = [letter.upper() for letter in string.letters if letter.islower()]

    CACHE = '/tmp/firstnames'
    URL = 'http://babynamen.infosnel.nl/voornamenlijst.php?page=%s'

    def __init__(self):
        if os.path.isfile(self.CACHE):
            log.debug('Getting firstnames cache from %s' % self.CACHE)
            fh = open(self.CACHE)
            self.name_list = pickle.load(fh)
            fh.close()
        else:
            self._get_names()
            for self.current_page in range(1, int(self.nr_of_pages)):
                self._get_names()
            self._parse_names()
            log.debug('Writing %i firstnames to cache %s' % (len(self.name_list), self.CACHE))
            fh = open(self.CACHE, 'w')
            pickle.dump(self.name_list, fh)
            fh.close()

    def random(self):
        return(random.sample(self.name_list, 1)[0])

    def _parse_names(self):
        name_list = []
        alpha_pointer = 0
        alpha_pointer_max = 1
        start = False

        for pointer in range(0, len(self.name_list)):
            if self.name_list[pointer][0] == self.alpha[0]:
                start = True
            if start:
                if pointer + 1 < len(self.name_list):
                    pointer_max = pointer + 1

                if self.name_list[pointer][0] == self.alpha[alpha_pointer] \
                    and self.name_list[pointer_max][0] == self.name_list[pointer][0]:
                        name_list.append(self.name_list[pointer])
                elif self.name_list[pointer][0] == self.alpha[alpha_pointer_max]:
                    if alpha_pointer_max + 1 < len(self.alpha):
                        alpha_pointer += 1
                        alpha_pointer_max += 1
                    else:
                        alpha_pointer += 1
                        name_list.append(self.name_list[pointer])
                        break

        self.name_list  = name_list

    def _get_names(self):
        url = self.URL % str(self.current_page)
        log.debug('Getting firstnames from %s' % url)
        html = urllib.urlopen(url).read()
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(html),parser)
        names = False
        for link in tree.xpath('//a'):
            if (link.text).isdigit():
                self.nr_of_pages = link.text
            else:
                names = True

            if names:
                if link.text[0] in self.alpha:
                    self.name_list.append(link.text)


if __name__ == "__main__":
    #names = DutchNameGrabber()
    #twitter_parser = TwitterParse(names.name_list)
    from Queue import Queue

    logging.basicConfig()
    log = logging.getLogger("dutchnames")
    log.setLevel(logging.DEBUG)

    surnames = SurName()
    firstnames = FirstName()

    f = open('names.json','r')
    names = json.loads( f.read() )
    firstnames.name_list = []
    for name in names:
        if names[name] == 'female':
            firstnames.name_list.append(name)

    dates = ['77','78','79','80','81','76', '75']
    seen = set([])
    que = []
    q = Queue()

    for i in range(10):
        rnd = random.random()

        surname = surnames.random().capitalize().replace(' ','_')
        firstname = firstnames.random()
        firstname1 = firstnames.random()

        if rnd < 0.3:
            name = firstname + random.sample(dates, 1)[0]
        elif rnd > 0.3 and rnd < 0.7:
            name = firstname + firstname1
        else:
            #name = surname + random.sample(dates, 1)[0]
            name = surname + '_' + firstname + random.sample(dates, 1)[0]

        if not name in seen:
            seen.add(name)
            q.put(name)

    for i in range(4):
        que.append(TwitterParse(q,i))
        que[i].start()

    for i in range(4):
        que[i].join()

