from gensim import corpora

dictionary = None

def build(doc):
    global dictionary
    dictionary = corpora.Dictionary(doc)
    return [test(item) for item in doc]

def test(item):
    global dictionary
    return dictionary.doc2bow(item)