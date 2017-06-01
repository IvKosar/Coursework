from modules.message_processing.translate import translate_whole

class Question():
    """
    Represents question
    """
    def __init__(self, question, value=None, user=None):
        """
        
        :param que_vec: list, characteristic of question
         example: [(1,1),(3,2)]
        :param question: str
        :param value: str, answer to the question
        """
        self._question_in_eng = question.lower() #translate_whole(question).lower()
        self._value = value
        self._user = user

    def set_value(self, value):
        self._value = value

    def set_que_vec(self, que_vec):
        self._que_vec = que_vec

    def get_user(self):
        """
        Return question vector
        
        :return: list
        """
        return self._user

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
