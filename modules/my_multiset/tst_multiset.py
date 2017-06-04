"""
# Module for testing MyMultiset ADT
"""

from pprint import pprint
from modules.my_multiset.my_multiset import MyMultiset
from modules.message_processing.main import create_multiset


def test_multiset():
    # initialize MyMultiset
    dictionary = create_multiset()

    # add keys
    dictionary.add_key("Один два три шість","sasa")
    dictionary.add_key("чотири п'ять шість десять",'fff')
    dictionary.add_key("п'ять сім дев'ять десять",'aaa')

    # test get keys
    keys = list(dictionary.get_keys())

    # test get_questions
    questions = dictionary.get_questions()
    print(questions)

    # test_make_corpus
    dictionary.make_corpus()
    corpus = list(dictionary.load_corpus())
    #pprint(corpus)

    # test make_model
    dictionary.make_model(corpus, "lsi")
    lsi = dictionary.load_model("lsi")
    #print(lsi)

    # test find_similarities
    similarities,quest_obj = dictionary.find_similarities(corpus, lsi, "питання по дз1 equipmentdifferences якщо в одній кімнаті два компютери а в іншій один я повертаю один компютер", "id1")
    print(similarities)

    # test find_most_similar
    most_similar = dictionary.find_most_similar(similarities, quest_obj)
    print(most_similar)


if __name__ == "__main__":
    test_multiset()