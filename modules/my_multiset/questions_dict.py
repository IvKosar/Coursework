"""
# Contain class for non-answered questions
"""

class Questions_dict(object):
    """
    Dictionary of non-answered questions.
    Key is user id, value is question object
    """
    def __init__(self):
        self._dict = {}

    def is_non_answered(self):
        """
        Check for questions without answers

        :return: bool
        """
        return self._dict != dict()

    def add_question(self, question):
        """
        Add question to dict of non-answered questions

        :param question: Question object
        :return: None
        """
        user = question.get_user()
        self._dict[user] = question

    def get_quest_to_answer(self, user):
        """
        Get non-answered question by user

        :param user: str, user id
        :return: Question object
        """
        return self._dict[user]

    def remove_question(self, user):
        """
        Remove question from queue(answer was found)

        :return: None
        """
        del(self._dict[user])

    def get_users(self):
        """
        Get users whose questions are in dict

        :return: set
        """
        return set(self._dict.keys())