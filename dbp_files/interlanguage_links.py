#!/usr/bin/env python

import re

try:
    from .dbp_file import DBP_file
except:
    from dbp_file import DBP_file


LOG_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'

class Interlanguage_links(DBP_file):
    FILENAME = 'interlanguage_links_nl.ttl'

    @staticmethod
    def prepare_es_doc(obj):
        prop_list = ['id_nl', 'id_wd', 'id_en']

        '''

        {'Geluk_(emotie)': [{'id_nl': ['Geluk_(emotie)']}, {'id_wd': ['Q8']}, {'id_en': ['Happiness']}], 'Triskaidekafobie': [{'id_nl': ['Triskaidekafobie']}, {'id_wd': ['Q13']}, {'id_en': ['Triskaidekaphobia']}], 'Imagine_(John_Lennon)': [{'id_nl': ['Imagine_(John_Lennon)']}, {'id_wd': ['Q1971']}, {'id_en': ['Imagine_(John_Lennon_song)']}], 'Leet': [{'id_nl': ['Leet']}, {'id_wd': ['Q1337']}, {'id_en': ['Leet']}], 'Mayakalender': [{'id_nl': ['Mayakalender']}, {'id_wd': ['Q2012']}, {'id_en': ['Maya_calendar']}], 'Getal_van_het_Beest': [{'id_nl': ['Getal_van_het_Beest']}, {'id_wd': ['Q666']}, {'id_en': ['Number_of_the_Beast']}], 'Lolcat': [{'id_nl': ['Lolcat']}, {'id_wd': ['Q56']}, {'id_en': ['Lolcat']}], 'Jack_Bauer_(personage)': [{'id_nl': ['Jack_Bauer_(personage)']}, {'id_wd': ['Q24']}, {'id_en': ['Jack_Bauer']}], 'Paul_Otlet': [{'id_nl': ['Paul_Otlet']}, {'id_wd': ['Q1868']}, {'id_en': ['Paul_Otlet']}], 'Heelal': [{'id_nl': ['Heelal']}, {'id_wd': ['Q1']}, {'id_en': ['Universe']}]}
        '''
        docs= []
        for i in [v for v in obj.values()]:
            props = {}
            for key in i:
                for prop in prop_list:
                    if key.get(prop):
                        props[prop] = key.get(prop).pop()

            if props.get('id_nl'):
                id_nl = props['id_nl']
            if props.get('id_wd'):
                id_wd = props['id_wd']
            if props.get('id_en'):
                id_en = props['id_en']

            title = set()
            disambig = 0

            if props.get('id_nl'):
                if id_nl.find('(') > -1:
                    disambig = 1
                    first_part = id_nl.split('(')[0].replace('_',' ').strip()
                    title.add(first_part)
                    title.add(DBP_file.normalize(first_part))
                    last_part = id_nl.replace(first_part,'').replace('_(',' ').replace(')','')
                    title.add(DBP_file.normalize(last_part))

                if not id_nl in title:
                    title.add(id_nl)
                    title.add(DBP_file.normalize(id_nl))

            if props.get('id_en'):
                id_en = id_en
                title.add(id_en)
                title.add(DBP_file.normalize(id_en))

                if id_en.find('(') > -1:
                    disambig = 1
                    first_part = id_en.split('(')[0].replace('_','').strip()
                    title.add(first_part)
                    title.add(DBP_file.normalize(first_part))
                    last_part = id_en.replace(first_part,'').replace('_(','').replace(')','')
                    title.add(DBP_file.normalize(last_part))

            doc = {}
            doc['id_nl'] = id_nl

            if doc.get('id_en'):
                doc['id_en'] = id_en

            doc['id_wd'] = id_wd
            doc['title'] = [i for i in set([t.replace('_', ' ') for t in title])]
            doc['title_str'] = [i for i in set([t.replace('_', ' ') for t in title])]
            doc['disambig'] = disambig

            docs.append(doc)

        return docs
        

if __name__ == '__main__':
    from pprint import pprint
    interlanguage_links = Interlanguage_links()
    for p in interlanguage_links.loop():
        for i in interlanguage_links.prepare_es_doc(p):
            print(i)
