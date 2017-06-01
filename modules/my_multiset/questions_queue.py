"""
# Contain class of non-answered questions
"""

from modules.my_multiset.queue import Queue

class Questions_queue(object):
    """
    Queue of non-answered questions
    """
    def __init__(self):
        self._queue = Queue()

    def is_non_answered(self):
        """
        Check for questions without answers

        :return:
        """
        return not self._queue.isEmpty()

    def add_question(self, question):
        """
        Add question to queue of non-answered questions

        :param question:
        :return:
        """
        self._queue.enqueue(question)

    def get_quest_to_answer(self):
        """
        Get first non-answered question

        :return:
        """
        return self._queue.peek()

    def remove_question(self):
        return self._queue.dequeue()