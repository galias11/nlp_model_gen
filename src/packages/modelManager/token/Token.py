class Token:
    __base_form = '',
    __is_out_of_vocabulary = False
    __part_of_speech = ''
    __sentence = 0.0
    __sentiment = '' # Experimental
    __tag = ''
    __token_text = ''

    def __init__(self, base_form, is_out_of_vocabulary, part_of_speech, sentence, sentiment, tag, token_text):
        self.__base_form = base_form
        self.__is_out_of_vocabulary = is_out_of_vocabulary
        self.__part_of_speech = part_of_speech
        self.__sentence = sentence
        self.__sentiment = sentiment
        self.__tag = tag
        self.__token_text = token_text

    def to_dict(self):
        """
        Devuelve los atributos del objeto en Diccionario de Python

        :return: [Dict] - Diccionario con los datos del token.
        """
        return {
            'base_form': self.__base_form,
            'is_out_of_vocabulary': self.__is_out_of_vocabulary,
            'part_of_speech': self.__part_of_speech,
            'sentence': self.__sentence,
            'sentiment': self.__sentiment,
            'tag': self.__tag,
            'token_text': self.__token_text
        }