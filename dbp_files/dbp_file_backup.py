#!/usr/bin/env python

import fileinput
import logging
import os
import re


LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'

'''
re.compile(r'<([^<]+?)> <([^<]+?)> <([^<]+?)> .\n')
re.compile(r'<([^<]+?)> <([^<]+?)> <([^<]+?)> .\n')
re.compile(r'<([^<]+?)> <([^<]+?)> <([^<]+?)> .\n')
re.compile(r'<([^<]+?)> <([^<]+?)> <([^<]+?)> .\n')
re.compile(r'<([^<]+?)> <([^<]+?)> <([^<]+?)> .\n')
re.compile(r'<([^<]+?)> <([^<]+?)> <([^<]+?)> .\n')
re.compile(r'<([^<]+?)> <[^<]+?> "(.*)"@(\w\w) .\n')
2016-06-09 09:14:00,842 Interlanguage_links INFO     line_nr: 3424      line: <http://nl.dbpedia.org/resource/Alexandrië> <http://www.w3.org/2002/07/owl#sameAs> <http://ko.dbpedia.org/resource/알렉산드리아> .



'''


class DBP_file():
    PATH = '../dbpedia_index/current/nl/' #'/opt3/dbpedia/downloads.dbpedia.org/2015-04/'
    FILENAME = 'disambiguations_nl.ttl'
    LINK_LINE_PATTERN = re.compile(r'^<http:\/\/nl.dbpedia.org\/resource\/(.+?)>.+')

    line_nr = 0

    def __init__(self, loglevel=logging.DEBUG):
        self.regex = re.compile(self.LINK_LINE_PATTERN)

        self.logger = logging.getLogger(self.__class__.__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(loglevel)

        self.logger.info("initialized.")

    def loop(self):
        fname = self.PATH + self.FILENAME
        self.logger.info("Loop starting with file: %s" % fname)

        if not os.path.isfile(fname):
            self.logger.error("Could not open %s for reading" % fname)
            yield (-1, -1)

        for line in fileinput.FileInput(files=[fname],
                                        openhook=fileinput.hook_encoded("utf-8")):
            self.logger.info("line_nr: %i\tline: %s" % (self.line_nr, line))
            self.line_nr += 1




            result = self.regex.match(line)
            values = []

            if result:
                for i in range(3):
                    print(result.groups())
                    if result.group(i) and not result.group(i) == line:
                        values.append(result.group(i))
                self.logger.info("line_nr: %i\tyielding: %s " %
                                 (self.line_nr, ','.join(values)))
                yield ([v for v in values])
            else:
                self.logger.warning("No regex match for %s" % line.strip())

        fileinput.close()

if __name__ == '__main__':
    DBP_file = DBP_file()
    for v, p in DBP_file.loop():
        print(v, p)
