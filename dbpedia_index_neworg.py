#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import requests
import urllib
import urllib2
import re

from pprint import pprint

import inspect
import time

DEBUG_MAX = 1579575
DEBUG = False

if not DEBUG:
    SOLR = 'http://localhost:4040/solr/dbpedia/'  # Where the Solr endpoint lives
else:
    SOLR = 'http://localhost:4040/solr/dbpedia/'  # Where the Solr endpoint lives

SOLR_ADD = SOLR + 'update/json'  # Add-path
SOLR_UPDATE = SOLR +  'update?softCommit=true' # Update-path
SOLR_QUERY = SOLR + 'select/?'  # Query-path

DBPEDIA_NL = '../2015-04/nl/'  # Path to Dutch DBPedia dumps
DBPEDIA_EN = '../2015-04/en/'  # Path to English DBPedia dumps


def fetch_by_id(dbpedia_id):
    print("FETCH_BY_ID: " + dbpedia_id)
    if dbpedia_id.find('"') > -1 and not dbpedia_id.find(r'\"') > -1:
        dbpedia_id = dbpedia_id.replace('"', r'\"')
    query = urllib.quote(unicode(dbpedia_id).encode('utf-8'))
    if dbpedia_id.find('nl.dbpedia.org') > -1:
        url = unicode(SOLR_QUERY + "wt=json&q=id:\"" + query + '"').encode('utf-8')
    else:
        url = unicode(SOLR_QUERY + "wt=json&q=id_en:\"" + query + '"').encode('utf-8')
    print("FETCH_BY_ID: " + url)
    data = urllib.urlopen(url).read()
    data = json.loads(data)
    try:
        if data.get('response').get('numFound') > 0:
            print("FETCH_BY_ID: FOUND!")
        else:
            print("FETCH_BY_ID: NOT FOUND!")
        return data
    except:
        print("FETCH_BY_ID: did not get result")
        return False


def add_solr(doc, force=False):
    if (doc.get("id").find("disambiguation") > -1 or
            doc.get("id").find("doorverwijspagina") > -1):
        return
    data = fetch_by_id(clean_id(doc.get("id")))
    #print("*****************")
    #print (data.get('response').get('numFound'))
    #print (data.get('response').get('numFound') == 1)
    #print("*****************")


    if type(data) == type({}) and data.get("response") and data.get('response').get('numFound') == 1:
        update_doc = {}
        record = data.get('response').get('docs')[0]


        if doc.get('id_en'):
            update_doc['id_en'] = clean_id(doc.get('id_en'))
            update_doc['id'] = clean_id(record.get('id'))

        for item in doc:
            if item.startswith('id'):
                continue
            if not isinstance(doc.get(item), type({})):
                    continue
            if doc.get(item).keys() == ['add']:
                for to_add in doc.get(item).get('add'):
                    if record.get(item) == None:
                        update_doc['id'] = clean_id(record.get('id'))
                        update_doc[item] = {'add' : to_add}
                    elif type(record.get(item)) == type([]):
                        if not to_add in record.get(item):
                            update_doc['id'] = clean_id(record.get('id'))
                            update_doc[item] = {'add' : to_add}
                    elif not record.get(item) == to_add:
                        if item == 'abstract_nl':
                            if len(to_add) > len(record.get(item)):
                                update_doc['id'] = clean_id(record.get('id'))
                                update_doc[item] = {'add' : to_add}
                        else:
                            update_doc['id'] = clean_id(record.get('id'))
                            update_doc[item] = {'add' : to_add}


            if doc.get(item).keys() == ['set']:
                for to_set in doc.get(item).get('set'):
                    if record.get(item) == None:
                        update_doc['id'] = clean_id(record.get('id'))
                        update_doc[item] = {'set' : to_set}
                    elif type(record.get(item)) == type([]):
                        if not to_set in record.get(item):
                            update_doc['id'] = clean_id(record.get('id'))
                            update_doc[item] = {'set' : to_set}
                    elif not record.get(item) == to_set:
                        if item == 'abstract_nl':
                            if len(to_set) > len(record.get(item)):
                                update_doc['id'] = clean_id(record.get('id'))
                                update_doc[item] = {'set' : to_set}
                        else:
                            update_doc['id'] = clean_id(record.get('id'))
                            update_doc[item] = {'set' : to_set}
        if update_doc:
            print("UPDATE!")
            _send_to_solr(update_doc)
            update_solr()
        elif force:
            print("FORCE!")
            _send_to_solr(doc)
            update_solr()
    elif force:
        print("FORCE!")
        _send_to_solr(doc)
        update_solr()
    else:
        print("UNKNOWN STATE!")
        _send_to_solr(doc)
        update_solr()

