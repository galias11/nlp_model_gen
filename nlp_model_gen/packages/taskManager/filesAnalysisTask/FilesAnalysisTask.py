# @Vendors
import time

# @Constants
from nlp_model_gen.constants.constants import (
    TASK_KEYS_MODEL_UPDATE,
    TASK_KEYS_WORD_PROCESSOR
)

# @Classes
from nlp_model_gen.utils.classUtills import Observer
from nlp_model_gen.packages.adminModule.AdminModuleController import AdminModuleController
from ..task.Task import Task
from ..textAnalysisTask.TextAnalysisTask import TextAnalysisTask

class FilesAnalysisTask(Task, Observer):
    def __init__(self, id, model_id, files, only_positives):
        super(FilesAnalysisTask, self).__init__(id, {TASK_KEYS_MODEL_UPDATE: False, TASK_KEYS_WORD_PROCESSOR: True})
        Observer.__init__(self)
        self.__model_id = model_id
        self.__files = files
        self.__only_positives = only_positives
        self.__analysis_tasks = list([])
        self.__completed_tasks = 0

    def get_model_id(self):
        return self.__model_id

    def get_files(self):
        files_data = list([])
        for file in self.__files:
            files_data.append(file.name)
        return files_data

    def is_only_positives(self):
        return self.__only_positives

    def __check_task_finalized(self):
        return len(self.__analysis_tasks) == self.__completed_tasks

    def __build_results(self):
        results = list([])
        for task in self.__analysis_tasks:
            task_status = {'file': task['file'], 'status': task['task'].get_results()}
            results.append(task_status)
        return results

    def update(self, data):
        """
        Escucha cada una de las subtareas de analysis para controlar la finalización de
        las mismas.
        """
        self.__completed_tasks = self.__completed_tasks + 1

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
        adminModule = AdminModuleController()
        model_loaded = adminModule.load_model(self.__model_id)
        if not model_loaded:
            self.set_error_data('0001', 'Generic error')
            return
        try:
            for file in self.__files:
                file_text = file.read()
                analysis_task = TextAnalysisTask(-1, self.__model_id, file_text, self.__only_positives)
                analysis_task.add_observer(self)
                self.__analysis_tasks.append({'file': file.name, 'task': analysis_task})
                analysis_task.init()
        except Exception as e:
            print(e)
            self.set_error_data('0001', 'Generic error')
            return
        while not self.__check_task_finalized():
            time.sleep(5)
        self.set_results(self.__build_results())

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
    