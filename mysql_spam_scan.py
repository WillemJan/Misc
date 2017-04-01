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

import logging
import MySQLdb
import os
import pickle
import random
import re
import smtplib
import socket
import sys
import time

from urlparse import urlparse

# allways have your logger to chop wood
log = logging.getLogger("mysql_spam_scan")
fh = logging.FileHandler("/var/log/mysql_spam_scan.log")
log.setLevel(logging.DEBUG)
log.addHandler(fh)


class PrutsDB():
    ''' Get the tables -> users mapping,
    try to get from /tmp/db_mapping,
    else query mysql for the mapping '''

    db = MySQLdb.connect(host="",
                         user="",
                         passwd="",
                         db="")
    mapping = {}

    def __init__(self):
        self.cur = self.db.cursor()

    def start_log(self):
        self.cur.execute("""SET GLOBAL general_log = 'ON';""")

    def stop_log(self):
        self.cur.execute("""SET GLOBAL general_log = 'OFF';""")

    def get_mapping(self):
        outfile = '/tmp/db_mapping'
        if os.path.isfile(outfile):
            try:
                cache = open(outfile, 'rb')
                self.mapping = pickle.load(cache)
                log.info('Depickled tablemappings from disk')
            except:
                log.info('Could not depickle /tmp/db_mapping')

        if not self.mapping:
            log.info('Trying to get tablemappings from database')
            self.cur.execute("SELECT * FROM mysql_db")

            for row in self.cur.fetchall():
                self.mapping[row[2]] = row[1]

            self.cur.close()
            log.info('Got tablemappings from databases')

            cache = open(outfile, 'wb')
            pickle.dump(self.mapping, cache)
            log.info('Wrote tablemappings to disk: %s' % self.outfile)


