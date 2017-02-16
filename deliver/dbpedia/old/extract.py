#!/usr/bin/env python3

import dbpedia

LANG = 'nl'

dbpedia_label = {   'label' : 'http://www.w3.org/2000/01/rdf-schema#label',
                    'abstract' : 'http://dbpedia.org/ontology/abstract',
                    'comment' : 'http://www.w3.org/2000/01/rdf-schema#comment'
                }



if __name__ == "__main__":
    i=0


    dbp = dbpedia.DBpedia()
    resource = dbp.next()

    while resource:
        prefLabel = False
        prefAbstract = False
        prefComment = False
        
        print("See also : ")
        for item in dbp.resource_json.keys():
            if not item == dbp.resource_id:
                if item.startswith('http://dbpedia.org/resource/'):
                    print(item.split('/')[-1].replace('_', ' '))
        print()
        if dbp.resource_id in dbp.resource_json.keys():
            for item in dbp.resource_json[dbp.resource_id].keys():
                comment = extract_from_resource(dbp.resource_json[dbp.resource_id], 'comment')
                abstract = extract_from_resource(dbp.resource_json[dbp.resource_id], 'abstract')
                '''

                if item.find('http://www.w3.org/2000/01/rdf-schema#label') > -1:
                    for label in dbp.resource_json[dbp.resource_id]['http://www.w3.org/2000/01/rdf-schema#label']:
                        if label['lang'] == 'nl':
                            prefLabel = label['value']
                    if not prefLabel:
                        for label in dbp.resource_json[dbp.resource_id]['http://www.w3.org/2000/01/rdf-schema#label']:
                            if label['lang'] == 'en':
                                prefLabel = label['value']

                if item.find('http://dbpedia.org/ontology/abstract') > -1:
                    for abstract in dbp.resource_json[dbp.resource_id]['http://dbpedia.org/ontology/abstract']:
                        if abstract['lang'] == 'nl':
                            prefAbstract=abstract['value']
                    if not prefAbstract:
                        for abstract in dbp.resource_json[dbp.resource_id]['http://dbpedia.org/ontology/abstract']:
                            if abstract['lang'] == 'en':
                                prefAbstract=abstract['value']

                if item.find('http://www.w3.org/2000/01/rdf-schema#comment') > -1:
                    prefComment = False
                    for comment in dbp.resource_json[dbp.resource_id]['http://www.w3.org/2000/01/rdf-schema#comment']:
                        if comment['lang'] == 'nl':
                            prefComment=comment['value']
                    if not prefComment:
                        for comment in dbp.resource_json[dbp.resource_id]['http://www.w3.org/2000/01/rdf-schema#comment']:
                            if abstract['lang'] == 'en':
                                prefComment=comment['value']
                '''

        if not prefLabel:
            prefLabel=dbp.resource_id.split('/')[-1]

        print(prefLabel, '\n', prefAbstract, '\n' , prefComment)

    
        resource = dbp.next()
        if i>3: break
        i+=1
