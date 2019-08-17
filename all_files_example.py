#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Create a Solr index from dbpedia dump files.

Index .nl first, with interlanguage stored in id_en,
then proceed to index .en files, and use the fallback
function to try and map the .en info to the .nl record.
'''

import json
import re
import sys
import urllib
import urllib2
from sets import Set

# Set the default encoding to utf-8
reload(sys)
sys.setdefaultencoding('utf8')

DEBUG = False
DEBUG_MAX = 10000 # Nr of records to index while debugging

if not DEBUG:
    SOLR = 'http://localhost:4040/solr/dbpedia/'  # Where the Solr endpoint lives
else:
    SOLR = 'http://localhost:4041/solr/dbpedia/'  # Where the Solr endpoint lives

SOLR_ADD = SOLR + 'update/json'  # Add-path
SOLR_UPDATE = SOLR_ADD + '?commit=true' # Update-path
SOLR_QUERY = SOLR + 'select/?'  # Query-path

DBPEDIA_NL = '2015-04/nl/'  # Path to Dutch DBPedia dumps
DBPEDIA_EN = '2015-04/en/'  # Path to English DBPedia dumps


def read_redirects(path):
    cache = Set()
    with open(path, 'r') as fp:
            for line in fp:
                if not line[0] == '<':
                    continue

                cache.add(line.split()[0])
    return cache

redirect_cache = Set()
path = DBPEDIA_NL + 'redirects_nl.nt'
redirect_cache = read_redirects(path)

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


def clean(input_str):
    ''' Convert to unicode utf-8 and clean string from leading and training
    whitespaces '''
    input_str = urllib.unquote(input_str)
    try:
        input_str = input_str.strip().decode('raw_unicode_escape')
        input_str = input_str.replace('\\"', "'")
        return unicode(input_str.encode('utf-8'))
    except:
        return unicode(input_str)


def id_to_text(input_str):
    '''
    Convert dbpedia id to text
    <http://nl.dbpedia.org/resource/Bach_(doorverwijspagina)> == Bach
    '''
    input_str = input_str.split('/')[-1].replace('>', '')
    input_str = input_str.replace('_(doorverwijspagina)', '')
    input_str = input_str.replace('_', ' ')
    return input_str


def add_solr(doc):
    ''' Index record to Solr '''
    doc = json.dumps([doc])
    req = urllib2.Request(url=SOLR_ADD, data=doc)
    req.add_header('Content-type', 'application/json; charset=utf-8')

    try:
        response = urllib2.urlopen(req)

        if not response.getcode() == 200:
            print('Error while adding record (%s)' % SOLR_ADD)
    except:
        print("Exception while adding record (%s_)" % SOLR_ADD)


def update_solr():
    req = urllib2.Request(url=SOLR_UPDATE)
    req.add_header('Content-type', 'application/json')
    response = urllib2.urlopen(req)

    if not response.getcode() == 200:
        print('Error while updating' % SOLR_ADD)


def fetch_solr_by_id(doc_id, lang=''):
    ''' Query Solr and return response Json '''
    doc_id = doc_id.replace('"','')
    q = {'q': 'id:"' + doc_id + '"', 'wt': 'json'}
    if lang:
        q = {'q': 'id_en:"' + doc_id + '"', 'wt': 'json'}

    query = urllib.urlencode(q)
    req = urllib2.Request(url=SOLR_QUERY, data=query)
    response = urllib2.urlopen(req)

    if not response.getcode() == 200:
        print('Error while retrieving record')

    return json.loads(response.read())


def fetch_solr_by_title_str(title_str, dbpedia_id=False):
    '''
    Query Solr for given title, (exact string match only)
    '''
    title_str = normalize(title_str)

    q = {'q': 'title_str:"' + title_str + '"', 'wt': 'json'}
    if dbpedia_id:
        q = {'q': 'title_str:"' + title_str + '" AND id:"' + dbpedia_id + '"', 'wt' : 'json'}

    query = urllib.urlencode(q)
    req = urllib2.Request(url=SOLR_QUERY, data=query)
    response = urllib2.urlopen(req)

    if not response.getcode() == 200:
        print('Error while retrieving record')

    return json.loads(response.read())


def fetch_solr_by_id_fallback(doc_id, lang=''):
    '''
    Query Solr and return response Json,
    first try to find by lang='nl', fallback to id (en),
    returns False if nothing was found
    '''
    query = urllib.urlencode({'q': 'id_en:"' + doc_id + '" AND lang:"nl"',
                              'wt': 'json'})
    req = urllib2.Request(url=SOLR_QUERY, data=query)
    response = urllib2.urlopen(req)

    if not response.getcode() == 200:
        print('Error while retrieving record')

    response = json.loads(response.read())
    try:
        doc_id = response.get('response').get('docs')[0].get('id')
    except:
        response = fetch_solr_by_id(doc_id)

        try:
            doc_id = response.get('response').get('docs')[0].get('id')
        except:
            doc_id = False

    return doc_id


def index_longabstracts_en(path):
    '''
    Index the abstracts with only .en identifiers,
    and only if the abstract is longer than the dutch abstract.

   <http://dbpedia.org/resource/Andre_Agassi> <http://dbpedia.org/ontology/abstract> "Andre Kirk Agassi (Las Vegas, 29 april 1970) is een voormalig tennisser uit de Verenigde Staten. Zijn vader is afkomstig uit Iran en van Armeense en Assyrische afkomst.In 1999 werd Agassi de vijfde speler in de geschiedenis van de sport die alle vier de Grand Slam toernooien had gewonnen: de Australian Open, de Open Franse Tenniskampioenschappen, Wimbledon en de US Open. In totaal won hij acht grand slam toernooien en staat hiermee op de lijst van Grand Slam Titels op een gedeelde 8e plaats, samen met Jimmy Connors en Ivan Lendl.Agassi is de enige speler ooit die alle Grands Slams en de Tennis Masters Cup heeft gewonnen, deel uitmaakte van een winnend Davis Cup-team en de Olympische gouden medaille heeft gewonnen. In de lijst van Tennis Masters Series titels staat Agassi met 17 titels op de derde plaats, onder Rafael Nadal en Roger Federer, die er respectievelijk 21 en 20 wonnen. Hij is op 22 oktober 2001 getrouwd met de voormalige Duitse toptennisster Steffi Graf, ze hebben twee kinderen."@nl .
    '''
    i = 0
    with open(path, 'r') as fp:
        for line in fp:
            if not line[0] == '<':
                continue

            i += 1
            if DEBUG and i > DEBUG_MAX:
                return

            line = clean(line)
            dbpedia_id_en = line.split()[0]
            abstract = line.split('"')[1]

            try:
                dbpedia_id = fetch_solr_by_id_fallback(dbpedia_id_en)
            except:
                dbpedia_id = ''

            lang = ''
            dutch_id = False
            if not dbpedia_id_en == dbpedia_id and dbpedia_id:
                dutch_id = True
            if not dbpedia_id:
                lang = 'en'
                dbpedia_id = dbpedia_id_en

            response = fetch_solr_by_id(dbpedia_id, lang)

            try:
                nl_abstract = response.get('response')
                nl_abstract = nl_abstract.get('docs')[0].get('abstract')
                if nl_abstract is None:
                    nl_abstract = ''
            except:
                nl_abstract = ''

            if len(abstract) > (len(nl_abstract) + 2):
                if dutch_id:
                    print("MINE is longer than yours: " + dbpedia_id)
                doc = {}
                doc['id'] = dbpedia_id
                doc['abstract_en'] = {'set': abstract}

                add_solr(doc)


def index_longabstracts(path):
    '''
    Index long abstracts

    <http://nl.dbpedia.org/resource/Andre_Agassi> <http://dbpedia.org/ontology/abstract> "Andre Kirk Agassi (Las Vegas, 29 april 1970) is een voormalig tennisser uit de Verenigde Staten. Zijn vader is afkomstig uit Iran en van Armeense en Assyrische afkomst.In 1999 werd Agassi de vijfde speler in de geschiedenis van de sport die alle vier de Grand Slam toernooien had gewonnen: de Australian Open, de Open Franse Tenniskampioenschappen, Wimbledon en de US Open. In totaal won hij acht grand slam toernooien en staat hiermee op de lijst van Grand Slam Titels op een gedeelde 8e plaats, samen met Jimmy Connors en Ivan Lendl.Agassi is de enige speler ooit die alle Grands Slams en de Tennis Masters Cup heeft gewonnen, deel uitmaakte van een winnend Davis Cup-team en de Olympische gouden medaille heeft gewonnen. In de lijst van Tennis Masters Series titels staat Agassi met 17 titels op de derde plaats, onder Rafael Nadal en Roger Federer, die er respectievelijk 21 en 20 wonnen. Hij is op 22 oktober 2001 getrouwd met de voormalige Duitse toptennisster Steffi Graf, ze hebben twee kinderen."@nl .
    '''
    i = 0
    with open(path, 'r') as fp:
        for line in fp:
            if not line[0] == '<':
                continue

            i += 1
            if DEBUG and i > DEBUG_MAX:
                return

            line = clean(line)
            dbpedia_id = line.split()[0]
            abstract = clean(line.split('"')[1])

            doc = {}
            doc['id'] = dbpedia_id
            doc['abstract_nl'] = {'set': abstract}

            add_solr(doc)


def index_infoboxproperties(path):
    '''
    Index dob, dod and gender

    <http://nl.dbpedia.org/resource/Anthony_Fokker> <http://nl.dbpedia.org/property/naam> "Anthony Fokker"@nl .
    <http://nl.dbpedia.org/resource/Anthony_Fokker> <http://nl.dbpedia.org/property/afbeelding> "Anthony Fokker 1912.jpg"@nl .
    <http://nl.dbpedia.org/resource/Anthony_Fokker> <http://nl.dbpedia.org/property/onderschrift> "Anthony Fokker"@nl .
    <http://nl.dbpedia.org/resource/Anthony_Fokker> <http://nl.dbpedia.org/property/volledigenaam> "Antonij Herman Gerard Fokker"@nl .
    <http://nl.dbpedia.org/resource/Anthony_Fokker> <http://nl.dbpedia.org/property/geboortedatum> "1890-04-06"^^<http://www.w3.org/2001/XMLSchema#date> .
    <http://nl.dbpedia.org/resource/Anthony_Fokker> <http://nl.dbpedia.org/property/geboorteplaats> <http://nl.dbpedia.org/resource/Kediri_(stad)> .
    <http://nl.dbpedia.org/resource/Anthony_Fokker> <http://nl.dbpedia.org/property/sterfdatum> "1939-12-23"^^<http://www.w3.org/2001/XMLSchema#date> .
    <http://nl.dbpedia.org/resource/Anthony_Fokker> <http://nl.dbpedia.org/property/sterfplaats> "New York City,"@nl .
    <http://nl.dbpedia.org/resource/Anthony_Fokker> <http://nl.dbpedia.org/property/nationaliteit> "Nederlandse"@nl .
    <http://nl.dbpedia.org/resource/Anthony_Fokker> <http://nl.dbpedia.org/property/portaal> "Luchtvaart"@nl .
    '''

    geboorte = ['http://nl.dbpedia.org/property/gbdat',
                'http://nl.dbpedia.org/property/geboortedatum',
                'http://dbpedia.org/property/birthDate',
                'http://dbpedia.org/property/dateOfBirth']

    dbp_nl = '<http://nl.dbpedia.org/resource/'
    dbp_en = '<http://dbpedia.org/resource/'

    i = 0
    with open(path, 'r') as fp:
        for line in fp:
            if not line[0] == '<':
                continue

            i += 1
            if DEBUG and i > DEBUG_MAX:
                return

            line = clean(line)

            if True in [line.find(f) > -1 for f in geboorte]:
                dbpedia_id = fetch_solr_by_id_fallback(line.split()[0])

                if line.split()[2].startswith('"'):
                    dob_string = line.split()[2].split('"')[1]
                    dob = re.match('.*(\d{4}-\d{2}-\d{2}).*', dob_string)
                else:
                    dob = False

                if dob:
                    dob = dob.groups()[0].strip() + 'T00:00:00Z'
                    doc = {}
                    doc['id'] = dbpedia_id
                    doc['dob'] = {'set': dob}
                    add_solr(doc)

            if line.find('http://nl.dbpedia.org/property/volledigeNaam') > -1:
                dbpedia_id = line.split()[0]
                if line.find('"') > -1:
                    name = line.split('"')[1]

                    doc = {}
                    doc['id'] = dbpedia_id
                    doc['title'] = {'add' : normalize(name)}
                    doc['title_str'] = {'add' : normalize(name)}

                    doc['org_title'] = {'add' : name}
                    doc['org_title_str'] = {'add' : name}

                    add_solr(doc)

            if line.find('http://nl.dbpedia.org/property/geslacht') > -1:
                dbpedia_id = line.split()[0]
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
                    doc['gender'] = {'set': gender}
                    add_solr(doc)

            if line.find('<http://dbpedia.org/property/gender>') > -1:
                dbpedia_id = fetch_solr_by_id_fallback(line.split()[0])

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
                    doc['gender'] = {'set': gender}
                    add_solr(doc)


def index_inlinks(path):
    '''
    Count the number of links, for a certain page,
    and add this to the existing id.

    <http://nl.dbpedia.org/resource/Albert_Speer> <http://dbpedia.org/ontology/wikiPageWikiLink> <http://nl.dbpedia.org/resource/Albert_Speer_(junior)> .
    <http://nl.dbpedia.org/resource/Albert_Speer> <http://dbpedia.org/ontology/wikiPageWikiLink> <http://nl.dbpedia.org/resource/Proces_van_Neurenberg> .
    <http://nl.dbpedia.org/resource/Albert_Speer> <http://dbpedia.org/ontology/wikiPageWikiLink> <http://nl.dbpedia.org/resource/Mannheim> .
    '''
    prev_dbpedia_id = ''
    counter = 1
    i = 0
    with open(path, 'r') as fp:
        for line in fp:
            if not line[0] == '<':
                continue

            i += 1
            if DEBUG and i > DEBUG_MAX:
                return

            line = clean(line)
            dbpedia_id = fetch_solr_by_id_fallback(line.split()[0])

            if dbpedia_id in redirect_cache:
                ####
                ###
                ##
                #  ! count this as a inlink for the target id !  #
                ##
                ###
                ###
                continue

            if not prev_dbpedia_id:
                prev_dbpedia_id = dbpedia_id
                counter = 1
                doc = {}
                doc['id'] = dbpedia_id
                doc['inlinks'] = {'set': counter}

            if not prev_dbpedia_id == dbpedia_id:
                add_solr(doc)
                counter = 1
                prev_dbpedia_id = dbpedia_id


            # TODO: CHECK IF THE inlinks are max()  :) : )  :: ) )

            if counter > current_counter:
                doc = {}
                doc['id'] = dbpedia_id
                doc['inlinks'] = {'set': counter}
            counter += 1


def index_redirects(path):
    '''
    Index all (nl) redirects,
    add the name of the redirect to the existing record.

    <http://nl.dbpedia.org/resource/Architekt> <http://dbpedia.org/ontology/wikiPageRedirects> <http://nl.dbpedia.org/resource/Architect> .
    <http://nl.dbpedia.org/resource/Anaximandros> <http://dbpedia.org/ontology/wikiPageRedirects> <http://nl.dbpedia.org/resource/Anaximander> .
    '''
    i = 0
    with open(path, 'r') as fp:
        for line in fp:
            if not line[0] == '<':
                continue

            i += 1
            if DEBUG and i > DEBUG_MAX:
                return

            line = clean(line)
            dbpedia_id = line.split()[2]
            title = id_to_text(line.split()[0])

            try:
                response = fetch_solr_by_id(dbpedia_id)
            except:
                response = {}
            known = []

            try:
                known = response.get('response').get('docs')[0].get('title')
                if known is None:
                    known = []
            except:
                pass

            if normalize(title).lower() not in known:
                doc = {}
                doc['id'] = dbpedia_id
                doc['title'] = {"add": normalize(title)}
                doc['title_str'] = {"add": normalize(title)}

                doc['org_title'] = {"add": title}
                doc['org_title_str'] = {"add": title}
                add_solr(doc)


def index_disambiguations(path):
    '''
    Index all (nl) disambiguations,
    add the name of the disambiguation to the existing record.

    <http://nl.dbpedia.org/resource/Animisme> <http://dbpedia.org/ontology/wikiPageDisambiguates> <http://nl.dbpedia.org/resource/Animisme_(kunst)> .
    <http://nl.dbpedia.org/resource/Animisme> <http://dbpedia.org/ontology/wikiPageDisambiguates> <http://nl.dbpedia.org/resource/Animisme_(parapsychologie)> .
    '''
    i = 0
    with open(path, 'r') as fp:
        for line in fp:
            if not line[0] == '<':
                continue

            i += 1
            if DEBUG and i > DEBUG_MAX:
                return

            line = clean(line)
            dbpedia_id = line.split()[0]
            title = id_to_text(line.split()[2])

            try:
                response = fetch_solr_by_id(dbpedia_id)
            except:
                response = {}
            known = []

            try:
                known = response.get('response').get('docs')[0].get('title')
                if known is None:
                    known = []
            except:
                pass

            if normalize(title) not in known:
                # print("disambiguation", normalize(title), known)
                doc = {}
                doc['id'] = dbpedia_id
                doc['org_title'] = {"add": title}
                doc['org_title_str'] = {"add": title}

                doc['title'] = {"add": normalize(title)}
                doc['title_str'] = {"add": normalize(title)}

                add_solr(doc)


def index_labels_en(path):
    '''
    Index all (en) dbpedia labels,
    disambig = 1, means that the id contains a '('.
    In that case there are multiple title_str entries.

    Example: Utrecht (provincie)
    Result: title_str: ['Utrecht (provincie)', 'Utrecht')]

    If there is a .nl entry, just add the .en identifier

    <http://dbpedia.org/resource/Albert_Speer> <http://www.w3.org/2000/01/rdf-schema#label> "Albert Speer"@nl .
    '''
    i = 0
    with open(path, 'r') as fp:
        for line in fp:
            if not line[0] == '<':
                continue

            i += 1
            if DEBUG and i > DEBUG_MAX:
                return

            line = clean(line)
            dbpedia_id_en = line.split()[0]

            try:
                dbpedia_id_nl = fetch_solr_by_id_fallback(dbpedia_id_en)
            except:
                dbpedia_id_nl = ''

            dbpedia_id = dbpedia_id_en
            update = False
            if dbpedia_id_nl:
                dbpedia_id = dbpedia_id_nl
                update = True

            doc = {}
            doc['id'] = dbpedia_id
            doc['id_en'] = {'set': dbpedia_id_en}

            title = line.split('"')[1]

            if update:
                try:
                    result = fetch_solr_by_title_str(title, dbpedia_id)
                except:
                    result = {'response' : {}}
                if not result.get('response').get('numFound'):
                    doc['pref_title'] = {'add': title}
                    doc['pref_title_str'] = {'add' : title}

                    doc['org_title_str'] = {'add': title}
                    doc['org_title'] = {'add': title}

                    doc['title_str'] = {'add': normalize(title)}
                    doc['title'] = {'add': normalize(title)}
            else:
                doc['lang'] = {'set': 'en'}
                doc['disambig'] = 0

                doc['title_str'] = doc['title'] = title

                doc['pref_title_str'] = doc['pref_title'] = title
                doc['title_str'] = doc['title'] = normalize(title)

                if dbpedia_id.find('(') > -1:
                    doc['disambig'] = 1

                    doc['org_title_str'] = [title, title.split('(')[0].strip()]
                    doc['org_title'] = doc['org_title_str']

                    doc['title_str'] = [normalize(title),
                                        normalize(title.split('(')[0].strip())]

            add_solr(doc)


def index_labels_nl(path):
    '''
    Index all (nl) dbpedia labels,
    disambig = 1, means that the id contains a '('.
    In that case there are multiple title_str entries.

    Example: Utrecht (provincie)
    Result: title_str: ['Utrecht (provincie)', 'Utrecht')]

    <http://nl.dbpedia.org/resource/Albert_Speer> <http://www.w3.org/2000/01/rdf-schema#label> "Albert Speer"@nl .
    '''
    i = 0
    with open(path, 'r') as fp:
        for line in fp:
            if not line[0] == '<':
                continue

            i += 1
            if DEBUG and i > DEBUG_MAX:
                return

            line = clean(line)

            if line.split()[0] in redirect_cache:
                continue

            doc = {}
            dbpedia_id = line.split()[0]
            doc['id'] = dbpedia_id
            doc['id_nl'] = dbpedia_id
            doc['lang'] = 'nl'
            title = line.split('"')[1]

            doc['disambig'] = 0
            doc['org_title_str'] = doc['org_title'] = title

            doc['title_str'] = doc['title'] = normalize(title)
            doc['pref_title'] = doc['pref_title_str'] = title

            if dbpedia_id.find('(') > -1:
                doc['disambig'] = 1
                doc['title_str'] = [normalize(title),
                                    normalize(title.split('(')[0].strip())]
                doc['title'] = doc['title_str']
                doc['org_title_str'] = [title,
                                        title.split('(')[0].strip()]
                doc['org_title'] = doc['org_title_str']

            add_solr(doc)


def index_en_id(path):
    '''
    Index all (en) id's that also have a dutch entry,
    also index the wikidata identifiers.
    '''
    i = 0
    with open(path, 'r') as fp:
        for line in fp:
            line = clean(line)

            i += 1
            if DEBUG and i > DEBUG_MAX:
                return

            if line.find('<http://dbpedia.org/resource/') > -1:
                dbpedia_id = line.split()[0]
                dbpedia_id_en = line.split()[2]

                doc = {}
                doc['id'] = dbpedia_id
                doc['id_en'] = {'set': dbpedia_id_en}

                try:
                    response = fetch_solr_by_title_str(id_to_text(dbpedia_id_en), dbpedia_id_en)
                except:
                    result = {'response' : {}}

                if response.get('response').get('numFound')  == 0:
                    # doc['pref_title_str'] = doc['pref_title'] = {'add' : [id_to_text(dbpedia_id_en)]}

                    doc['org_title'] = {'add' : [id_to_text(dbpedia_id_en)]}
                    doc['org_title_str'] = {'add' : [id_to_text(dbpedia_id_en)]}

                    doc['title_str'] = {'add' : [normalize(id_to_text(dbpedia_id_en))]}
                    doc['title'] = doc['title_str']

                    if dbpedia_id_en.find('(') > -1:
                        if not dbpedia_id_en.split(' (')[0] in doc['title']:

                            title = dbpedia_id_en.split(' (')[0]

                            doc['org_title']['add'].append(title)
                            doc['org_title_str']['add'].append(title)

                            doc['title']['add'].append(normalize(title))
                            doc['title_str']['add'].append(normalize(title))

                    add_solr(doc)

            if line.find('http://wikidata.dbpedia.org/resource/') > -1:
                dbpedia_id = line.split()[0]
                wd_id = line.split()[2].split('/')[-1].replace('>', '')

                doc = {}
                doc['id'] = dbpedia_id
                doc['wd_id'] = {'set': wd_id}
                add_solr(doc)


def index_instance_types(path):
    '''
    Index instance type's like Person // Actor //..
    '''
    i = 0
    with open(path, 'r') as fp:
        for line in fp:
            if not line[0] == '<':
                continue

            i += 1
            if DEBUG and i > DEBUG_MAX:
                return

            line = clean(line)

            dbpedia_id = fetch_solr_by_id_fallback(line.split()[0])

            instance_type = line.split()[2]
            instance_type = instance_type.split('/')[-1].replace('<', '').replace('>', '').strip()

            doc = {}
            doc['id'] = dbpedia_id
            doc['schemaorgtype'] = {'add': instance_type}

            add_solr(doc)




def main():
    if DEBUG:
        print('Starting in debug mode, indexing %i lines per file' % DEBUG_MAX)

    # Start with getting all re-directs, for there are labels,
    # that serve only as an redirect, we don't want to create
    # seperate entries for that, we just want to add the value to the title
    # field, this requires a cache of all redirect labels.
    print('Starting: index_labels_nl')
    # Index all .nl labels
    path = DBPEDIA_NL + 'labels_nl.nt'
    index_labels_nl(path)
    update_solr()

    print('Starting: interlanguage-links_nl')
    # Index all .en id's that have a .nl entry
    # also index the wikidata identifier
    path = DBPEDIA_NL + 'interlanguage-links_nl.nt'
    index_en_id(path)
    update_solr()

    print('Starting: index_en')
    # Index all .en id's that have a .nl entry
    path = DBPEDIA_NL + 'labels-en-uris_nl.nt'
    index_labels_en(path)
    update_solr()

    print('Starting: disambiguations_nl')
    # Index all disambiguation pages, as title_str
    # if not allready in index.
    path = DBPEDIA_NL + 'disambiguations_nl.nt'
    index_disambiguations(path)
    update_solr()

    print('Starting: redirects')
    # Index all redirects, as title_str
    # if not allready in index.
    path = DBPEDIA_NL + 'redirects_nl.nt'
    index_redirects(path)
    update_solr()

    print('Starting: inlinks')
    # Count the number of inlinks the page has,
    # index this as a inlinks
    path = DBPEDIA_NL + 'page-links_nl.nt'
    index_inlinks(path)
    update_solr()

    print('Starting: infobox')
    # Fetch properties from the infoboxes,
    # for now gender (M / F) and DOB / DOD
    path = DBPEDIA_NL + 'infobox-properties_nl.nt'
    index_infoboxproperties(path)
    update_solr()

    print('Starting: long abstracts')
    # Index long abstracts into the .nl records
    path = DBPEDIA_NL + 'long-abstracts_nl.nt'
    index_longabstracts(path)
    update_solr()

    print('Starting: long abstracts (old)')
    # Index long abstracts into the .nl records
    path = DBPEDIA_NL + 'long-abstracts-en-uris_nl_old.nt'
    index_longabstracts_en(path)
    update_solr()


    print('Starting: instance_types')
    # Index all instances, like Person // Scientist
    path = DBPEDIA_NL + 'instance-types_nl.nt'
    index_instance_types(path)
    update_solr()

    print('Starting: long abstracts (en)')
    # Index dutch abstracts belonging to .en articles,
    # if the there is a dutch entry that allready has
    # an abstract, check the length if new entry
    # is longer index the new one.
    path = DBPEDIA_NL + 'long-abstracts-en-uris_nl.nt'
    index_longabstracts_en(path)
    update_solr()

    print('Starting: labels (en)')
    # Index .en labels if there is no .nl entry
    path = DBPEDIA_EN + 'labels_en.nt'
    index_labels_en(path)
    update_solr()

    print('Starting: disambiguations (en)')
    # Index .en disambiguations
    path = DBPEDIA_EN + 'disambiguations_en.nt'
    index_disambiguations(path)
    update_solr()

    print('Starting: infobox (en)')
    # Index .en infoboxes-properties
    path = DBPEDIA_EN + 'infobox-properties_en.nt'
    index_infoboxproperties(path)
    update_solr()

    print('Starting: instance_types (en)')
    # Index all instances, like Person // Scientist
    path = DBPEDIA_EN + 'instance-types_en.nt'
    index_instance_types(path)
    update_solr()

    print('Starting: long abstracts (en)')
    # Index long abstracts into the .en records
    path = DBPEDIA_EN + 'long-abstracts_en.nt'
    index_longabstracts(path)
    update_solr()

    print('Starting: inlinks (en)')
    # Count the number of inlinks the page has,
    # index this as a inlinks
    path = DBPEDIA_EN + 'page-links_en.nt'
    index_inlinks(path)
    update_solr()

    print('Starting: redirects (en)')
    # Index all redirects, as title_str
    # if not allready in index.
    path = DBPEDIA_EN + 'redirects_en.nt'
    index_redirects(path)
    update_solr()

if __name__ == "__main__":
    main()
