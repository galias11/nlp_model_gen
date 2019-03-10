# @Classes
from ..task.Task import Task

class ModelCreationTask(Task):
    __model_name = ''
    __description = ''
    __author = ''
    __tokenizer_exceptions = dict({})

    def __init__(self, model_name, description, author, tokenizer_exceptions):
        self.__model_name = model_name
        self.__description = description
        self.__author = author
        self.__tokenizer_exceptions = tokenizer_exceptions

    def get_model_name(self):
        return self.__model_name

    def get_description(self):
        return self.__description

    def get_author(self):
        return self.__author

    def get_tokenizer_exceptions(self):
        return self.__tokenizer_exceptions

    def task_init_hook(self):
        """
        Método hook para completar el template de inicializadion en el padre.
        """
        pass

    def get_task_data(self):
        """
        Devuelve los datos de la tarea.

        :return: [Dict] - Diccionario con los datos de la tarea.
        """
        return {
            'model_name': self.get_model_name(),
            'description': self.get_description(),
            'author': self.get_author(),
            'tokenizer_exceptions': self.get_tokenizer_exceptions()
        }
