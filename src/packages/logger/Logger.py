# @Vendors
from termcolor import colored

# @Constants
from src.constants.constants import LOGGER_WILDCARD

class Logger:
    def __init__(self):
        pass

    @staticmethod
    def log(main_text, inserted_texts=None):
        """
        Loggea por consola un texto. Reemplaza dentro del mismo los distintos wildcards con la
        información provista en los textos insertados.

        :main_text: [String] - texto principal

        :inserted_texts: [List(Dict)] - Textos insertados con sus caracteristicas.
        """
        if inserted_texts is None:
            print(main_text)
            return
        formatted_text = main_text
        for text in inserted_texts:
            formatted_text = formatted_text.replace(LOGGER_WILDCARD, colored(text['text'], text['color']), 1)
        print(formatted_text)
        