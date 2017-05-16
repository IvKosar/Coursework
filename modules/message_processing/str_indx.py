import os
from gensim import corpora,models,similarities

#import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def from_str_to_vec():
    '''documents = [
        "It is not so important for this problem but turn 1pk",
        "This thing is not very important for the problem mentioned but return 1pk",
        "This case is not important for the given problem, but turn 1pk"
    ]'''
    documents = [
        "One two three four five six one",
        "six seven eight nine ten twelve",
        "eleven twelve thirteen fourteen six",
    ]

    # remove common words and tokenize
    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in document.lower().split() if word not in stoplist]
             for document in documents]
    #print(texts)

    # remove words that appear only once
    '''from collections import defaultdict
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    
    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]
    '''
    from pprint import pprint
    #pprint(texts)


    # make mappings between words and their ids
    dictionary = corpora.Dictionary(texts)
    dictionary.save("/tmp/deerwester.dict") # store the dictionary, for future reference
    #print(dictionary)

    # convert tokenized documents to vectors
    new_doc = "one six ten"
    new_vec = dictionary.doc2bow(new_doc.lower().split())
    #print(new_vec)

    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('/tmp/deerwester.mm', corpus)
    pprint(corpus)

    # another way to convert tokenized documents to vectors using class
    class MyCorpus(object):
        def __iter__(self):
            for line in texts:
                yield dictionary.doc2bow(line)

        def __str__(self):
            res_str = ''
            for vector in self:
                res_str += str(vector) + '\n'

            return res_str


    corpus_mem_friend = MyCorpus()
    print((corpus_mem_friend))

    # read corpus from file
    corpus = corpora.MmCorpus('/tmp/deerwester.mm')
    #print(corpus)
    #pprint(list(corpus))

def topics_and_transformations():
    # read dictionary and corpus from files
    dictionary = corpora.Dictionary.load("/tmp/deerwester.dict")
    corpus = corpora.MmCorpus("/tmp/deerwester.mm")
    #print(corpus)

    # initialize transformation
    tfidf = models.TfidfModel(corpus)

    # apply transformation to whole corpus
    corpus_tfidf = tfidf[corpus]
    for doc in corpus_tfidf:
        print(doc)
    print("------------------------------------------------------")

    lsi = models.LsiModel(corpus_tfidf,id2word=dictionary,num_topics=2)
    corpus_lsi = lsi[corpus_tfidf]
    for doc in corpus_lsi:
        print(doc)

    lsi.save("/tmp/model.lsi")
    lsi = models.LsiModel.load("/tmp/model.lsi")

if __name__ == "__main__":
    from_str_to_vec()
    topics_and_transformations()