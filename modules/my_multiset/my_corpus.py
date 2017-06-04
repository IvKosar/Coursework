"""
# Contain class for converting strings to vectors
# Each string is converted into vector, which represent frequency of
# each word in string
"""

class MyCorpus():
    """
    Memory friendly representation of corpus as simple generator
    """
    def __init__(self,dictionary, texts):
        """
        
        :param dictionary: representation of the question
        :param texts: filename, where questions are stored
        """
        self.dictionary = dictionary
        self.texts = texts


    def __iter__(self):
        """
        iterate over read strings
        covert them to vectors

        :return: generator
        """
        file = open(self.texts)
        for line in file:
            if line:
                yield self.dictionary.doc2bow(line.split())
        file.close()
