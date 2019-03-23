# @Constants
from nlp_model_gen.constants.constants import TRAIN_MANAGER_SCHEMAS

# @Classes
from nlp_model_gen.utils.classUtills import Singleton
from nlp_model_gen.packages.modelManager.ModelManagerController import ModelManagerController
from .ModelTrainerManager.ModelTrainerManager import ModelTrainerManager
from .TrainDataManager.TrainDataManager import TrainDataManager

# @Utils
from .packageUtils.validations import validate_data

class ModelTrainingController(metaclass=Singleton):
    def __init__(self):
        self.__model_manager = None
        self.__model_trainer = None
        self.__train_data_manager = None
        self.__init_success = False
        self.__init()

    def is_ready(self):
        return self.__init_success

    def __init(self):
        """
        Inicializa el módulo.
        """
        self.__model_trainer = ModelTrainerManager()
        self.__model_manager = ModelManagerController()
        if not self.__model_manager.is_ready():
            self.__init_success = False
            return
        available_models = self.__model_manager.get_available_models()
        self.__train_data_manager = TrainDataManager(available_models)
        self.__init_success = self.__train_data_manager.is_ready() and self.__model_manager.is_ready()

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
        results = list([])
        pending_examples = self.__train_data_manager.get_pending_examples(model_id)
        if pending_examples is None:
            return None
        for pending_example in pending_examples:
            results.append(pending_example.to_dict())
        return results

    def get_approved_training_examples(self, model_id):
        """
        Obtiene un listado de los ejemplos de entrenamiento aprobados par un determinado modelo.

        :model_id: [String] - Id del modelo.

        :return: [List (Dict)] - Listados con todos los ejemplos de entrenamiento aprobados para 
        el modelo solicitado.
        """
        results = list([])
        pending_examples = self.__train_data_manager.get_approved_examples(model_id)
        if pending_examples is None:
            return None
        for pending_example in pending_examples:
            results.append(pending_example.to_dict())
        return results

    def get_training_examples_history(self, model_id):
        """
        Obtiene el historial completo de todos los ejemplos de entrenamiento para un determinado
        modelo sin importar el estado de dichos ejemplos.

        :model_id: [String] - Id del modelo.

        :return: [List(Dict)] - Listado con todos los ejemplos de entrenamiento, cuaquiera sea
        su estado, para el modelo solicitado.
        """
        results = list([])
        pending_examples = self.__train_data_manager.get_examples_history(model_id)
        if pending_examples is None:
            return None
        for pending_example in pending_examples:
            results.append(pending_example.to_dict())
        return results

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

    def add_training_examples(self, model_id, examples_list):
        """
        Agrega una lista de ejemplos de entrenamiento. Para que la operación sea exitosa todos los
        ejemplos deben poder ser validados correctamente, en caso contrario no se añadirá ninguno.

        :model_id: [String] - Id del modelo al cual se aplicará el ejemplo.

        :examples_list: [List(Dict)] - Listado de ejemplos de entrenamiento.

        :return: [boolean] - True si el listado pudo ser agregado exitosamente, False en caso
        contrario.
        """
        if not self.is_ready():
            return False
        model = self.__model_manager.get_model(model_id)
        if model is None:
            return False
        return self.__train_data_manager.add_training_examples(model_id, examples_list)

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
        if not self.is_ready():
            return False
        if not validate_data(TRAIN_MANAGER_SCHEMAS['CUSTOM_ENTITY'], {'name': name, 'description': description}):
            return False
        if not name:
            return False
        return self.__train_data_manager.add_custom_entity(name.upper(), description)

    def edit_custom_entity(self, name, description):
        """
        Edita la descripción de una entidad personalizada. La misma debe existir de lo contrario 
        fallará la operación. 

        :name: [String] - Nombre de la entidad a modificar.

        :description: [String] - Descripción de la entidad.
        """
        if not self.is_ready():
            return False
        if not validate_data(TRAIN_MANAGER_SCHEMAS['CUSTOM_ENTITY'], {'name': name, 'description': description}):
            return False
        if not name:
            return False
        return self.__train_data_manager.edit_custom_entity(name.upper(), description)

    def get_available_entities(self):
        """
        Devuelve un listado con todas las entidades personalizadas disponibles.

        :return: [List(Dict)] - Listado con todas las entidades personalizadas disponibles.
        """
        if not self.is_ready():
            return None
        return self.__train_data_manager.get_available_entities()
