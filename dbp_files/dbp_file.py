#!/usr/bin/env python

import fileinput
import logging
import os
import re


LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'


class DBP_file():
    PATH = '/home/aloha/nobackup/dbp/' #'/opt3/dbpedia/downloads.dbpedia.org/2015-04/'
    FILENAME = 'disambiguations_nl.ttl'
    LINK_LINE_PATTERN = re.compile(r'^<http:\/\/nl.dbpedia.org\/resource\/(.+?)>.+')

    regex_list = [
        {'id_nl' : re.compile(r'^<http:\/\/nl.dbpedia.org\/resource\/(.+?)>.+')},
        {'id_nl' : re.compile(r'.+<http:\/\/nl.dbpedia.org\/resource\/(.+?)>.+')},
        {'id_en' : re.compile(r'^.+<http:\/\/dbpedia.org\/resource\/(.+?)>.+')},
        {'id_en' : re.compile(r'.+<http:\/\/dbpedia.org\/resource\/(.+?)>.+')},
        {'id_wd' : re.compile(r'.+<http:\/\/www.wikidata.org\/entity\/(Q\d+?)>.+')},
        {'id_wd' : re.compile(r'.+<http://wikidata.dbpedia.org/resource/(Q\d+?)>.+')},
        {'title'  : re.compile('.+"(.*)"@\w\w .$')}
    ]

    line_nr = 0
    record_count = 0

    def __init__(self, loglevel=logging.DEBUG, *args, **kwargs):
        #self.regex = re.compile(self.LINK_LINE_PATTERN)

        self.logger = logging.getLogger(self.__class__.__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(loglevel)

        self.logger.info('initialized.')


    @staticmethod
    def normalize(input_str):
        '''
        Normalize given input to lowercase, and remove . _–- tokens.

        >>> normalize("A. Bertols-Apenstaartje")
        "a bertols apenstaartje"
        '''

        if input_str.find('.') > -1:
            input_str = input_str.replace('.', ' ')
        if input_str.find('-') > -1:
            input_str = input_str.replace('-', ' ')
        if input_str.find('_') > -1:
            input_str = input_str.replace('_', ' ')
        if input_str.find('   ') > -1:
            input_str = input_str.replace('   ', '  ')
        if input_str.find('  ') > -1:
            input_str = input_str.replace('  ', ' ')
        if input_str.find('\u2013') > -1:
            input_str = input_str.replace('\u2013', ' ')

        input_str = input_str.strip()
        input_str = input_str.lower()

        return input_str


    def loop(self, primary_key='id_nl', nr_of_records=10):
        all_results = []

        fname = self.PATH + self.FILENAME
        self.logger.info('Loop starting with file: %s' % fname)

        if not os.path.isfile(fname):
            self.logger.error('Could not open %s for reading' % fname)
            yield (-1, -1)

        current_id = ''
        records = {}

        for line in fileinput.FileInput(files=[fname],
                                        openhook=fileinput.hook_encoded('utf-8')):
            self.line_nr += 1
            results = []

            # Try all available regexes to get info from line
            for reg in self.regex_list:
                for regex in reg:
                    values = []
                    result = reg[regex].match(line)

                    if result:
                        # In order to create records from snipplets of info
                        # we have to group it, using primary_key
                        if regex == primary_key and not current_id == result.groups()[0]:
                            if current_id and all_results:
                                records[current_id] = all_results
                            current_id = result.groups()[0]
                            all_results = []

                        for value in result.groups():
                            if not value in values:
                                values.append(value)

                        if not {regex: values} in results:
                            results.append({regex : values})
                            results.append({"linenr": self.line_nr})

            if results:
                for item in results:
                    if item and not item in all_results:
                        all_results.append(item)

            if records and len(records) % nr_of_records == 0:
                self.record_count += len(records)
                #self.logger.info("Yielding %i records, current linenr: %i" % (len(records), self.line_nr))
                yield records
                records = {}

        if records:
            self.record_count += len(records)
            yield(records)
        fileinput.close()
        self.logger.info("Done")
        #inished lines:%i records:%i", (self.line_nr, self.record_count))

if __name__ == '__main__':
    DBP_file = DBP_file()
    for v, p in DBP_file.loop():
        print(v, p)
