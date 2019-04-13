# @Classes
from nlp_model_gen.packages.adminModule.AdminModuleController import AdminModuleController
from ..task.Task import Task

class ModelTrainingTask(Task):
    def __init__(self, id, model_id):
        super(ModelTrainingTask, self).__init__(id)
        self.__model_id = model_id

    def get_model_id(self):
        return self.__model_id

    def task_init_hook(self):
        """
        Método que se ejecutará en el template del init de la task de la clase padre.
        """
        admin = AdminModuleController()
        results = admin.apply_approved_examples(self.__model_id)
        if results:
            self.set_results(self.get_task_data())
        else:
            self.set_error_data('0001', 'Generic error')

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
            'model_id': self.get_model_id()
        }
