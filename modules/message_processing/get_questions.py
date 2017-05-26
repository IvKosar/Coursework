#from modules.my_multiset.question import Question


def get_questions():
    """
    get list of questions
    
    :return: 
    """
    questions = []
    with open("messages", 'r') as file:
        for line in file:
            message = eval(line)
            if "?" in message.text:
                new_message = remove_addresing(message.text)

def get_addressator_to_remove(message_text):
    """
    Get id to who message is written
    
    :return: 
    """
    if "<" and ">" in message_text:
        lbracket_indx = message_text.index("<")
        rbracket_indx = message_text.index(">")
        addressator = message_text[lbracket_indx:rbracket_indx]
        addressator = addressator[1:]
        return addressator

def get_addressator(message_text):
    return get_addressator_to_remove(message_text)[1:]

def remove_addresing(message_text):
    addressator = get_addressator_to_remove(message_text)
    message_text = message_text.replace(addressator, "")
    message_text = message_text.replace("<>", "").strip()

    return message_text

if __name__ == "__main__":
    print(remove_addresing("<@dfdfd>  dfd"))
