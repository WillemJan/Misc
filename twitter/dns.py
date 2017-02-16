#!/usr/bin/env python
"""
$URL$
$Id$

A multi-threaded DNS query solution, originally developed to check a
large list of candidate domain names -- if no NS is present, the candidate
likely does not have a domain registration.

(C) mwatkins, a WebHostingTalk.com user. Use for any purpose you like provided
attribution is provided.
"""
# install PyDNS: http://pydns.sourceforge.net
# FreeBSD: /usr/ports/dns/py-dns

import DNS
import threading
import time
import Queue
from optparse import OptionParser

DNS.ParseResolvConf()

WORKERS = 60

def has_ns (domain):
    try:
        query = DNS.Request(domain, qtype="NS").req()
    except:
        time.sleep(0.014)
        has_ns(domain)
    status = query.header['status']
    return (domain, status)


def get_domains_from_file(path):
    return [domain.strip().decode('ascii', 'replace') for domain in open(path).readlines() if domain.strip()]


class Worker(threading.Thread):
    def __init__(self, work_queue, result_queue):
        self.__queue = work_queue
        self.__result = result_queue
        threading.Thread.__init__(self)

    def run(self):
        while 1:
            domain = self.__queue.get()
            if domain is None:
                break
            self.__result.put(has_ns(domain))

def process_domains(domains):
    work = Queue.Queue()
    result = Queue.Queue()
    for domain in domains:
        work.put(domain)
    for i in range(60):
        work.put(None)

    workers = [Worker(work, result) for i in range(60)]
    for worker in workers:
        worker.start()

    for w in workers:
        w.join()

    available = []
    unavailable = []
    while not result.empty():
        domain, status = result.get(0)
        if status == 'NXDOMAIN':
            available.append(domain)
        else:
            unavailable.append(domain)
    return available, unavailable


def run_domain_checker_main():
    global WORKERS

    parser = OptionParser()
    parser.set_description('Checks domain names for available name servers. Domain names with no name servers defined are potentially available for registration. A final check for availability against a registrarwhois API is recommended.')
    parser.add_option('-f', '--inputfile', dest='input_file', default='domains.txt', help='A file containing one domain name per line ')
    parser.add_option('-o', '--outputfile', dest='output_file', default='available.txt',help=('A file to contain the candidate domains which may be available. Note: This file is overwritten on every run.'))
    parser.add_option('-s', '--server', dest='dns_server', default=None, help='Force use of a specific name server, overriding /etc/resolve.conf.')
    parser.add_option( '-t', '--threads', dest='workers', default=10, type=int, help='Number of worker threads')
    parser.add_option( '-c', '--cache', action="store_true", dest='use_cache', default=False, help=('Use contents of <outputfile>, if it exists, as a cache.added to the cache in <outputfile>.'))

    options, args = parser.parse_args()
    domains = get_domains_from_file(options.input_file)
    cached_domains = []
    WORKERS = options.workers
    DNS.defaults['server'] = ['8.8.8.8',]
    if options.use_cache:
        try:
            cached_domains = get_domains_from_file(options.output_file)
        except IOError, e:
            print "INFO: Skipping cache", e

    domains = [domain for domain in domains if domain not in
    cached_domains]
    start = time.time()

    print "Domains to process:", len(domains)

    avail, unavail = process_domains(domains)
    fout = open(options.output_file, 'w')
    result = sorted(avail + cached_domains)
    fout.writelines(['%s\n' % domain for domain in result])
    fout.close()

    print "Available domains written to file:", len(result)
    print "Run time:", time.time() - start

if __name__ == '__main__':
    run_domain_checker_main()
