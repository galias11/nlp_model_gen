# @Classes
from ..task.Task import Task

class TextAnalysisTask(Task):
    __model_id = -1
    __text = ''
    __only_positives = False

    def __init__(self, model_id, text, only_positives):
        self.__model_id = model_id
        self.__text = text
        self.__only_positives = only_positives

    def get_model_id(self):
        return self.__model_id

    def get_text(self):
        return self.__text

    def is_only_positives(self):
        return self.__only_positives

    def task_init_hook(self):
        """
        Método hook para completar el template de inicializadion en el padre.
        """
        pass

    def get_task_data(self):
        """
        Retorna los datos de la tarea.

        :return: [Dict] - Diccionario con los datos de la tarea.
        """
        return {
            'model_id': self.get_model_id(),
            'text': self.get_text(),
            'only_positives': self.is_only_positives()
        }
    