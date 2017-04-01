#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import unicodedata

import test_text
import enchant

import cluster

from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

from pattern.nl import sentiment

dictionary = enchant.Dict("nl_NL")

class shallowStats():
    '''
        Shallow stats on text.
    '''
    def __init__(self, xml, raw_text = False):

        self.text = u''
        self.title = u''
        self.p_count = 0

        self.tokenized_text_extended = []
        self.tokenized_text_short = []
        self.tokenized_text_nostop = []


        if raw_text:
            if type(raw_text) in [type(u''), type('')]:
                self.text = raw_text
            if type(raw_text) in [type([])]:
                self.text = "\n".join(raw_text)

        else:
            # Get the content from an xml object formatted like
            # http://resources2.kb.nl/010065000/articletext/ 
            # 010069811/DDD_010069811_0001_articletext.xml
            for item in xml.iter():
                if item.tag == 'title':
                    self.title += item.text + u'\n'
                    self.text += item.text + u'\n'
                if item.tag == 'p':
                    if not type(item.text) == type(None):
                        self.text += item.text + u'\n'
                        self.p_count += 1
            self.text = self.text.strip()
        self.tokenize()

    @property
    def text_length(self):
        return len(self.text.replace('\n', ''))

    @property
    def nr_of_whitespaces(self):
        return len(self.text.split(' '))

    @property
    def nr_of_alpanumeric(self):
        res = [a for a in self.text.replace('\n', '') if a.isalpha()]
        return len(res)

    @property
    def alphanumeric_representation(self):
        res = [a for a in self.text.replace('\n', '') if a.isalpha()]
        return u''.join(res)

    def tokenize(self):
        # letters is a table of valid letters,
        # this is to fiqure out the amount of noise.
        letters = u''
        letters += string.letters

        all_unicode = ''.join(unichr(i) for i in xrange(65536))
        letters += ''.join(c for c in all_unicode if
                unicodedata.category(c)=='Lu' or unicodedata.category(c)=='Ll')

        # numbers != noise, so we add them here.
        letters += ''.join([str(a) for a in range(0,10)])

        # first get the vanilla tokens.
        self.tokenized_text_extended = word_tokenize(self.text)

        # create a cleaner instance of the token list
        # remove all char's (words only).
        tokenized_text_short = [w for w in self.tokenized_text_extended if len(w) > 2]

        # remove strings we don't want, to reduce noise.
        # also create a list of words that are non-stopwords.
        total_noise = 0
        total_words = 0
        total_stop = 0
        for word in tokenized_text_short:
            if len(word) > 1:
                # iterate over char in word, if the word contains a lot of
                # non-letter, classify it as noise.
                noise = 100-len([char for char in word if char in letters]) / (len(word)/100.0)
                if noise < 30:
                    if not word.lower() in stopwords.words('dutch') and not word.lower() in [u'den', u'ten']:
                        self.tokenized_text_nostop.append(word)
                    else:
                        total_stop += 1
                        total_noise += 1
                    total_words += 1
                else:
                    total_noise += 1
        self.noise_to_text_ratio = total_noise / (total_words / 100.0)
        self.stop_to_text_ratio = total_stop / (total_words / 100.0)

    @property
    def noise_to_text_ratio(self):
        return self.noise_to_text_ratio

    @property
    def nr_of_sentences(self):
        sentences = self.sentences = [s for s in sent_tokenize(self.text) if len(s) > 3]
        #tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        #tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
        #print(tagged_sentences)
        return len(self.sentences)

    @property
    def avg_wordlen(self):
        #print self.tokenized_text_short
        total = 0
        for word in self.tokenized_text_nostop:
            total += len(word)
        avg = total / float(len(self.tokenized_text_nostop))
        return avg

    @property
    def whitespace_to_text_ratio(self):
        nr_of_whitespaces = self.nr_of_whitespaces
        text_length = self.text_length
        return nr_of_whitespaces / (text_length / 100.0)

    @property
    def usefull_tokens_ratio(self):
        return len(self.tokenized_text_nostop) / (len(self.tokenized_text_extended) / 100.0)

    @property
    def upcase_ratio(self):
        upcase_words = [w for w in self.tokenized_text_nostop if w.istitle()]
        return len(upcase_words) / (len(self.tokenized_text_nostop) / 100.0)

    def most_used_words(self, maxnr):
        freq = {}
        for word in self.tokenized_text:
            if not word in freq:
                freq[word] = 0
            else:
                freq[word] += 1

        for item in freq:
            if freq[item] > 0:
                print item
        return

    @property
    def dict_check(self):
        total_in_dict = len([word for word in self.tokenized_text_nostop if \
            dictionary.check(word)])
        return total_in_dict / (len(self.tokenized_text_nostop) / 100.0)



