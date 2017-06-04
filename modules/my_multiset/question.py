"""
# Contain class Question for storing question and its answer
"""

class Question():
    """
    Represents question
    Attributes: question(required)
                value(not required)
                user(not required)
    """
    def __init__(self, question, value=None, user=None):
        """
        :param question: str
        :param value: str, answer to the question
        :param user: Slack user ID
        """
        self._question = question.lower() #translate_whole(question).lower()
        self._value = value
        self._user = user

    def set_value(self, value):
        """
        Set self.value to given value

        :param value: str, answer to the question
        :return: None
        """
        self._value = value

    def set_user_to_None(self):
        self._user = None

    def get_user(self):
        """
        Return Slack user id
        
        :return: str
        """
        return self._user

    def get_question(self):
        """
        Return question
        
        :return: str
        """
        return self._question


    def get_value(self):
        """
        Return answer
        
        :return: str
        """
        return self._value
