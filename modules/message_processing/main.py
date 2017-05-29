import os
from modules.my_multiset.my_multiset import MyMultiset
from modules.message_processing.get_questions import get_questions, remove_addresing


def main(message, multiset):
    """
    Make all operations with read message:
    -detect whether it's question
    -if so create corpus, make linguistic model, 
     find most similar to given question
    
    :param message: str, latest message from Slack channel
    :param multiset: created multiset of questions
    :return: int/str
    """
    if is_question(message):
        message = remove_addresing(message)
        multiset.make_corpus()
        corpus = MyMultiset.load_corpus()

        # in next versions best model detection will be added
        # now it's lsi model by default, which is the most universal
        multiset.make_model(corpus, "lsi")
        model = MyMultiset.load_model("lsi")

        similarities = multiset.find_similarities(corpus, model, message)
        # answer to the question most similar to given
        most_similiar = multiset.find_most_similar(similarities, message)
        return most_similiar
    else:
        return 1

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
    return "?" in message
