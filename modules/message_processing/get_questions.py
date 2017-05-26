from modules.my_multiset.question import Question


def get_questions():
    """
    get list of questions
    
    :return: 
    """
    questions = []
    values = ['pdf або html',
              'так цього достатньо',
              '''Тест почнеться о 20.20 і буде тривати 10 хв. 
              Нагадую що при проходженні тесту потрібно використовувати своє прізвище як ідентифікатор. 
              Як тільки я побачу що хтось зайшов під іншим ідентифікатором я відразу припиню тест і виставлю ті оцінки,
               які будуть на той момент.''',
              'так)',
              'ну то вже як ти вирішиш)',
              ' 5x5 теж підходить по умові',
              'ні',
              'В завданні написано про множину.Отже, повертаємо множину',
              'не накручуйнете Flask, просто на рівні абстракції поки',
              'Як вам подобається. Маєте готовий модуль можете його доробляти чи переробляти',
              '''Користувачу пароль потрібен, хоча в користувача може паролем бути пустий рядок, 
              якщо система дозволить мати такий пароль. 
              Зрозуміло що базу даних користувачів вам реалізовувати не потрібно.''',
              '''Правильно. Якщо перелік обладнання це просто список рядків то тоді якщо є декілька одиниць техніки
              то треба їх всіх в тому списку записувати як окремі рядки.  
              Приклади до цієї задачі до цього і спонукають хоча насправді так представляти обладнання, 
              якщо чогось  може бути декілька одиниць  погано ...''',
              ]
    i = 0
    with open("messages", 'r') as file:
        for line in file:
            message = eval(line)
            if "?" in message['text']:
                new_message = remove_addresing(message["text"])
                question = (new_message, values[i])
                questions.append(question)
                i += 1
    return questions

def get_addressator_to_remove(message_text):
    """
    Get id to who message is written
    
    :return: 
    """
    lbracket_indx = message_text.index("<")
    rbracket_indx = message_text.index(">")
    addressator = message_text[lbracket_indx:rbracket_indx]
    addressator = addressator[1:]
    return addressator

def check_for_addressator(message_text):
    return "<" and ">" in message_text

def get_addressator(message_text):
    return get_addressator_to_remove(message_text)[1:]

def remove_addresing(message_text):
    while "<" and ">" in message_text:
        addressator = get_addressator_to_remove(message_text)
        message_text = message_text.replace(addressator, "")
        message_text = message_text.replace("<>", "").strip()
    return message_text

if __name__ == "__main__":
    #print(remove_addresing("<@dfdfd>  dfd"))
    print(get_questions())
