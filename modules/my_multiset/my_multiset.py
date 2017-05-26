import os

from arrays import DynamicArray
from question import Question
from gensim import corpora, models, similarities


class MyMultiset():
    """
    This class is a simplified dict, where keys are question vectors, values - answers 
    """
    PATH = os.getcwd() + "/tmp/"

    def __init__(self):
        self.keys = DynamicArray()

    def __getitem__(self, item):
        if not (0 <= item < len(self.keys)):
            raise IndexError("Key index out of range")

        return self.keys[item].get_value()

    def add_key(self, question,value=None):
        """
        Adds key(class Question object to self.keys)
        
        :param quest_vec: question characteristic
        :param question: question to add
        :param value: 
        :return: 
        """
        key = self.create_Question_obj(question, value)
        self.keys.append(key)

    @staticmethod
    def create_Question_obj(question,value, quest_vec=None):
        """
        Create Question object with given parameters
        
        :param question: str
        :param value: str
        :param quest_vec: str 
        :return: 
        """
        return Question(question, value, quest_vec)

    def get_keys(self):
        """
        Return generator of keys
                
        :return: generator object of keys
        """
        for index in range(len(self.keys)):
            yield self.keys[index]


    def get_key_value(self,que_vec):
        """
        Get answer to the given question
        
        :param que_vec: list
        :return: attribute value of given Question object
        """
        for index in range(len(self.keys)):
            if self.keys[index].get_que_vec() == que_vec:
                return self.keys[index].get_value()

        raise KeyError()


    def get_questions(self):
        """
        Get list of questions as list of strings

        :return: 
        """
        keys = list(self.get_keys())
        questions = list(map(lambda x: x.get_question(), keys))
        return questions


    def make_corpus(self):
        """
        Makes corpus of questions
        
        :return: corpus represented in list
        """
        from my_corpus import MyCorpus

        questions = self.get_questions()
        # remove common words and tokenize
        stoplist = set('for a of the and to in'.split())
        texts = [[word for word in question.lower().split() if word not in stoplist]
                 for question in questions]

        # make mappings between words and their ids
        dictionary = corpora.Dictionary(texts)
        # store the dictionary
        dictionary.save(MyMultiset.PATH + "gensim_dictionary.dict")

        # create corpus
        corpus = list(MyCorpus(dictionary, texts))
        corpora.MmCorpus.serialize(MyMultiset.PATH + 'corpus.mm', corpus)
        return

    @staticmethod
    def load_corpus():
        return corpora.MmCorpus(MyMultiset.PATH + "corpus.mm")

    def make_model(self, corpus, model):
        """
        Make vectors of given corpus represented in model to compare them
        
        :param corpus: corpus of questions, list(list)
        :param model: tf-idf or lsi(lsa)
        :return: 
        """
        dictionary = corpora.Dictionary.load(MyMultiset.PATH + "gensim_dictionary.dict")
        tfidf = models.TfidfModel(corpus)

        # apply transformation to whole corpus
        corpus_tfidf = tfidf[corpus]

        if model is "lsi":
            # create lsi model
            lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
            lsi.save(MyMultiset.PATH + "model.lsi")
        else:
            tfidf.save(MyMultiset.PATH + "model.tfidf")
        return

    @staticmethod
    def load_model(model):
        return models.LsiModel.load(MyMultiset.PATH + "model." + model)

    def find_similarities(self, corpus, model, question):
        """
        Find percentage of similarity of each question with given one
        
        :param model: list(list)
        :param question: str
        :return: 
        """
        # read corpora dictionary from file
        dictionary = corpora.Dictionary.load(MyMultiset.PATH + "gensim_dictionary.dict")

        # create question object
        question_obj = Question(question)
        question = question_obj.get_question()

        # convert question to vector
        vec_bow = dictionary.doc2bow(question.split())

        # convert question to LSI space
        vec_lsi = model[vec_bow]

        # initialize matrix of similarities
        index = similarities.MatrixSimilarity(model[corpus])

        sims = index[vec_lsi]
        return sims

    def sort(self, reverse = False):
        """
        Sort list of similarities
        
        :return: 
        """
        pass

    def find_most_similar(self, similarities, question):
        """
        Find most similar question
        
        :param similarities: 
        :return: 
        """
        sims = sorted(enumerate(similarities), reverse=True, key=lambda x: x[1])
        highest_similarity = sims[0][1]
        if highest_similarity > 0.9:
            index = sims[0][0]
            value = self[index]
            return value
        else:
            self.add_key(question)
            return 0