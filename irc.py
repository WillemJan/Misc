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


import re
import random
import urllib
import lxml.html

from twisted.internet import protocol
from twisted.words.protocols import irc

import Fe2.tools.log
from Fe2.tools.solr import Solr
import Fe2.tools.commons as commons

__version__ = "1.1"


class Bot(irc.IRCClient):
    """ Prutshot a hot bot.\n
    at this moment in time, i'm good at, \n
    extracting title's from youtube, vinemo links.\n
    following query commands are supported: \n
    prutshot: img: Moon (Wikicommons image)\n
    prutshot: news: find (Fuzzy solr query (local news rss))\n
    Have a nice day, the Sirius Cybernetics Corporation. \n"""

    log = Fe2.tools.log.create_logger(__name__)  # log
    prutsers = []

    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        """" Signed ON """
        greeting = ["worlds", "trees", "birds", "ants", "cats",
                    "toads", "spiders", "dogs", "seas", "gulls",
                    "monkeys", "bees", "webz", "channelz", "you", "ppl"]
        self.join(self.factory.channel)
        self.log.info("Entered %s as %s." % (self.factory.channel,
                                             self.nickname,))
        self.say(self.factory.channel,
            str("Hello %s!" % random.choice(greeting)))
        self.sendLine('WHO %s' % self.factory.channel)

    def irc_RPL_WHOREPLY(self, *nargs):
        self.prutsers.append(nargs[1][2])

    def joined(self, channel):
        """ Joined function.
        :param channel: Channel name. """
        self.channel = channel
        self.log.info("Joined %s." % channel)

    def privmsg(self, user, channel, msg):
        sentences = ["Flopop!", "No flopping on the grass.",
                 "If flop then make some boiled leaves.",
                 "Flopout!", "On the flop again.",
                 "You realy know how to flop it",
                 "I am floppiefied.", "I demand another shrubbery."]

        self.log.info("%s:\t%s" % (user, msg))  # Log the message
        solr = Solr('http://localhost:8983/solr/core1/', self.log)
        if msg.startswith("!new news"):
            result = solr.query('*:*&fl=title,url&sort=timestamp+desc')
            if result.hits:
                for i in range(0,3):
                    msg = ""
                    msg += result.docs[i]["title"]+" , ".encode('utf-8')
                    msg += result.docs[i]["url"].encode('utf-8')
                    self.say(self.factory.channel, str(msg.encode('ascii', 'ignore')))
        if msg.startswith("!news "):
            result = solr.query(urllib.quote(msg.replace('!news ', '')).strip()+'&fl=title,url&sort=timestamp+desc')

            if result.hits:
                msg = "Found %s hits\n" % str(result.hits).encode('utf-8')
                msg += result.docs[0]["title"]+" , ".encode('utf-8')
                msg += result.docs[0]["url"].encode('utf-8')
                self.say(self.factory.channel, str(msg.encode('ascii', 'ignore')))
        if msg.startswith(self.nickname + ":"):
            if msg.lower().find('help') > -1:
                self.say(self.factory.channel, self.__doc__)
            if msg.lower().startswith(self.nickname + ': img:'):
                image = commons.WikiImage(msg.lower().replace(self.nickname + ': img:', '').strip())
                if image.result:
                    if channel == self.nickname:
                        self.log.info(user.split('!')[0])
                        if user.split('!')[0] in self.prutsers:
                            self.say(user, image.result)
                        else:
                            self.say(self.factory.channel, "extruder! " +user)
                    else:
                        self.say(self.factory.channel, image.result)

        if re.search("flo*p", msg):  # Flop routine
            self.say(self.factory.channel, str(random.choice(sentences)))

        if msg.find("http://vimeo.com/") > -1 and not channel == self.nickname:  # vinemo search
            try:
                start = msg.find('http://vimeo.com/')
                end = msg.find('http://vimeo.com/') + 25
                data = lxml.html.parse(urllib.urlopen(urllib.quote(msg[start:end])))
            except:
                data = False
            if data:
                for item in (data.xpath('//head')[0].getchildren()):
                    if item.tag == "meta":
                        prop = (item.get('property', ''))
                        if prop == "og:description":
                            line = "Vimeo omschrijving:%s" % \
                                        str(item.values()[1].encode('utf-8'))
                            self.say(self.factory.channel, line)
                        if prop == "og:title":
                            line = "Vimeo title: %s" % \
                                        str(item.values()[1].encode('utf-8'))
                            self.say(self.factory.channel, line)

        if msg.find('youtu.be') > -1:
            msg = "https://www.youtube.com/watch?v=" + msg.replace("youtu.be")
        if msg.find("https://www.youtube.com/watch") > -1 or \
            msg.find("http://www.youtube.com/watch") > -1 and\
            not channel == self.nickname:
            try:
                params = msg.split('?')[1].split('&')
            except:
                params = []

            for param in params:
                youtube_hash = False
                if param.split('=')[0] == 'v':
                    youtube_hash = param.split('=')[1]
                if youtube_hash:
                    try:
                        url = "https://www.youtube.com/watch?v=%s" % urllib.quote(youtube_hash)
                        data = lxml.html.parse(
                                urllib.urlopen(url)
                               )
                        for item in (data.xpath('//head')[0].getchildren()):
                            if item.tag == "meta":
                                prop = item.get('property', '')
                                if prop == "og:description":
                                    self.say(self.factory.channel, "JijBuis omschrijving: " + str(item.values()[1].encode('utf-8')))
                                if prop == "og:title":
                                    self.say(self.factory.channel, "JijBuis title: " + str(item.values()[1].encode('utf-8').decode('utf-8')))
                    except:
                        pass

class BotFactory(protocol.ClientFactory):
    """
        This part of the Bot creates the initial connection.
    """
    log = Fe2.tools.log.create_logger(__name__)  # log
    protocol = Bot

    def __init__(self, channel, nickname='prutshot'):
        """ Set nickname and channel.

        :param channel: Channel to join.
        :param nickname: Nickname to use, defaults to prutshot.
        """
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        """ Connection Lost.

        :param connector: Twisted connector to reconnect to.
        :param reason: Text string containing the disconnect reason.
        """
        self.log.info("Lost connection (%s), reconnecting." % (reason))
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        """ Connection Failed.

        :param connector: Twisted connector to reconnect to.
        :param reason: Text string containing the disconnect reason.

        """
        self.log.info("Could not connect: %s" % (reason))


def prutshot():
    """
    .. function:: Fe2.tools.irc.prutsbot()

        Joins #pruts as prutshot :)
    """
    from twisted.internet import reactor

    chan = "pruts"  # Channel to join.
    reactor.connectTCP('irc.freenode.net', 6667, BotFactory('#' + chan))
    reactor.run()

if __name__ == "__main__":
    bot = prutshot()
