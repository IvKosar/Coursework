from modules.message_processing import translate_whole

class Question():
    """
    Represents question
    """
    def __init__(self, question, value, que_vec=None):
        """
        
        :param que_vec: list, characteristic of question
         example: [(1,1),(3,2)]
        :param question: str
        :param value: str, answer to the question
        """
        self._que_vec = que_vec
        self._question_in_eng = translate_whole(question)
        self._value = value


    def get_que_vec(self):
        """
        Return question vector
        
        :return: list
        """
        return self._que_vec

    def get_question(self):
        """
        Return question as str
        
        :return: str
        """
        return self._question_in_eng


    def get_value(self):
        """
        Return answer
        
        :return: str
        """
        return self._value