def repr_stats(st):
    #print u"Input object: %s" % st.text
    print u"Nr of paragraphs: %i" % st.p_count
    print u"Nr of whitespaces: %i" % st.nr_of_whitespaces
    print u"Nr of alphanumeric characters: %i" % st.nr_of_alpanumeric
    print u"Tokenized words: %s" % \
    (u",".join(st.tokenized_text_extended[0:20]) + u'....')
    print u"Tokenized (clean)words: %s" % \
    (u",".join(st.tokenized_text_short[0:20]) + u'....')
    print "Tokenized (nostop)words: %s" % \
    (u",".join(st.tokenized_text_nostop[0:20]) + u'....')
    print u"Nr of total tokens: %i" % len(st.tokenized_text_extended)
    print u"Nr of total (clean)tokens: %i" % len(st.tokenized_text_short)
    print u"Nr of total (nostop)tokens: %i" % len(st.tokenized_text_nostop)
    from collections import Counter
    c = Counter(st.tokenized_text_nostop)
    print u"Top ten nostop tokens:"
    print u"".join([u"\t" + str(i)+u" freq: %i\n" % j for i,j in c.most_common(10)])
    print u"Usefull to 'useless' tokens ratio: %2.2f%%" % st.usefull_tokens_ratio
    print u"Avg word length (based on nostop): %2.2f" % st.avg_wordlen
    print u"Whitespace to text ratio: %2.2f%%" % st.whitespace_to_text_ratio
    print u"Upcase-starting words ratio (based on nostop): %2.2f%%" % st.upcase_ratio
    print u"Noise to text ratio: %2.2f%%" % st.noise_to_text_ratio
    print u"Nr of sentences: %i" % st.nr_of_sentences
    print u"Ratio nr of (nostop)tokens in dutch dict: %2.2f%%" % st.dict_check

    polarity_total = 0
    subjectivity_total = 0
    total_sentences = 0
    for s in st.sentences:
        polarity, subjectivity = sentiment(s)
        if not polarity == 0:
            polarity_total += polarity
            subjectivity_total += subjectivity
            total_sentences += 1
    if total_sentences > 0:
        polarity_total = polarity_total / (total_sentences)
        subjectivity_total = subjectivity_total / (total_sentences)

    print "Avg sentiment (polarity/subjectivity): %2.2f, %2.2f" % \
    (polarity_total, subjectivity_total)

    print "Clusters (nostop)tokens:"
    from pprint import pprint
    pprint (cluster.get_clusters(st.sentences))
    print "Ngrams:"
    from nltk.util import ngrams
    pprint(list(ngrams(st.tokenized_text_nostop, 3))[:10])
    print "==========================================\n\n"

if __name__ == '__main__':
    xml = test_text.get_text()
    all_words = []

    for i in xml:
        st = shallowStats(i)
        #st = shallowStats(None,'appels zijn lekker. Peren zijn ook best te eten. De meeste peren uit Nederland worden nu naar Rusland verscheept.')
        repr_stats(st)
        for s in st.sentences:
            all_words.append(s)

    st = shallowStats(None, all_words)
    repr_stats(st)
