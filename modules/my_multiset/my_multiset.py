"""
# Contain MyMultiset ADT
"""

from gensim import corpora, models, similarities

from modules.my_multiset.arrays import DynamicArray
from modules.my_multiset.question import Question


class MyMultiset():
    """
    This class is a simplified dict, where keys are question vectors, values - answers 
    """
    import os
    PATH = os.getcwd() + "/modules/my_multiset/tmp/"

    def __init__(self):
        self.keys = DynamicArray()

    def __getitem__(self, item):
        """
        Return answer to question on given position in keys
        
        :param item: position in self.keys
        :return: answer to the question
        """
        if not (0 <= item < len(self.keys)):
            raise IndexError("Key index out of range")

        return self.keys[item].get_value()

    def __len__(self):
        return self.keys.__len__()

    def add_key(self, question,value=None):
        """
        Add key(class Question object to self.keys)

        :param question: question to add
        :param value: answer to the question
        :return: None
        """
        if not isinstance(question, str):
            self.keys.append(question)
            return

        key = self.create_Question_obj(question, value)
        self.keys.append(key)

    @staticmethod
    def create_Question_obj(question,value=None, user=None):
        """
        Create Question object with given parameters
        
        :param question: str
        :param value: str
        :param quest_vec: str 
        :return: class Question object
        """
        return Question(question, value, user)

    def get_keys(self):
        """
        Return generator of keys in self.keys

        :return: generator object of values of keys
        """
        for index in range(len(self.keys)):
            yield self.keys[index]

    def get_questions(self):
        """
        Get list of questions

        :return: list(str)
        """
        keys = list(self.get_keys())
        questions = list(map(lambda x: x.get_question(), keys))
        return questions

    def get_values(self):
        """

        :return:
        """
        keys = list(self.get_keys())
        answers = list(map(lambda x: x.get_value(), keys))
        return answers

    @staticmethod
    def read_from_file(filename):
        """
        Read lines from file
        
        :param filename: str, name of file to read from
        :return: list
        """
        with open(filename, "r") as file:
            return file.readlines()

    @staticmethod
    def write_to_file(texts):
        """
        Write texts(e.g. processed questions) to file

        :param texts: list(list)
        :return: None
        """
        with open(MyMultiset.PATH + "texts.txt", 'w') as file:
            for text in texts:
                file.write(" ".join(text) + "\n")

    def make_corpus(self):
        """
        Make corpus of questions
        Save corpus to file
        
        :return: None
        """
        from modules.my_multiset.my_corpus import MyCorpus

        questions = self.get_questions()
        # remove common words and tokenize
        stoplist = set(MyMultiset.read_from_file("/home/ivan/Документи/Slackbot/docs/ukrainian-stopwords.txt"))
        texts = [[word for word in question.lower().split() if word not in stoplist]
                 for question in questions]
        MyMultiset.write_to_file(texts)

        # make mappings between words and their ids
        dictionary = corpora.Dictionary(texts)
        # store the dictionary
        dictionary.save(MyMultiset.PATH + "gensim_dictionary.dict")

        # create corpus
        corpus = list(MyCorpus(dictionary, MyMultiset.PATH + "texts"))
        corpora.MmCorpus.serialize(MyMultiset.PATH + 'corpus.mm', corpus)
        return

    @staticmethod
    def load_corpus():
        # Read corpus from file
        return corpora.MmCorpus(MyMultiset.PATH + "corpus.mm")

    def make_model(self, corpus, model):
        """
        Make vectors of given corpus represented in model to compare them
        Save the model to file
        
        :param corpus: corpus of questions, list(list)
        :param model: tf-idf or lsi
        :return: None
        """
        dictionary = corpora.Dictionary.load(MyMultiset.PATH + "gensim_dictionary.dict")
        tfidf = models.TfidfModel(corpus)

        # apply transformation to whole corpus
        corpus_tfidf = tfidf[corpus]

        if model is "lsi":
            # create lsi model
            lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=5)
            lsi.save(MyMultiset.PATH + "model.lsi")
        else:
            tfidf.save(MyMultiset.PATH + "model.tfidf")
        return

    @staticmethod
    def load_model(model):
        return models.LsiModel.load(MyMultiset.PATH + "model." + model)

    def find_similarities(self, corpus, model, question, user):
        """
        Find percentage of similarity of each question in model with given one

        :param corpus: list(list)
        :param model: list(list)
        :param question: str
        :param user: Slack user id
        :return: list(list), inner list is a sequence number of question with percentage similarity to given one
        """
        # read corpora dictionary from file
        dictionary = corpora.Dictionary.load(MyMultiset.PATH + "gensim_dictionary.dict")

        # create question object
        question_obj = self.create_Question_obj(question, user=user)

        # convert question to vector
        vec_bow = dictionary.doc2bow(question.split())

        # convert question to LSI space
        vec_lsi = model[vec_bow]

        # initialize matrix of similarities
        index = similarities.MatrixSimilarity(model[corpus])

        sims = index[vec_lsi]
        return sims, question_obj

    def find_most_similar(self, similarities):
        """
        Find most similar question
        
        :param similarities: list(list) created in find_similarities method
        :return: str/int
        """
        sims = sorted(enumerate(similarities), reverse=True, key=lambda x: x[1])
        highest_similarity = sims[0][1]
        if highest_similarity > 0.99:
            index = sims[0][0]
            value = self[index]
            return value
        else:
            return 0