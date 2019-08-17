#!/usr/bin/env python3.5


try:
    from .dbp_file import DBP_file
except:
    from dbp_file import DBP_file

import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                os.pardir))
from es_helpers import *


es = ElasticsearchHelper()


class Labels(DBP_file):
    FILENAME = 'labels_nl.ttl'
    ES_HANDLER = False
    LANG = 'nl'
    ID_FORMAT = '%s_%i'

    def prepare_es_doc(self, record):
        prop_list = ['id_nl', 'title', 'linenr']
        docs = []

        for i in [v for v in record.values()]:
            props = {}

            for key in i:
                for prop in prop_list:
                    if key.get(prop):
                        value = key.get(prop)
                        if isinstance(value, list):
                            value = value.pop()
                        props[prop] = value

            title = set()
            title.add(props.get('title'))
            disambig = 0
            wdid = props.get('id_' + self.LANG)

            if wdid:
                if wdid.find('(') > -1:
                    disambig = 1
                    first_part = wdid.split('(')[0].replace('_',' ').strip()
                    title.add(first_part)
                    title.add(DBP_file.normalize(first_part))
                    last_part = wdid.replace(first_part,'').replace('_(',' ').replace(')','')
                    title.add(DBP_file.normalize(last_part))
                if not wdid in title:
                    title.add(wdid)
                if not DBP_file.normalize(wdid) in title:
                    title.add(DBP_file.normalize(wdid))
            
                
                doc = {}

                doc['id_' + self.LANG] = wdid
                new_id = self.ID_FORMAT % (self.LANG, props.get('linenr'))

                doc['id'] = new_id
                doc['title'] = [i for i in set([t.replace('_', ' ') for t in title])]
                doc['title_str'] = [i for i in set([t.replace('_', ' ') for t in title])]
                doc['disambig'] = disambig

                docs.append(doc)
        return docs
                
            



        '''
        for key in obj.keys():
            for item in obj[key]:
                id_nl = ''
                if not item.get('id_' + self.LANG):
                    continue
                myid = item.get('id_' + self.LANG)[0]
                results = []
                if myid:
                    result = es.search('id_%s:"%s"' % (self.LANG, id_nl))
                    if result.get('total') == 0:
                        for item in ([(list(i.keys())[0], i.get(list(i.keys())[0])) for i in obj[key]]):
                            if item[0] == 'linenr':
                                line_number = int(item[1])
                                results.append({"id": new_id})
                            else:
                                results.append({item[0]: item[1]})

                        all_results.append(results)
        return all_results
        '''

if __name__ == '__main__':
    labels = Labels()
    from pprint import pprint
    import sys

    for p in labels.loop():
        for label in labels.prepare_es_doc(p):
            pprint(label)
        break
