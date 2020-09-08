from gensim import corpora,models,similarities

_tfidf=None
_dictionary=None
_corpus=None

def build(corpus,dictionary):
    global _tfidf
    global _dictionary
    global _corpus
    _tfidf = models.TfidfModel(corpus)
    _dictionary = dictionary
    _corpus=corpus

def analyse(item):
    global _tfidf
    global _dictionary
    global _corpus
    index = similarities.SparseMatrixSimilarity(_tfidf[_corpus], num_features=len(_dictionary.keys()))
    sim = index[_tfidf[item]]
    return sorted(enumerate(sim), key=lambda item: -item[1])