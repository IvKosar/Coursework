class MyCorpus():
    """
    Memory_friendly representation of corpus as simple generator
    """
    def __init__(self,dictionary, texts):
        """
        
        :param dictionary: representation of the question
        :param texts: filename, where questions are stored
        """
        self.dictionary = dictionary
        self.texts = texts


    def __iter__(self):
        file = open(self.texts)
        for line in file:
            if line:
                yield self.dictionary.doc2bow(line.split())
        file.close()

    def __str__(self):
        res_str = ''
        for vector in self:
            res_str += str(vector) + '\n'

        return res_str