class MySQLSpamParser():
    ''' Parse the mysql log file,
    extract all INSERT and UPDATES per user,
    and mail them if spam was seen.  '''

    querys = {}
    data = False
    db_whitelist = ["roundcube", "quarantine"]

    user_whitelist = ['root', 'roundcube', 'spammert']

    spam_profiles = {'sex': ['sex', 'pussy', 'porn', 'girl'],
                     'gamble': ['casino', 'poker', 'gamble',
                     'blackjack', 'slotmachine'],
                     'shopping': ['shopping', 'free', 'online',
                     'discount', 'store', 'cheap',
                     'outlet', 'sale'],
                     'drugs': ['pharmacies', 'pills', 'looseweight'],
                     'money': ['credit', 'divident', 'stocks'],
                     'russian': ['.ru'],
                     'japan': ['.jp']}

    spam_seen = []

    def __init__(self, data, mapping):
        self.mapping = mapping
        self.data = data
        self.analyze()

    def analyze(self):
        ## FIXME : seperate class
        ## is the right solution here..
        sessions = {}
        if not self.data or len(self.data) < 100:
            sys.stdout.write("Error mysql log file to small.\n")
            sys.exit(-1)

        # connection tracking querys
        connect = re.compile('\\t\\t\s+(\d+)\sConnect\\t(\w+)@.+\son\s(\w.+)?')
        init = re.compile('\\t\\t\s+(\d+)\sInit DB\\t(\w+)$')
        quit = re.compile('\\t\\t\s+(\d+)\sQuit\\t$')

        # modification querys
        sql_prepare = re.compile('\\t\\t\s+(\d+)\sQuery\\tPREPARE\s(.+)')
        sql_set = re.compile('\\t\\t\s+(\d+)\sQuery\\tSET\s(.+)')
        sql_insert = re.compile('\\t\\t\s+(\d+)\sQuery\\tINSERT\s(.+)')

        # other stuff..
        tabs = re.compile('\\t\\t\s+(\d+)\s.+?')
        sql_select = re.compile('\\t\\t\s+(\d+)\sQuery\\tSELECT\s(.+)')

        # skip the first 3 lines..
        self.data = self.data[3:]

        log.info("Parsing %i bytes" % len(self.data))

        current_id = ''

        # I don't like big long elseif statemts either..
        for line_number, line in enumerate(self.data.split('\n')):
            if connect.match(line):
                # MySQL connect, might contain username..
                session_id = connect.match(line).group(1)
                username = connect.match(line).group(2)
                dbname = connect.match(line).group(3)

                if sql_select.match(line):
                    # Discard select lines
                    continue

                if not session_id in sessions:
                    log.info('New session id: %s' % session_id)
                    if dbname:
                        if dbname in self.mapping and not dbname in self.db_whitelist:
                            if not self.mapping[dbname] in self.user_whitelist:
                                sessions[session_id] = {
                                    'username': self.mapping[dbname],
                                    'dbname': dbname,
                                    'data': []}
                                log.info('%s: %s %s' %
                                        (session_id, dbname, self.mapping[dbname]))
                        else:
                            if not username in self.user_whitelist and not dbname in self.db_whitelist:
                                sessions[session_id] = {
                                    'username': username,
                                    'dbname': dbname,
                                    'data': []}
                                log.info('%s: %s %s' %
                                        (session_id, username, dbname))
                    else:
                        if not username in self.user_whitelist:
                            sessions[session_id] = {
                                    'username': username,
                                    'dbname': '',
                                    'data': []}
                            log.info('%s: %s' %
                                    (session_id, username))
            elif init.match(line):
                # sql init
                session_id = init.match(line).group(1)
                dbname = init.match(line).group(2)
                if dbname in self.db_whitelist:
                    continue
                if not session_id in sessions:
                    if dbname in self.mapping and not dbname in self.db_whitelist:
                        if not self.mapping[dbname] in self.user_whitelist:
                            sessions[session_id] = {
                                    'username': self.mapping[dbname],
                                    'dbname': dbname, 'data': []}
                    elif not dbname in self.db_whitelist:
                        sessions[session_id] = {
                                'username': "",
                                'dbname': dbname, 'data': []}
                else:
                    if not ('dbname' in sessions[session_id] or
                            dbname == sessions[session_id]['dbname']):
                        if not dbname in self.db_whitelist:
                            sessions[session_id]['dbname'] = dbname
                if dbname in self.mapping:
                    sessions[session_id]['username'] = self.mapping[dbname]
            elif sql_prepare.match(line):
                # sql prepare
                session_id = sql_prepare.match(line).group(1)
                if session_id in sessions:
                    sessions[session_id]['data'].append(line)
            elif sql_set.match(line):
                # sql set
                session_id = sql_set.match(line).group(1)
                if session_id in sessions:
                    sessions[session_id]['data'].append(line)
            elif sql_insert.match(line):
                # sql insert
                session_id = sql_insert.match(line).group(1)
                if session_id in sessions:
                    sessions[session_id]['data'].append(line)
            elif quit.match(line):
                # end session
                session_id = quit.match(line).group(1)
                if session_id in sessions:
                    log.info("%s: Start content rating" % session_id)
                    sessions[session_id]['session_id'] = session_id
                    self.check_content(sessions[session_id])
                    log.info("%s: End content rating" % session_id)
                    sessions.pop(session_id)
            elif tabs.match(line):
                # random stuff
                current_id = tabs.match(line).group(1)
            else:
                # random stuff
                if current_id in sessions:
                    sessions[current_id]['data'].append(line)

        # process all pending session
        for session_id in sessions:
            log.info("%s: Start rating" % str(session_id))
            sessions[session_id]['session_id'] = session_id
            self.check_content(sessions[session_id])
            log.info("%s: End rating" % str(session_id))

    def _calc_spam_type(self, urls):
        spam_type = {}
        # find out which type of spam
        for url in urls:
            for p in self.spam_profiles:
                for word in self.spam_profiles[p]:
                    if url.lower().find(word) > -1:
                        if not p in spam_type:
                            spam_type[p] = 1
                        else:
                            spam_type[p] += 1
        return(spam_type)

    def check_content(self, session):
        log.info('Checking content')
        if not ('username' in session or 'dbname' in session):
            # If usernmae or dbname is missing, move along
            return
        if not (session['username'] or session['dbname']):
            # If usernmae or dbname is missing, move along
            return
        if (session['username'] in self.user_whitelist):
            # Skip users in user whitelist
            return
        if 'data' in session and len(session['data']) < 100:
            # Don't bother to look at small sessions
            return

        urls = self._extract_urls(session['data'])
        if len(urls) < 3:
            # Spam does not come alone...
            return

        log.info('%s: Found interseting content' % session['session_id'])
        spam = self._calc_spam_type(urls)
        if spam:
            log.info('%s: Found some spam' % session['session_id'])
            self.rate_and_mail(session, urls, spam)

    def bye(self):
        log.info('bye, pep8 end')

    def rate_and_mail(self, session, urls, spam):
        for s in spam:
            # At least 2 wierd urls in a single transaction
            if spam[s] > 2:
                urls = [u.replace('.', '_') for u in urls]
                ses_id = (session['username']
                         + "_"
                         + session['dbname'])
                if not ses_id in self.spam_seen:
                    self.mail_user(session['username'],
                                   session['dbname'],
                                   spam, urls,
                                   session['data'],
                                   session['session_id'])

                    log.warn("Found spam in db: %s, \
                              owned by %s, sending warning\n" %
                             (session['dbname'], session['username']))

                    self.spam_seen.append(ses_id)

    def mail_user(self, username, dbname, spam, urls, data, session_id):
        sender = 'beheer@pruts.nl'
        receivers = [username, 'beheer@pruts.nl']
        message = """From: beheer@pruts.nl
To: %s
Cc: beheer@pruts.nl
Subject: Hoi prutster, je verstuurt spam via pruts.

Beste %s,

We willen je verzoeken de volgende database te inspecteren:

%s

Vanwege dit type spam:
\n- %s

Aangetroffen urls:
\n- %s

(en waarschijnlijk nog veel meer meuk,
zie /tmp/%s_%s op pruts voor details)

mocht dit niet kloppen,
geef het even door,

anders database gaarne afsluiten..

Alvast bedankt,

Pruts beheer.
""" % (username, username, dbname,
       "\n- ".join(spam.keys()), "\n- ".join(urls[:3]),
       username, dbname)

        smtpObj = smtplib.SMTP('localhost')
        lockfile = '/tmp/' + username + '_' + dbname

        log.info('Mail sent to %s' % username)

        # If not db is whitelisted,
        # or mail allready send..
        # alert the user for incoming spam

        if username:
            log.info('%s: Mailing %s' % (session_id, username))
        if not (dbname in self.db_whitelist or
                os.path.isfile(lockfile)):
            if not username in self.user_whitelist:
                smtpObj.sendmail(sender, receivers, message)

        fh = open(lockfile, 'wb')
        fh.write("\n".join(data))
        fh.write("\n".join(urls))
        fh.close()

    def _extract_urls(self, data):
        data = " ".join(data)
	data = data.replace("'",' ')
	data = data.replace('"',' ')
	data = data.replace('\\',' ')

        url_seen = []

        for part in data.split():
            if len(part) > 4:
                link = urlparse(part)
                if link.netloc:
                    if not link.netloc in url_seen:
                        url_seen.append(link.netloc)
        return(url_seen)


