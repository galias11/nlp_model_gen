# @Vendors
import time

# @Constants
from nlp_model_gen.constants.constants import TASK_STATUS_QUEUED, TASK_STATUS_RUNNING

# @Classes
from nlp_model_gen.utils.classUtills import Observer
from .modelCreationTask.ModelCreationTask import ModelCreationTask
from .modelTrainingTask.ModelTrainingTask import ModelTrainingTask
from .textAnalysisTask.TextAnalysisTask import TextAnalysisTask

class TaskManager(Observer):
    def __init__(self):    
        Observer.__init__(self)
        self.__active_tasks = list([])
        self.__completed_tasks = list([])
        self.__last_id = 0

    def __get_next_task_id(self):
        """
        Devuelve el proximo id disponible para colocar una tarea en cola.
        """
        next_index = self.__last_id + 1
        self.__last_id = next_index
        return next_index

    def __check_active_status_for_model(self, model_id=None, model_name=None):
        """
        Checkea si existe alguna tarea en cola (activa o no) para un determinado id de modelo
        o nombre de modelo.
        """
        for task in self.__active_tasks:
            if task.check_model_relation(model_id, model_name) and task.get_status() == TASK_STATUS_RUNNING:
                return True
        return False

    def __create_task(self, task, is_able_to_start):
        """
        Crea una tarea, la agrega al administrador y si es posible la inicializa.

        :task: [Task] - Tarea a crear.

        :is_able_to_start: [boolean] - Indica si la tarea se puede inicializar inmediatamente 
        después de creada.
        """
        self.__active_tasks.append(task)
        task.add_observer(self)
        if is_able_to_start:
            task.init()

    def __move_completed_task(self, task):
        """
        Mueve una tarea completada de la lista de activas a la lista de completadas

        :task: Tarea a mover
        """
        self.__active_tasks = list(filter(lambda active_task: active_task is not task, self.__active_tasks))
        self.__completed_tasks.append(task)

    def update(self, data):
        """
        Escucha a las tareas y realiza las actualizaciones necesarias
        """
        task = data
        self.__move_completed_task(task)
        if not self.__active_tasks:
            return
        for active_task in self.__active_tasks:
            active_task_status = active_task.get_task_status_data()
            active_task_data = active_task.get_task_data()
            model_id = active_task_data.get('model_id', None)
            model_name = active_task_data.get('model_name', None)
            if active_task_status['status'] == TASK_STATUS_QUEUED and not self.__check_active_status_for_model(model_id, model_name):
                active_task.init()
            time.sleep(5)


    def create_model_training_task(self, model_id, path, examples):
        """
        Crea y agrega a la cola una nueva tarea de entrenamiento de modelo.

        :model_id: [int] - Id del modelo a utilizar.

        :path: [String] - Ruta en disco del modelo a entrenar.

        :examples: [List] - Set de ejemplos de entrenamiento a aplicar.

        :return: [int] - Id. de la tarea creada.
        """
        pass

    def create_model_creation_task(self, model_id, model_name, description, author, tokenizer_exceptions, max_dist):
        """
        Crea y agrega a la cola una nueva tarea de creación de modelo.

        :model_id: [String] - Id del modelo a crear.

        :model_name: [String] - Nombre del modelo a crear.

        :description: [String] - Descripcion del modelo a crear.

        :author: [String] - Autor del modelo a crear.

        :tokenizer_exceptions: [Dict] - Datos de las excepciones al tokenizer a aplicar al nuevo modelo.

        :max_dist: [int] - Distancia de demerau levenshtein máxima.

        :return: [int] - Id. de la tarea creada.
        """
        next_task_id = self.__get_next_task_id()
        new_task = ModelCreationTask(next_task_id, model_id, model_name, description, author, tokenizer_exceptions, max_dist)
        is_able_to_init = not self.__check_active_status_for_model(model_id, model_name)
        self.__create_task(new_task, is_able_to_init)
        return next_task_id

    def create_text_analysis_task(self, model_id, text, only_positives):
        """
        Crea y agrega a la cola una nueva tarea de análisis de texto.

        :model_id: [int] - Id del modelo a utilizar.

        :text: [String] - Texto a analizar.

        :only_positives: [boolean] - Flag que indica si los resultados solo deben contener los positivos
        encontrados.

        :return: [int] - Id. de la tarea creada.
        """
        next_task_id = self.__get_next_task_id()
        new_task = TextAnalysisTask(next_task_id, model_id, text, only_positives)
        is_able_to_init = not self.__check_active_status_for_model(model_id)
        self.__create_task(new_task, is_able_to_init)
        return next_task_id

    def get_task_status(self, task_id):
        """
        Devuelve el status de una tarea, la misma debe existir en la cola de tareas.

        :task_id: [int] - Id de la tarea a buscar

        :return: [Dict] - Diccionario con el estado de la tarea.
        """
        try:
            founded_task = next(active_task for active_task in self.__active_tasks if active_task.get_id() == task_id)
            if founded_task is not None:
                return founded_task.get_task_status_data()
        except:
            try:
                founded_task = next(completed_task for completed_task in self.__completed_tasks if completed_task.get_id() == task_id)
                if founded_task is not None:
                    return founded_task.get_task_status_data()
            except:
                return None

    def get_active_tasks(self):
        """
        Devuelve una lista con las tareas activas del sistema.

        :return: [List] - Listado de todas las tareas activas.
        """
        return self.__active_tasks

    def get_finished_tasks(self):
        """
        Devuelve una lista con las tareas finalizadas del sistema.

        :return: [List] - Listado con las tareas finalizadas
        """
        return self.__completed_tasks