def update_solr():
    req = urllib2.Request(url=SOLR_UPDATE)
    req.add_header('Content-type', 'application/json')
    response = urllib2.urlopen(req)

    if not response.getcode() == 200:
        print('Error while updating' % SOLR_ADD)

def id_to_text(input_str):
    input_str = input_str.split('/')[-1].replace('>', '')
    input_str = input_str.replace('_', ' ')
    return input_str

def _send_to_solr(doc):
    pprint(doc)
    doc = json.dumps([doc])
    print("SEND_TO_SOLR: " + doc)
    req = urllib2.Request(url=SOLR_ADD, data=doc)
    req.add_header('Content-type', 'application/json; charset=utf-8')

    response = urllib2.urlopen(req)
    if not response.getcode() == 200:
        print("Error while adding", doc)

def clean_id(dbpedia_id):
    #return dbpedia_id.replace('"', "\"")
    return dbpedia_id

def clean(input_str):
    input_str = urllib.unquote(input_str)
    input_str = input_str.strip()
    try:
        input_str = input_str.strip().decode('raw_unicode_escape')
    except:
        #print("FAILED")
        #print(input_str)
        pass
    return unicode(input_str)

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
    if input_str.find(u'\u2013') > -1:
        input_str = input_str.replace('\u2013', ' ')

    input_str = input_str.strip()
    input_str = input_str.lower()

    return input_str


def start():
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    now = str(time.strftime("%d-%m %H:%M:%S"))
    print("=====\n\n")
    print "Start: %s Time: %s" % (calframe[1][3], now)
    print("=====\n\n")

def stop():
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    now = str(time.strftime("%d-%m %H:%M:%S"))
    print("=====\n\n")
    print "Stop: %s Time: %s" % (calframe[1][3], now)
    print("=====\n\n")

def index_labels_nl(path):
    i = 0
    start()
    with open(path, 'r') as fp:
        for line in fp:
            if not line[0] == '<':
                continue

            i += 1
            if DEBUG and i > DEBUG_MAX:
                return

            doc = {}
            line = clean(line)
            dbpedia_id = clean_id(line.split()[0])

            if dbpedia_id.find('disambiguation') > -1 or dbpedia_id.find("doorverwijspagina") > -1:
                continue

            doc['id'] = dbpedia_id
            doc['id_nl'] = dbpedia_id
            doc['lang'] = 'nl'
            title = line.split('"')[1]

            doc['disambig'] = 0
            doc['org_title_str'] = doc['org_title'] = title

            doc['title_str'] = doc['title'] = normalize(title)
            doc['pref_title'] = doc['pref_title_str'] = title
            if len(normalize(title).split()) > 1:
                doc['lastpart_str'] = normalize(title).split()[-1]
            else:
                doc['lastpart_str'] = normalize(title)


            if dbpedia_id.find('(') > -1:
                doc['disambig'] = 1
                doc['title_str'] = [normalize(title),
                                    normalize(title.split('(')[0].strip())]
                doc['title'] = doc['title_str']
                doc['org_title_str'] = [title,
                                        title.split('(')[0].strip()]
                doc['org_title'] = doc['org_title_str']

                if len(normalize(title.split('(')[0].strip()).split()) > 1:
                    doc['lastpart_str'] = normalize(title.split('(')[0].strip()).split()[-1]
                else:
                    doc['lastpart_str'] = normalize(title.split('(')[0].strip())

            add_solr(doc, force=True)
    stop()


