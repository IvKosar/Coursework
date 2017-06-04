"""
# Module for processing messages which were got from Slack channel history
# Find questions in this messages
# Make question-answer pairs
"""
import os
from modules.my_multiset.question import Question


def get_questions():
    """
    Make list of question-answer pairs
    
    :return: list(tuple)
    """
    # read answers
    questions = []
    with open(os.getcwd() + "/docs/answers_base", "r") as file:
        values = list(map(lambda x: x.strip(), file.readlines()))

    # find questions
    # make pairs
    i = 0
    with open("/home/ivan/Документи/Slackbot" + "/docs/messages", 'r') as file:
        for line in file:
            message = eval(line)
            if "?" in message['text']:
                new_message = remove_addressee(message["text"])
                question = (new_message, values[i])
                questions.append(question)
                i += 1
    return questions


def check_for_addressee(message_text):
    """
    Check whether message has id of user to whom this message is written

    :param message_text: str
    :return: bool
    """
    return ("<@" in message_text or "<!" in message_text) and ">" in message_text


def get_addressee_to_remove(message_text):
    """
    Get id to whom message is written(string which is between triangle braces)
    
    :return: 
    """
    lbracket_indx = message_text.index("<")
    rbracket_indx = message_text.index(">")
    addressator = message_text[lbracket_indx:rbracket_indx]
    addressator = addressator[1:]
    return addressator


def get_addressee(message_text):
    """
    Extract addressee from string between triangle braces(the same string without '@' or '!')
    :param message_text: str
    :return: str

    Example: input: "@userid"
             output: userid
    """
    return get_addressee_to_remove(message_text)[1:]


def remove_addressee(message_text):
    """
    :param message_text: str
    :return: message without addressee and punctuation marks
    """
    import string
    while "<" in message_text and ">" in message_text:
        addressator = get_addressee_to_remove(message_text)
        message_text = message_text.replace(addressator, "")
        message_text = message_text.replace("<>", "").strip()

    # remove punctuation marks
    punctuation = string.punctuation.replace("<", "").replace(">", "")
    for c in punctuation:
        message_text = message_text.replace(c, "")

    return message_text.strip()


if __name__ == "__main__":
    from pprint import pprint
    print(remove_addresing("<@dfdfd>  dfd"))
    pprint(get_questions())
