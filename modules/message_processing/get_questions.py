import os
from modules.my_multiset.question import Question


def get_questions():
    """
    get list of questions
    
    :return: 
    """
    questions = []
    with open("/home/ivan/Документи/Slackbot/docs/answers_base", "r") as file:
        values = file.readlines()

    i = 0
    with open(os.getcwd() + "/modules/message_processing/messages", 'r') as file:
        for line in file:
            message = eval(line)
            if "?" in message['text']:
                new_message = remove_addresee(message["text"])
                question = (new_message, values[i])
                questions.append(question)
                i += 1
    return questions


def check_for_addressee(message_text):
    """
    Check whether message has id of user to whom this message is written

    :param message_text:
    :return:
    """
    return ("<@" in message_text or "<!" in message_text) and ">" in message_text


def get_addressee_to_remove(message_text):
    """
    Get id to whom message is written
    
    :return: 
    """
    lbracket_indx = message_text.index("<")
    rbracket_indx = message_text.index(">")
    addressator = message_text[lbracket_indx:rbracket_indx]
    addressator = addressator[1:]
    return addressator


def get_addressee(message_text):
    """
    Extract addressator from
    :param message_text:
    :return:
    """
    return get_addressee_to_remove(message_text)[1:]


def remove_addresee(message_text):
    while "<" in message_text and ">" in message_text:
        addressator = get_addressee_to_remove(message_text)
        message_text = message_text.replace(addressator, "")
        message_text = message_text.replace("?", "")
        message_text = message_text.replace("<>", "").strip()
    return message_text


if __name__ == "__main__":
    #print(remove_addresing("<@dfdfd>  dfd"))
    print(get_questions())
