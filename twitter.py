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

import json
import os
import re
import socket
import sys
import urllib

import guess_language
import hashlib
import Image

from lxml import etree
from StringIO import StringIO
from pprint import pprint

class TwitterImage:
    CACHE_ORG = 'img_org'
    CACHE_THUMB = 'img_thumb'
    CACHE_MEDIA = 'img_media'

    def __init__(self, twitter):
        self.image = None
        self.size = None

        if twitter.image:
            for dirname in [self.CACHE_MEDIA,
                           self.CACHE_THUMB,
                           self.CACHE_ORG]:
                if not os.path.isdir(dirname):
                    os.mkdir(dirname)

            if not os.path.isdir(self.CACHE_THUMB):
                os.mkdir(self.CACHE_THUMB)

            self.path_to_file = os.path.join('img_org',
                    twitter.name) + '.png'

            if not os.path.isfile(self.path_to_file):
                if self._get_image(twitter.image,
                        twitter.name):
                    self._scale_image(twitter.name)

            if os.path.isfile(self.path_to_file):
                self.image = Image.open(self.path_to_file)
                self.size = self.image.size

            if twitter.media:
                for (i, media) in enumerate(twitter.media):
                    if self._get_image(media, twitter.name + str(i) , self.CACHE_MEDIA):
                        print('media!', media)

    def _get_image(self, image_url, name, path=False, known = []):
        if not path:
            path = self.CACHE_ORG
        if not os.path.isfile(path + os.sep + name + '.png'):
            data = urllib.urlopen(image_url).read()
            if not hashlib.md5(data).hexdigest() in known:
                if len(data) > 10000:
                    fh = open(path + os.sep + name + '.png', 'wb')
                    fh.write(data)
                    fh.close()
                    return(hashlib.md5(data).hexdigest())
        else:
            print('skip')
        return(False)

    def _scale_image(self, name):
        outfile = self.CACHE_THUMB + os.sep + name + '.png'
        im = Image.open(self.CACHE_ORG + os.sep + name + '.png')
        im = im.convert('LA')
        im.thumbnail((200,200), Image.ANTIALIAS)
        im.save(outfile, "PNG")

class Twitter:
    def __init__(self, name, data):
        self.name = name
        self._reset()

        self._parse_data(data)
        if self.image:
            self.image_data = TwitterImage(self)
        #import pdb
        #pdb.set_trace()

    def _reset(self):
        self.at_mentions = []
        self.at_reply = []
        self.bio = ""
        self.data = {}
        self.image = ""
        self.image = None
        self.lang_guess = []
        self.location = ""
        self.timestamp = []
        self.media = []
        self.tweets = []

    def _parse_data(self, data):
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(data), parser)
        for link in tree.xpath('//a'):
            if link.get('class') == 'profile-picture media-thumbnail':
                if not link.get('href').find('default') > -1:
                    self.image = link.get('href')
            if link.get('class') == 'twitter-atreply pretty-link':
                self.at_reply.append(link.get('href'))

        for link in tree.xpath('//p[@class="bio "]'):
            if link.text and link.text.strip():
                self.bio = link.text.strip()

        for link in tree.xpath('//p[@class="js-tweet-text"]'):
            if link.text.strip():
                self.tweets.append(unicode(link.text.strip()))

        regex = re.compile('@[a-zA-Z]*\s')
        for tweet in self.tweets:
            self.lang_guess.append(guess_language.guessLanguage(tweet))
            if regex.findall(tweet):
                for at_mention in regex.findall(tweet):
                    self.at_mentions.append(at_mention)
            if tweet.split(' ')[-1].startswith('@'):
                self.at_mentions.append(tweet.split(' ')[-1])

        for link in tree.xpath('//span[@class="_timestamp js-short-timestamp js-relative-timestamp"]'):
            self.timestamp.append(link.get('data-time'))

        for link in tree.xpath('//p[@class="location-and-url"]'):
            if link is not None:
                for loc in link.iterchildren():
                    if loc.text and loc.text.strip() and len (loc.text.strip()) > 2:
                        self.location = loc.text.strip()

        for link in tree.xpath('//span[@class="media-thumbnail"]'):
            if link.get('data-resolved-url-large'):
                self.media.append(link.get('data-resolved-url-large'))

    @property
    def json(self):
        data = {}
        data["name"] = self.name
        data["media"] = self.media
        data["location"] = self.location
        data["bio"] = self.bio
        data["at_reply"] = [i[1:] for i in set(self.at_reply)]
        data["tweets"] = self.tweets
        data["lang_guess"] = self.lang_guess
        data["timestamp"] = self.timestamp

        try:
            data["image"] = self.image
            data ["image_width"] = self.image_data.size[0]
            data ["image_height"] = self.image_data.size[1]
        except:
            pass
        return(data)


    @property
    def nr_of_tweets(self):
        return(len(self.tweets))

    @property
    def nr_of_media(self):
        return(len(self.tweets))

    @property
    def nr_of_atreply(self):
        return(len(self.at_reply))

    def __repr__(self):
        return '<feed>%s</feed>' % self.name

def main(arg):
    #name = arg[1].split('/')[-1].split('.')[0]
    #fh = open ('/home/aloha/tw.txt', 'r')
    #
    for dirn in os.listdir('.'):
        if os.path.isdir(dirn):
            for filen in os.listdir(dirn + '/'):
                tw = Twitter(filen)
                if tw.tweets:
                    print(tw.json)

if __name__ == "__main__":
    main(sys.argv)