def index_labels_en(path):
    start()
    i = 0
    print __name__
    with open(path, 'r') as fp:
        for line in fp:
            if not line[0] == '<':
                continue

            i += 1
            if DEBUG and i > DEBUG_MAX:
                return

            dbpedia_id_en = clean_id(clean(line.split()[0]))

            if dbpedia_id_en.find('disambiguation') > -1 or dbpedia_id_en.find("doorverwijspagina") > -1:
                continue

            line = clean(line)

            result = fetch_by_id(dbpedia_id_en)
            if result:
                if not result.get('response').get('numFound') or result.get('response').get('numFound') == 0:
                    doc = {}

                    doc['id'] = dbpedia_id_en
                    doc['id_en'] = dbpedia_id_en
                    doc['lang'] = 'en'
                    doc['disambig'] = 1

                    title = line.split('"')[1]

                    doc['org_title_str'] = doc['org_title'] = title
                    doc['title_str'] = doc['title'] = normalize(title)
                    doc['pref_title'] = doc['pref_title_str'] = title

                    if len(normalize(title).split()) > 1:
                        doc['lastpart_str'] = normalize(title).split()[-1]
                    else:
                        doc['lastpart_str'] = normalize(title)

                    if dbpedia_id_en.find('(') > -1:
                        doc['disambig'] = 0
                        doc['title_str'] = [normalize(title),
                                            normalize(title.split('(')[0].strip())]
                        doc['title'] = doc['title_str']
                        doc['org_title_str'] = [title,
                                                title.split('(')[0].strip()]
                        doc['org_title'] = doc['org_title_str']

                        if len(normalize(title.split('(')[0].strip()).split()) > 1:
                            doc['lastpart_str'] = normalize(title.split('(')[0].strip()).split()[-1]
                        else:
                            doc['lastpart_str'] = normalize(title.split('(')[0].strip())

                    add_solr(doc, force=True)
        stop()


def index_interlanguage(path):
    start()

    i = 0
    with open(path, 'r') as fp:
        for line in fp:
            if not line[0] == '<':
                continue

            if DEBUG and i > DEBUG_MAX*10:
                return

            doc = {}

            if not (line.find('http://dbpedia.org/') > -1 or line.find('http://wikidata.org/entity/') > -1) or not line:
                continue

            i += 1

            dbpedia_id = clean_id(clean(line.split()[0]))

            doc = {}
            doc['id'] = dbpedia_id

            if line.find('wikidata.org') > -1:
                wd_id = line.split()[2].split('/')[-1].replace('>', '')
                doc['wd_id'] = {'set' : wd_id}
            elif line.find('http://dbpedia.org/resource/') > -1:
                dbpedia_id_en = clean_id(clean(line.split()[2]))
                doc['id_en'] = {'set' : [dbpedia_id_en]}
                title = id_to_text(dbpedia_id_en)
                doc['title'] = {'add' : [normalize(title)]}
                doc['title_str'] = {'add' : [title]}
            add_solr(doc)
    stop()

def index_disambiguations(path, lang='nl'):
    start()
    i = 0
    with open(path, 'r') as fp:
        for line in fp:
            if not line[0] == '<':
                continue

            i += 1
            if DEBUG and i > DEBUG_MAX:
                return

            line = clean(line)

            title = id_to_text(line.split()[0])
            dbpedia_id = line.split()[2]

            try:
                response = fetch_by_id(dbpedia_id)
            except:
                response = {}

            doc = {}
            doc['id'] = dbpedia_id
            doc['org_title'] = {"add": [title]}
            doc['org_title_str'] = {"add": [title]}

            doc['title'] = {"add": [normalize(title)]}
            doc['title_str'] = {"add": [normalize(title)]}

            add_solr(doc)
    stop()


def index_redirects(path):
    start()
    i = 0
    with open(path, 'r') as fp:
        for line in fp:
            if not line[0] == '<':
                continue

            i += 1
            if DEBUG and i > DEBUG_MAX:
                return

            line = clean(line)
            dbpedia_id = clean_id(clean(line.split()[2]))
            title = id_to_text(line.split()[0])

            doc = {}
            doc['id'] = dbpedia_id
            doc['title'] = {"add": [normalize(title)]}
            doc['title_str'] = {"add": [normalize(title)]}

            doc['org_title'] = {"add": [title]}
            doc['org_title_str'] = {"add": [title]}

            add_solr(doc)
    stop()


