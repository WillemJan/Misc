#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

import time

import codecs
import requests

from urlparse import urlparse

from Queue import Queue
from threading import Thread

howtoUse = """%s: missing file operand
Try '%s --help' for more information.\n"""

errFileNotFound = """%s: cannot stat ‘%s’
No such file.\n"""

SKETCHY = "http://localhost:8000/"

def extract_links(*argv):
    all_links = []

    # Parse input filename.
    if len(argv[0]) == 2:
        fname = argv[0][1]
    else:
        sys.stderr.write(howtoUse % (argv[0][0],argv[0][0]))
        sys.exit(-1)

    # Exit if file not found.
    if not os.path.isfile(fname):
        sys.stderr.write(errFileNotFound % (argv[0][0], fname))
        sys.exit(-1)

    # Open file, and search for url patterns
    fh = codecs.open(fname, 'rb', 'utf-8')
    for line in fh.read().split('\n'):
        line = unicode(line.lower())
        if line.startswith('http://') or line.startswith('www.'):
            url = line.split(' ')[0].strip()
            if url.endswith('.'):
                url = url[:-1]
            if not url.startswith('http://'):
                url = 'http://' + url
            if not url in all_links and not url + '/' in all_links:
                all_links.append(url)
        else:
            while line.find('http://') > -1:
                pos = line.find('http://')
                url = line[pos:].split(' ')[0]
                if url.endswith('.'):
                    url = url[:-1]
                line = line[pos+len(url):]
                if not url in all_links and not url + '/' in all_links:
                    all_links.append(url)
            while line.find('www.') > -1:
                pos = line.find('www.')
                url = line[pos:].split(' ')[0]
                if url.endswith('.'):
                    url = url[:-1]
                if not url.startswith('http://'):
                    url = 'http://' + url
                line = line[pos+len(url):]
                if not url in all_links and not url + '/' in all_links:
                    all_links.append(url)
    return sorted(all_links)

def worker():
    while not done:
        while not q.empty():
            url = q.get()
            print "worker working on" + url

            req = requests.get(SKETCHY + '?url=%url&type=sketch' % url)
            if req.status_code == 200:
                print dir(req)
    
            '''
            o = urlparse(url)
            outfile = '/tmp/' + o.netloc.split(':')[0].replace('.', '_') + ".png"
            s,e = os.popen2('cutycapt --url=%s --out=%s' % (url, outfile))
            e.read()
            '''



            q.task_done()
        time.sleep(0.01)

if __name__ == '__main__':
    all_links = extract_links(sys.argv)
    q = Queue()
    t = []
    done = False
    for i in range(10):
        t.append(Thread(target=worker))
        t[i].daemon = True
        t[i].start()

    for url in all_links:
        try:
            r = requests.head(url=url, timeout=1.1)
            if r.status_code == 200:
                q.put(url)
                print "adding url " + url + "\n"
        except requests.exceptions.InvalidURL as e:
            pass
        except requests.exceptions.ConnectionError as e:
            pass
        except requests.exceptions.Timeout as e:
            pass
        except requests.exceptions.MissingSchema as e:
            pass


    done = True
    print "all done!"

    for i in range(10):
        t[i].join()
