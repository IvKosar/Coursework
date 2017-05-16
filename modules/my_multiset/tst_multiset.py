from pprint import pprint

from arrays import DynamicArray

from modules.my_multiset import MyMultiset


def test():
    lst = DynamicArray()
    lst.append(1)
    print(lst[0])

def test_multiset():
    # initialize MyMultiset
    dictionary = MyMultiset()

    # add keys
    dictionary.add_key("one two three six","sasa")
    dictionary.add_key("four five six ten",'fff')
    dictionary.add_key("five seven nine ten",'aaa')

    # test get keys
    keys = list(dictionary.get_keys())

    # test get_key_value
    que_vec = [1,3,4]
    print(dictionary.get_key_value(que_vec))

    # test get_questions
    questions = dictionary.get_questions()
    print(questions)

    # test_make_corpus
    corpus = dictionary.make_corpus()
    pprint(corpus)

    # test make_model
    tf_idf = dictionary.make_model(corpus, "tf-idf")

    # test find_similarities
    similarities = dictionary.find_similarities(tf_idf, "three four  ten")

    # test find_most_similar
    most_similar = dictionary.find_most_similar(similarities)
    print(most_similar)


if __name__ == "__main__":
    test_multiset()