def index_infoboxproperties(path, lang='nl'):
    geboorte = ['http://nl.dbpedia.org/property/gbdat',
                'http://nl.dbpedia.org/property/geboortedatum',
                'http://nl.dbpedia.org/property/geboren',
                'http://dbpedia.org/property/birthDate',
                'http://dbpedia.org/property/dateOfBirth']

    sterfte = ['http://nl.dbpedia.org/property/sterfdatum',
               'http://nl.dbpedia.org/property/sterfdat',
               'http://nl.dbpedia.org/property/overlijddatum',
               'http://nl.dbpedia.org/property/overlijdensdatum',
               'http://dbpedia.org/property/deathDate',
               'http://dbpedia.org/property/dateOfDeath']

    dbp_nl = '<http://nl.dbpedia.org/resource/'
    dbp_en = '<http://dbpedia.org/resource/'

    start()

    i = 0
    with open(path, 'r') as fp:
        for line in fp:
            if not line[0] == '<':
                continue

            i += 1
            if DEBUG and i > DEBUG_MAX:
                return

            line = clean(line)

            dbpedia_id = clean_id(clean(line.split()[0]))

            if dbpedia_id.find('disambiguation') > -1 or dbpedia_id.find("doorverwijspagina") > -1:
                continue

            if True in [line.find(f) > -1 for f in geboorte]:
                if line.split()[2].startswith('"'):
                    dob_string = line.split()[2].split('"')[1]
                    dob = re.match('.*(\d{4}-\d{2}-\d{2}).*', dob_string)
                else:
                    dob = False

                if dob:
                    dob = dob.groups()[0].strip() + 'T00:00:00Z'
                    doc = {}
                    doc['id'] = dbpedia_id
                    doc['dob'] = {'set': [dob]}
                    doc['yob'] = {'set': [dob[:4]]}
                    add_solr(doc)

            if True in [line.find(f) > -1 for f in sterfte]:
                dbpedia_id = line.split()[0]

                if line.split()[2].startswith('"'):
                    dod_string = line.split()[2].split('"')[1]
                    dod = re.match('.*(\d{4}-\d{2}-\d{2}).*', dod_string)
                else:
                    dod = False

                if dod:
                    dod = dod.groups()[0].strip() + 'T00:00:00Z'

                    doc = {}
                    doc['id'] = dbpedia_id
                    doc['dod'] = {'set': [dod]}
                    doc['yod'] = {'set': [dod[:4]]}
                    add_solr(doc)

            if line.find('http://nl.dbpedia.org/property/volledigeNaam') > -1:
                if line.find('"') > -1:
                    name = line.split('"')[1]

                    doc = {}
                    doc['id'] = dbpedia_id
                    doc['title'] = {'add' : [normalize(name)]}
                    doc['title_str'] = {'add' : [normalize(name)]}

                    doc['org_title'] = {'add' : [name]}
                    doc['org_title_str'] = {'add' : [name]}

                    add_solr(doc)

            if line.find('http://nl.dbpedia.org/property/geslacht') > -1:
                gender = line.split()[2]
                gender = gender.replace(dbp_nl + 'Man_(geslacht)>', '"M"')
                gender = gender.replace(dbp_nl + 'Man>', '"M"')
                gender = gender.replace(dbp_nl + 'Vrouw>', '"V"')
                gender = gender.replace(dbp_nl + 'Vrouw_(geslacht)>', '"V"')
                gender = gender.replace('Man', 'M')
                gender = gender.replace('Vrouw', 'V')
                gender = gender.replace('<', '"').replace('>', '"')
                gender = gender.split('"')[1]
                gender = gender.lower()

                if gender in ['m', 'v']:
                    gender = gender.replace('v', 'f')
                    doc['id'] = dbpedia_id
                    doc['gender'] = {'set': [gender]}
                    add_solr(doc)

            if line.find('<http://dbpedia.org/property/gender>') > -1:
                gender = line.split()[2]
                gender = gender.replace(dbp_en + 'Male>', '"M"')
                gender = gender.replace(dbp_en + 'Fenale>', '"F"')
                gender = gender.replace('Male', 'M')
                gender = gender.replace('Female', 'F')

                if gender.find('"') > -1:
                    gender = gender.split('"')[1]
                else:
                    gender = ''
                gender = gender.lower()

                if gender in ['m', 'f']:
                    doc['id'] = dbpedia_id
                    doc['gender'] = {'set': [gender]}
                    add_solr(doc)
    stop()

def index_inlinks(path):
    start()
    print __name__
    prev_dbpedia_id = ''
    counter = 1
    i = 0
    with open(path, 'r') as fp:
        for line in fp:
            if not line[0] == '<':
                continue

            i += 1
            if DEBUG and i > DEBUG_MAX * 5:
                return

            dbpedia_id = clean_id(clean(line.split()[0]))
            line = clean(line)

            if dbpedia_id.find('disambiguation') > -1 or dbpedia_id.find("doorverwijspagina") > -1:
                continue

            if not prev_dbpedia_id:
                prev_dbpedia_id = dbpedia_id
                counter = 1
                doc = {}
                doc['id'] = dbpedia_id
                doc['inlinks'] = {'set': [counter]}

            if not prev_dbpedia_id == dbpedia_id:
                add_solr(doc)
                counter = 1
                prev_dbpedia_id = dbpedia_id

            doc = {}
            doc['id'] = dbpedia_id
            doc['inlinks'] = {'set': [counter]}
            counter += 1
    stop()

