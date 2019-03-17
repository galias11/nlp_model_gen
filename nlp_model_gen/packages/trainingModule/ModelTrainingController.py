# @Classes
from nlp_model_gen.utils.classUtills import Singleton
from nlp_model_gen.packages.modelManager.ModelManagerController import ModelManagerController
from .ModelTrainerManager.ModelTrainerManager import ModelTrainerManager
from .TrainDataManager.TrainDataManager import TrainDataManager

class ModelTrainingController(metaclass=Singleton):
    def __init__(self):
        self.__model_manager = ModelManagerController()
        self.__model_trainer = ModelTrainerManager()
        self.__train_data_manager = TrainDataManager()
        self.__init_success = False
        self.__init()

    def __init(self):
        """
        Inicializa el módulo.
        """
        pass

    def retry_init(self):
        """
        Reintenta la inicialización del módulo
        """
        self.__init()

    def add_model(self, model_id):
        """
        Agrega un modelo (aplicable en los casos que se añade un nuevo modelo al sistema).

        :model_id: [String] - Id del modelo.

        :return: [boolean] - True si se ha agregado exitosamente, False en caso contrario.
        """
        pass

    def get_pending_training_examples(self, model_id):
        """
        Obtiene un listado de los ejemplos de entrenamiento pendientes para un determinado modelo.

        :model_id: [String] - Id del modelo.

        :return: [List(Dict)] - Listado con los ejemplos de entrenamiento con una decisión
        pendiente para el modelo solicitado.
        """
        pass

    def apply_training_approved_examples(self, model_id):
        """
        Aplica el conjunto de ejemplos de entrenamiento aprobados para un determinado modelo. Es
        necesario que exista un número mínimo de modelos de entrenamiento aprobados para inicializar
        el proceso de entrenamiento.

        :model_id: [String] - Id del modelo.

        :return: [boolean] -  True si el entrenamiento se ha realizado exitosamente, False en 
        caso contrario.
        """
        pass

    def discard_training_examples(self, examples_id_list):
        """
        Rechaza el conjunto de ejemplos de entrenamiento que tienen los ids especificados en la lista
        de ids provista. Todos los ids provistos deben existir, de lo contrario, no se descartará
        ninguno.

        :examples_id_list: [List(int)] - Listado con los ids de los ejemplos a rechazar.

        :return: [boolean] - True si el listado pudo ser rechazado exitosamente, False en caso 
        contrario.
        """
        pass

    def add_training_examples(self, examples_list):
        """
        Agrega una lista de ejemplos de entrenamiento. Para que la operación sea exitosa todos los
        ejemplos deben poder ser validados correctamente, en caso contrario no se añadirá ninguno.

        :examples_list: [List(Dict)] - Listado de ejemplos de entrenamiento.

        :return: [boolean] - True si el listado pudo ser agregado exitosamente, False en caso
        contrario.
        """
        pass

    def approve_traning_examples(self, examples_id_list):
        """
        Aprueba un conjunto de ejemplos de entrenamiento cuyos ids se encuentran en la lista de 
        ids provista. Si alguno de los ids en la lista no existe la operación no se realizará para
        ningún ejemplo.

        :examples_id_list: [List(int)] - Lista con los ids de los ejemplos de entrenamiento a aprobar.

        :return: [boolean] - True si los ejempos se han aprobado correctamente, False en caso
        contrario.
        """
        pass

    def add_custom_entity(self, name, description):
        """
        Agrega una nueva entidad personalizada. No debe existir previamente una entidad con el mismo
        nombre.

        :name: [String] - Nombre de la entidad, actuará como identificador de la misma.

        :description: [String] - Descripción de la entidad.

        :return: [boolean] - True si se ha agregado correctamente, False en caso contrario.
        """
        pass

    def edit_custom_entity(self, name, description):
        """
        Edita la descripción de una entidad personalizada. La misma debe existir de lo contrario 
        fallará la operación. 

        :name: [String] - Nombre de la entidad a modificar.

        :description: [String] - Descripción de la entidad.
        """
        pass

    def get_available_entities(self):
        """
        Devuelve un listado con todas las entidades personalizadas disponibles.

        :return: [List(Dict)] - Listado con todas las entidades personalizadas disponibles.
        """
        pass