class MySQLLogCollector():
    MIN_SIZE = 1048576 * 3   # 2 megs of log should do the trick
    MAX_SIZE = 1048576 * 10  # bail out value

    def __init__(self, prutsdb):
        size = 0
        log.info("Waiting for %i bytes of data..." % self.MIN_SIZE)

        # start mysql logging
        prutsdb.start_log()
        while size < self.MIN_SIZE:
            size = os.path.getsize('/var/log/mysql/mysql.log')
            time.sleep(10)
            prutsdb.start_log()
            log.info("Got %i bytes" % size)

        # stop mysql logging
        prutsdb.stop_log()

        # Prevent this program from taking down the system
        size = os.path.getsize('/var/log/mysql/mysql.log')
        if not size > self.MAX_SIZE:
            # Read mysql log data
            fh = open('/var/log/mysql/mysql.log', 'rb')
            self.data = fh.read()
            fh.close()

        # Empty mysql log -> *zap*
        fh = open('/var/log/mysql/mysql.log', 'w')
        fh.write('')
        fh.close()

        # Empty error log
        fh = open('/var/log/mysql/error.log', 'w')
        fh.write('')
        fh.close()


def main(arg):
    lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        # Lock the processs
        lock_socket.bind('\0mysql_spam_scan')
    except socket.error:
        # Exit if locked
        log.info('mysql_spam_scan currenly locked, bye')
        sys.exit(-1)

    # Sleep random, don't sample at same time
    rnd = random.randrange(0, 140)
    log.info('About to sleep for %i min' % rnd)
    time.sleep(rnd * 60)

    # Connect to the pruts database
    pruts_db = PrutsDB()

    # Create and read the mysql log file
    log.info('Starting logcollector')
    logcol = MySQLLogCollector(pruts_db)
    log.info('Logcollector done')

    # Create the user -> table mapping
    pruts_db.get_mapping()
    mapping = pruts_db.mapping

    # Parse the log
    log.info('Pawrsing mysql log to find spam..')
    log_parser = MySQLSpamParser(logcol.data, mapping)

    log_parser.bye()  # This is here to make pep8 happy :)

if __name__ == "__main__":
    main(sys.argv)
