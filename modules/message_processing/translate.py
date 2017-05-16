# Imports the Google Cloud client library
from google.cloud import translate
A = 12
# Instantiates a client
translate_client = translate.Client()

# The text to translate
def translate_by_word(text):
    """
    Translate given sentence to english
    :param text: 
    :return: 
    """
    split_text = text.split()

    # The target language
    target = 'en'

    # Translates some text into English word-by-word
    translated_text = ""
    for word in split_text:
        encoded_word = word.encode("utf-8")
        translation = translate_client.translate(
                             word,
                             target_language=target)
        translated_text += translation['translatedText'] + ' '

    return translated_text[:-1]


# Whole sentence translation
def translate_whole(text):
    target = 'en'
    translation = translate_client.translate(
                                 text,
                                 target_language=target)
    translated_text = translation['translatedText']

    return translated_text

if __name__ == "__main__":
    text = 'Це не так важливо для цієї задачі але так повертайте 1pk'
    translated_text = translate_whole(text)
    print(u'Text: {}'.format(text))
    print(u'Translation: {}'.format(translated_text))