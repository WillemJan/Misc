#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import solr
import sys

SOLR = solr.SolrConnection('http://solr.kbresearch.nl/dbpedia/')
DEBUG = False

def clean(ne, re_capitalize=False):
    ''' Remove unwanted charactarts from the naned-entity '''
    remove_char = ["+", "&&", "||", "!", "(", ")", "{", u'„',
                   "}", "[", "]", "^", "\"", "~", "*", "?", ":"]

    if re_capitalize:
        ne = ne.lower().title()

    ne = ne.strip()

    for char in remove_char:
        if ne.find(char) > -1:
            ne = ne.replace(char, u'')

    return ne

def linkEntity(ne):
    cleaned_ne = clean(ne.decode('utf-8')).strip()
    match, prob, match_label, reason = query_label(cleaned_ne, "title")
    return match, prob, match_label, reason


def calculate_propability(total, inlinks, match_label, ne):
    if total > 0:
        p = (float(inlinks) / total)
    else:
        p = 0.1
    if len(match_label[0].split()) - 1 > 2:
        c = float(len(ne.split())) / (len(match_label[0].split()) -1)
    else:
        c = 1
        p *= c
    if p>1:
        p = 1
    return p

def query_label(ne, field):

    if len(ne) < 2:
        reason = "Ne to short"
        return None, -1.0, None, reason

    if ne[0].islower():
        ne = ne.lower().title()
    if ne.find('.') > -1:
        ne = ne.replace('. ',' ')

    if ne.find('.') > -1:
        ne = ne.replace('.',' ')

    query = "title_str:\""
    query += ne + "\""
    query += " OR lastpart_str:\""
    query += ne.split(' ')[-1] + "\""

    if DEBUG:
        print query

    try:
        response = SOLR.query(q=query, rows=10, indent="on", sort="lang,inlinks", sort_order="desc")
    except:
        reason = "Failed to query solr"
        return None, -1.0, None, reason

    
    if response.numFound > 0:
        if response.numFound > 10:
            maximum = 10
        else:
            maximum = response.numFound

        score = []
        total_nl = 0
        total_en = 0

        for i in range(maximum):
            # Get all the values for calculate_propability
            document = response.results[i]

            lang = document.get('lang')
            match_label = document.get('title_str')

            score.append(document.get('inlinks'))

            if lang == 'nl':
                total_nl += document.get('inlinks')
            else:
                total_en += document.get('inlinks')

        for i in range(maximum):
            # First try an ID match
            document = response.results[i]
            match = document.get('id')
            match_label = document.get('title_str')
            disambig = document.get('disambig')
            reason = query + "&sort=lang desc, inlinks desc  #ID match"

            if match.split('resource/')[1].replace('>','') ==  ne:
                return match, 1, ne, reason

        for i in range(maximum):
            # Resort to highest score match
            disambig = document.get('disambig')
            document = response.results[i]
            match = document.get('id')
            match_label = document.get('title_str')

            reason = query

            for m in match_label:
                if m == ne and disambig == 1:
                    reason += " m == ne"
                    p = calculate_propability(total_nl, score[i], match_label, ne)
                    # Boost score m == ne == exact match
                    if p < 0.6:
                        p += 0.4
                    m = document.get('id').split('resource/')[1].replace('>','')
                    return match, p, m, reason


            '''
            for m in match_label:
                if m == ne:
                    p = calculate_propability(total_nl, score[i], match_label, ne)
                    reason += " m == ne, disambig"
                    # Boost score m == ne == exact match
                    if p < 0.6:
                        p += 0.2
                    return match, p, m, reason
            '''


        # From this point on work with the first hit
        document = response.results[0]

        lang = document.get('lang')
        match = document.get('id')
        match_label = document.get('title_str')

        reason = query + "&sort=lang desc, inlinks desc"

        # Calculate propabilty
        if lang == 'nl':
            total = total_nl
            p = calculate_propability(total_nl, score[0], match_label, ne)
        else:
            total = total_en
            p = calculate_propability(total_en, score[0], match_label, ne)

        if len(ne.split()) > 1:
            ma = " ".join(ne.split(" ")[:-1]).strip()
            for l in match_label:
                if l.startswith(ma):
                    return match, 0.7, match_label[0], reason
        else:
            if len(match_label[0]) >= len(ne):
                return match, p, match_label[0], reason + " p: inlinks : " + str(score[0]) + " total : " + str(total)
            else:
                return False, 0, False, u'length mismatch: ' + match_label[0] + u' < ' + ne

        # Match W.F. Hermans instead of name conflict.
        count_letters = len(match_label[0].split(' ')) - 1
        count_query = 0
        for i in range(count_letters):
            if i < len(ma.split(' ')):
                if match_label[0].split(' ')[i].startswith(ma.split(' ')[i]):
                    count_query += 1
                    if p < 0.8:
                        p += 0.2
        if count_query == count_letters:
            if len(match_label[0]) >= len(ne):
                return match, p, match_label[0], reason + " (name jumble)  p: inlinks : " + str(score[0]) + " total : " + str(total)
            else:
                return False, 0, False, u'length mismatch: ' + match_label[0] + u' < ' + ne

        return False, 0, False, 'Name conflict (' + match_label[0] + ', ' + ne + ')'

    return False, 0, False, 'Nothing found'

if __name__ == '__main__':
    print(linkEntity(sys.argv[1]))
