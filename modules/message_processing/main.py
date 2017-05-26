from modules.my_multiset.my_multiset import MyMultiset
from modules.message_processing.get_questions import get_questions

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
        corpus = multiset.make_corpus()
        # in next versions best model detection will be added
        # now it's lsi model by default, which is the most universal
        model = multiset.make_model(corpus, "lsi")
        similarities = multiset.find_similarities(model, message)
        most_similiar = multiset.find_most_similar(similarities)
        return most_similiar
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
    return "?" in message

