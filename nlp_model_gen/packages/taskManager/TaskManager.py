# @Classes
from .modelCreationTask.ModelCreationTask import ModelCreationTask
from .modelTrainingTask.ModelTrainingTask import ModelTrainingTask
from .textAnalysisTask.TextAnalysisTask import TextAnalysisTask

class TaskManager:
    tasks_queue = list([])

    def __init__(self):
        pass

    def __check_active_status_for_model(self, model_id=None, model_name=None):
        """
        Checkea si existe alguna tarea en cola (activa o no) para un determinado id de modelo
        o nombre de modelo.
        """
        pass

    def create_model_training_task(self, model_id, path, examples):
        """
        Crea y agrega a la cola una nueva tarea de entrenamiento de modelo.

        :model_id: [int] - Id del modelo a utilizar.

        :path: [String] - Ruta en disco del modelo a entrenar.

        :examples: [List] - Set de ejemplos de entrenamiento a aplicar.

        :return: [int] - Id. de la tarea creada.
        """
        pass

    def create_model_creation_task(self, model_name, description, author, tokenizer_exceptions):
        """
        Crea y agrega a la cola una nueva tarea de creación de modelo.

        :model_name: [String] - Nombre del modelo a crear.

        :description: [String] - Descripcion del modelo a crear.

        :author: [String] - Autor del modelo a crear.

        :tokenizer_exceptions: [Dict] - Datos de las excepciones al tokenizer a aplicar al nuevo modelo.

        :return: [int] - Id. de la tarea creada.
        """
        pass

    def create_text_analysis_task(self, model_id, text, only_positives):
        """
        Crea y agrega a la cola una nueva tarea de análisis de texto.

        :model_id: [int] - Id del modelo a utilizar.

        :text: [String] - Texto a analizar.

        :only_positives: [boolean] - Flag que indica si los resultados solo deben contener los positivos
        encontrados.

        :return: [int] - Id. de la tarea creada.
        """
        pass

    def init_task(self, task_id):
        """
        Inicia una de las tareas en cola.

        :task_id: [int] - Id de la tarea a iniciar.

        :return: [boolean] - True si la tarea inició correctamente, False en caso contrario
        """
        pass

    def get_task_status(self, task_id):
        """
        Devuelve el status de una tarea, la misma debe existir en la cola de tareas.

        :task_id: [int] - Id de la tarea a buscar

        :return: [Dict] - Diccionario con el estado de la tarea.
        """
        pass

    def get_active_tasks(self):
        """
        Devuelve una lista con las tareas activas del sistema.

        :return: [List] - Listado de todas las tareas activas.
        """
        pass
