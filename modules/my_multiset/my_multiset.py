import os

from arrays import DynamicArray
from question import Question
from gensim import corpora


class MyMultiset():
    """
    This class is a simplified dict, where keys are question vectors, values - answers 
    """
    def __init__(self):
        self.keys = DynamicArray()


    def add_key(self, question,value, quest_vec=None):
        """
        Adds key(class Question object to self.keys)
        
        :param quest_vec: question characteristic
        :param question: question to add
        :param value: 
        :return: 
        """
        key = Question(question,value, quest_vec)
        self.keys.append(key)


    def remove_key(self, key_vec):
        """
        Removes key from self.keys by given question vector
        
        :param key_vec: list
        :return:
        """
        for i in range(len(self.keys)):
            if self.keys[i].que_vec == key_vec:
                self.keys.remove(key)

        raise KeyError()


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
        path = os.path.join(os.getcwd() + '/tmp/' + "corpus.dict")
        dictionary.save(path)

        corpus = list(MyCorpus(dictionary, texts))
        return corpus

    def make_model(self, corpus, model):
        """
        Make vectors of given corpus represented in model to compare them
        
        :param corpus: corpus of questions, list(list)
        :param model: tf-idf or lsi(lsa)
        :return: 
        """
        pass


    def find_similarities(self, model, question):
        """
        Find percentage of similarity of each question with given one
        
        :param model: list(list)
        :param question: str
        :return: 
        """
        pass


    def sort(self, reverse = False):
        """
        Sort list of similarities
        
        :return: 
        """
        pass


    def find_most_similar(self, similarities):
        """
        Find most similar question
        
        :param similarities: 
        :return: 
        """
        pass