# @Classes
from ..task.Task import Task

class ModelTrainingTask(Task):
    def __init__(self, model_id, path, examples):
        self.__model_id = model_id
        self.__path = path
        self.__examples = examples

    def get_model_id(self):
        return self.__model_id

    def get_path(self):
        return self.__path

    def get_examples(self):
        return self.__examples

    def init_task_hook(self):
        """
        Método que se ejecutará en el template del init de la task de la clase padre.
        """
        pass

    def check_model_relation(self, model_id, model_name):
        """
        Determina si una tarea esta relacionada con un determinado modelo utilizando su
        id y su nombre

        :model_id: [String] - Id del modelo

        :model_name: [String] - Nombre del modelo

        :return: [boolean] - True si el modelo esta releacionado, False en caso contrario.
        """
        return self.__model_id == model_id

    def get_task_data(self):
        """
        Retorna los datos de la tarea.

        :return: [Dict] - Diccionario con los datos de la tarea.
        """
        return {
            'model_id': self.get_model_id(),
            'path': self.get_path(),
            'examples': self.get_examples()
        }
