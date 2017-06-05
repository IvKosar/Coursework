"""
# Module for processing received message
# Create multiset object
"""

import os
from modules.my_multiset.my_multiset import MyMultiset
from modules.message_processing.get_questions import get_questions, remove_addressee, \
    check_for_addressee, get_addressee


def main(message, multiset, non_answ_dict, user):
    """
    Make all operations with read message:
    - detect whether it's question
    - if so create corpus, make linguistic model,
     find most similar to given question
    - detect whether the message is an answer to unanswered question
    - if so add it to questions base
    
    :param message: str, latest message from Slack channel
    :param multiset: created multiset of questions, MyMultiset object
    :param non_answ_dict: created Questions_dict object for storing questions without answers
    :param user: id of user who asked question
    :return: int/str
    """
    if is_question(message):
        message = remove_addressee(message)
        multiset.make_corpus()
        corpus = MyMultiset.load_corpus()

        # in next versions detection of most appropriate model will be added
        # now it's lsi model by default, which is the most universal
        multiset.make_model(corpus, "lsi")
        model = MyMultiset.load_model("lsi")

        similarities, question_object = multiset.find_similarities(corpus, model, message, user)
        print(question_object.get_user())

        # answer to the question most similar to given
        most_similiar = multiset.find_most_similar(similarities)
        if most_similiar:
            return (most_similiar, 0)
        else:
            non_answ_dict.add_question(question_object)
            print(non_answ_dict.is_non_answered())
            return (message, 1)
    elif is_answer(multiset, non_answ_dict, message):
        return 1
    else:
        return 0

def create_multiset():
    """
    Create new MyMultiset object for storing questions

    :return: MyMultiset object
    """
    my_multiset = MyMultiset()
    questions = get_questions()
    for question in questions:
        my_multiset.add_key(question[0], question[1])

    return my_multiset

def is_question(message):
    """
    Detect whether message is a question

    :param message: str
    :return: bool
    """
    return "?" in message

def is_answer(multiset,non_answ_dict, message):
    """
    Detect whether message is an answer to one of given questions

    :param multiset: questions base
    :param non_answ_dict: Questions_dict object created after launch
    :param message: str
    :return: bool
    """
    if check_for_addressee(message) is True and non_answ_dict.is_non_answered() is True:
        message_addressee = get_addressee(message)
        users_wait_for_answ = non_answ_dict.get_users()
        if message_addressee in users_wait_for_answ:
            question = non_answ_dict.get_quest_to_answer(message_addressee)
            non_answ_dict.remove_question(message_addressee)
            message = remove_addressee(message)
            question.set_value(message)
            question.set_user_to_None()
            multiset.add_key(question)
            return 1
        else:
            return 0
    else:
        return 0
