# @Vendors
import datetime
from termcolor import colored

# @Constants
from nlp_model_gen.constants.constants import LOGGER_WILDCARD, STD_TIME_OUTPUT

# @Colors
from .assets.logColors import (
    CLASS_COLOR,
    ERROR_COLOR,
    INFO_COLOR,
    METHOD_COLOR,
    SUCCESS_COLOR,
    WARNING_COLOR
)
from .assets.logTexts import (
    LOG_DATA,
    TYPE_INFO,
    TYPE_ERR,
    TYPE_WRN,
    TYPE_SUCCESS
)

class Logger:
    def __init__(self):
        pass

    @staticmethod
    def get_current_time():
        """
        Devuelve una cadena de caracteres con la fecha y hora actual.

        :return: [String] - Cadena con la fecha y hora actual.
        """
        current_date = datetime.datetime.now()
        return current_date.strftime(STD_TIME_OUTPUT)

    @staticmethod
    def get_main_text_color(text, type):
        """
        Formatea al texto principal con un color de acuerdo a su tipo de información
        """
        if type == TYPE_INFO:
            return colored(text, INFO_COLOR)
        if type == TYPE_ERR:
            return colored(text, ERROR_COLOR)
        if type == TYPE_WRN:
            return colored(text, WARNING_COLOR)
        if type == TYPE_SUCCESS:
            return colored(text, SUCCESS_COLOR)
        return text

    @staticmethod
    def format_composed_text(code, inserted_texts):
        """
        Construye el texto con textos insertados (permite recuperar el color original luego 
        de usar otro).

        :code: [String] - Código de acción a loguear

        :inserted_texts: [List(String)] - Lista de textos a insertar.

        :return: [String] - texto formateado
        """
        main_text = LOG_DATA[code]['main_text']
        splitted_texts = main_text.split(LOGGER_WILDCARD)
        splitted_length = len(splitted_texts)
        if not inserted_texts or not splitted_length - 1 == len(inserted_texts):
            return Logger.get_main_text_color(main_text, LOG_DATA[code]['type'])
        formatted_text = Logger.get_main_text_color(splitted_texts[0], LOG_DATA[code]['type'])
        for pos, text in enumerate(inserted_texts, 1):
            formatted_inserted_text = colored(text['text'], text['color'])
            splitted_text = splitted_texts[pos]
            formatted_splitted_text = Logger.get_main_text_color(splitted_text, LOG_DATA[code]['type'])
            formatted_text = formatted_text + formatted_inserted_text + formatted_splitted_text
        return formatted_text

    @staticmethod
    def log(code, inserted_texts=None):
        """
        Loggea por consola un texto. Reemplaza dentro del mismo los distintos wildcards con la
        información provista en los textos insertados.

        :code: [String] - Código de la acción a loguear.
        """
        if not code in LOG_DATA.keys():
            return
        class_name = LOG_DATA[code]['class_name']
        method_name = LOG_DATA[code]['method_name']
        log_id_text = '[ ' + Logger.get_current_time() + ' |' + colored(class_name, CLASS_COLOR) + '|' + colored(method_name, METHOD_COLOR) + '| ]: '
        formatted_text = Logger.format_composed_text(code, inserted_texts)
        print(log_id_text + formatted_text)
