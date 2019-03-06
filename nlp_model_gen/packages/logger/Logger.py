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
    def log(code, inserted_texts=''):
        """
        Loggea por consola un texto. Reemplaza dentro del mismo los distintos wildcards con la
        información provista en los textos insertados.

        :code: [String] - Código de la acción a loguear.
        """
        if not code in LOG_DATA.keys():
            return
        class_name = LOG_DATA[code]['class_name'] 
        method_name = LOG_DATA[code]['method_name'] 
        main_text = Logger.get_main_text_color(LOG_DATA[code]['main_text'], LOG_DATA[code]['type'])
        log_id_text = '[ ' + Logger.get_current_time() + ' |' + colored(class_name, CLASS_COLOR) + '|' + colored(method_name, METHOD_COLOR) + '| ]: '
        formatted_text = main_text
        for text in inserted_texts:
            formatted_text = formatted_text.replace(LOGGER_WILDCARD, colored(text['text'], text['color']), 1)
        print(log_id_text + formatted_text)
        