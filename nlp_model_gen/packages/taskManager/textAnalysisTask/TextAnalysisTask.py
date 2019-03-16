# @Classes
from nlp_model_gen.packages.adminModule.AdminModuleController import AdminModuleController
from ..task.Task import Task

class TextAnalysisTask(Task):
    def __init__(self, id, model_id, text, only_positives):
        super(TextAnalysisTask, self).__init__(id)
        self.__model_id = model_id
        self.__text = text
        self.__only_positives = only_positives

    def get_model_id(self):
        return self.__model_id

    def get_text(self):
        return self.__text

    def is_only_positives(self):
        return self.__only_positives

    def check_model_relation(self, model_id, model_name):
        """
        Determina si una tarea esta relacionada con un determinado modelo utilizando su
        id y su nombre

        :model_id: [String] - Id del modelo

        :model_name: [String] - Nombre del modelo

        :return: [boolean] - True si el modelo esta releacionado, False en caso contrario.
        """
        return model_id == self.__model_id

    def task_init_hook(self):
        """
        Método hook para completar el template de inicializadion en el padre.
        """
        admin = AdminModuleController()
        results = admin.analyse_text(self.__model_id, self.__text, self.__only_positives)
        if results is not None:
            self.set_results(results)
        else:
            self.set_error_data('0001', 'Generic error')

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
    