def index_longabstracts(path, lang='nl'):
    start()
    i = 0
    with open(path, 'rb') as fp:
        for line in fp:
            if not line[0] == '<':
                continue

            i += 1
            if DEBUG and i > DEBUG_MAX:
                return

            line = clean(line)
            dbpedia_id = clean_id(line.split()[0])

            if dbpedia_id.find('disambiguation') > -1 or dbpedia_id.find("doorverwijspagina") > -1:
                continue

            abstract = clean(line.split('"')[1])

            doc = {}
            doc['id'] = dbpedia_id
            doc['abstract_' + lang] = {'set': [abstract]}

            add_solr(doc, True)
    stop()

def index_instance_types(path):
    '''
    Index instance type's like Person // Actor //..
    '''
    start()
    i = 0
    prev_line = 'a b'
    doc = {}
    with open(path, 'r') as fp:
        for line in fp:
            if not line[0] == '<':
                continue

            i += 1
            if DEBUG and i > DEBUG_MAX:
                return

            line = clean(line)

            if line.split()[0].find('disambiguation') > -1 or line.split()[0].find("doorverwijspagina") > -1:
                continue

            if prev_line.split()[0] == line.split()[0]:
                dbpedia_id = prev_dbpedia_id
            else:
                if doc:
                    add_solr(doc)
                    update_solr()
                dbpedia_id = clean_id(line.split()[0])

            instance_type = line.split()[2]
            instance_type = instance_type.split('/')[-1].replace('<', '').replace('>', '').strip()

            doc = {}
            doc['id'] = dbpedia_id
            doc['schemaorgtype'] = {'add': [instance_type]}

            prev_line = line
            prev_dbpedia_id = dbpedia_id
    stop()

'''
path = DBPEDIA_NL + 'labels_nl.nt'
index_labels_nl(path)
update_solr()

path = DBPEDIA_NL + 'interlanguage-links_nl.nt'
index_interlanguage(path)
update_solr()

path = DBPEDIA_NL + 'labels-en-uris_nl.nt'
index_labels_en(path)
update_solr()

path = DBPEDIA_EN + 'labels_en.nt'
index_labels_en(path)
update_solr()

path = DBPEDIA_NL + 'disambiguations_nl.nt'
index_disambiguations(path)
update_solr()

path = DBPEDIA_NL + 'redirects_nl.nt'
index_redirects(path)
update_solr()

path = DBPEDIA_NL + 'page-links_nl.nt'
index_inlinks(path)
update_solr()

path = DBPEDIA_NL + 'infobox-properties_nl.nt'
index_infoboxproperties(path)
update_solr()
'''

path = DBPEDIA_NL + 'long-abstracts_nl.nt'
index_longabstracts(path)
update_solr()

path = DBPEDIA_NL + 'long-abstracts-en-uris_nl_old.nt'
index_longabstracts(path)
update_solr()

path = DBPEDIA_NL + 'instance-types_nl.nt'
index_instance_types(path)
update_solr()

path = DBPEDIA_NL + 'instance-types_nl_old.nt'
index_instance_types(path)
update_solr()

path = DBPEDIA_NL + 'long-abstracts-en-uris_nl.nt'
index_longabstracts(path)
update_solr()

path = DBPEDIA_EN + 'disambiguations_en.nt'
index_disambiguations(path)
update_solr()

path = DBPEDIA_EN + 'infobox-properties_en.nt'
index_infoboxproperties(path)
update_solr()

path = DBPEDIA_EN + 'instance-types_en.nt'
index_instance_types(path)
update_solr()

path = DBPEDIA_EN + 'long-abstracts_en.nt'
index_longabstracts(path, lang='en')
update_solr()

path = DBPEDIA_EN + 'page-links_en.nt'
index_inlinks(path)
update_solr()

path = DBPEDIA_EN + 'redirects_en.nt'
index_redirects(path)
update_solr()
