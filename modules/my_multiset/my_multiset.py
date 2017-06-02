import os

from modules.my_multiset.arrays import DynamicArray
from modules.my_multiset.question import Question
from modules.my_multiset.questions_dict import Questions_dict
from gensim import corpora, models, similarities


class MyMultiset():
    """
    This class is a simplified dict, where keys are question vectors, values - answers 
    """
    PATH = "/home/ivan/Документи/Slackbot/modules/my_multiset/tmp/"

    def __init__(self):
        self.keys = DynamicArray()
        self.non_answ_questions = Questions_dict()

    def __getitem__(self, item):
        """
        Returns answer to question on given position in keys
        
        :param item: position in self.keys
        :return: answer to the question
        """
        if not (0 <= item < len(self.keys)):
            raise IndexError("Key index out of range")

        return self.keys[item].get_value()

    def __len__(self):
        return self.keys

    def add_key(self, question,value=None):
        """
        Adds key(class Question object to self.keys)
        
        :param quest_vec: question characteristic
        :param question: question to add
        :param value: 
        :return: 
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
        :return: 
        """
        return Question(question, value, user)

    def get_keys(self):
        """
        Return generator of keys
                
        :return: generator object of keys
        """
        for index in range(len(self.keys)):
            yield self.keys[index]

    def get_questions(self):
        """
        Get list of questions as list of strings

        :return: 
        """
        keys = list(self.get_keys())
        questions = list(map(lambda x: x.get_question(), keys))
        return questions

    @staticmethod
    def read_from_file(filename):
        """
        Read lines from file
        
        :param filename: str, name of file to read from
        :return: 
        """
        with open(filename, "r") as file:
            return file.readlines()

    @staticmethod
    def write_to_file(texts):
        """
        Write texts(e.g. processed questions) to file
        :param texts: list(list)
        :return: 
        """
        with open(MyMultiset.PATH + "texts", 'w') as file:
            for text in texts:
                file.write(" ".join(text) + "\n")

    def make_corpus(self):
        """
        Makes corpus of questions
        
        :return: corpus represented in list
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
            lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=6)
            lsi.save(MyMultiset.PATH + "model.lsi")
        else:
            tfidf.save(MyMultiset.PATH + "model.tfidf")
        return

    @staticmethod
    def load_model(model):
        return models.LsiModel.load(MyMultiset.PATH + "model." + model)

    def find_similarities(self, corpus, model, question, user):
        """
        Find percentage of similarity of each question with given one
        
        :param model: list(list)
        :param question: str
        :return: 
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
        if highest_similarity > 0.99:
            index = sims[0][0]
            value = self[index]
            return value
        else:
            self.non_answ_questions.add_question(question)
            return 0