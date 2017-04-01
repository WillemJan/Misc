import numpy

## NLTK imports
from nltk.cluster import KMeansClusterer, euclidean_distance
import nltk.corpus
import nltk.stem

import enchant

stemmer_func = nltk.stem.snowball.DutchStemmer().stem


## Define module wide constants
DEFAULT_NUM_CLUSTERS = 2
dictionary = enchant.Dict("nl_NL")

def normalize_word(word):
    return word.lower()
    #return stemmer_func(word.lower())

def get_words(survey):
    words = set()
    for response in survey:
        for word in response.split():
            #if dictionary.check(word):
            words.add(normalize_word(word))
    return list(words)

def vectorspaced(response, words):
    response_components = [normalize_word(word) for word in response.split()]
    return numpy.array([word in response_components for word in words], numpy.short)
    #return numpy.array([word in response_components for word in words if dictionary.check(word)], numpy.short)


def get_clusters(txt):
    clusters = {}
    num_clusters = len(txt)/4 
    if num_clusters < 2:
        num_clusters = 2
    if num_clusters > 5:
        num_clusters = 5
    #txt = [''.join([l for l in txt])]
    #print txt
    responses = [line.strip() for line in txt]
    words = get_words(responses)

    cluster = KMeansClusterer(num_clusters, euclidean_distance, repeats=100, avoid_empty_clusters=True)
    cluster.cluster([vectorspaced(response, words) for response in responses if response])
    classified_examples = [cluster.classify(vectorspaced(response, words)) for response in responses]

    for cluster_id, title in sorted(zip(classified_examples, responses)):
        if not cluster_id in clusters:
            clusters[cluster_id] = [title]
        else:
            clusters[cluster_id].append(title)

    return(clusters)
