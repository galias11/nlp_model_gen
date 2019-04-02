# @Constants
from nlp_model_gen.constants.constants import EVENT_MODEL_CREATED, EVENT_MODEL_DELETED, TRAIN_MANAGER_SCHEMAS

# @Logger
from nlp_model_gen.packages.logger.Logger import Logger
from nlp_model_gen.packages.logger.assets.logColors import HIGHLIGHT_COLOR

# @Classes
from nlp_model_gen.utils.classUtills import ObserverSingleton
from nlp_model_gen.packages.modelManager.ModelManagerController import ModelManagerController
from .ModelTrainerManager.ModelTrainerManager import ModelTrainerManager
from .TrainDataManager.TrainDataManager import TrainDataManager

# @Utils
from .packageUtils.validations import validate_data

class ModelTrainingController(ObserverSingleton):
    def __init__(self):
        ObserverSingleton.__init__(self)
        self.__model_manager = None
        self.__model_trainer = None
        self.__train_data_manager = None
        self.__init_success = False
        self.__init()

    def is_ready(self):
        return self.__init_success

    def update(self, data):
        if data['event'] == EVENT_MODEL_CREATED:
            self.__add_model(data['payload'])
            return
        if data['event'] == EVENT_MODEL_DELETED:
            self.__remove_model(data['payload'])
            return

    def __init(self):
        """
        Inicializa el módulo.
        """
        Logger.log('L-0243')
        self.__model_trainer = ModelTrainerManager()
        self.__model_manager = ModelManagerController()
        self.__model_manager.add_observer(self)
        if not self.__model_manager.is_ready():
            Logger.log('L-0244')
            self.__init_success = False
            return
        available_models = self.__model_manager.get_available_models()
        self.__train_data_manager = TrainDataManager(available_models)
        if self.__train_data_manager.is_ready() and self.__model_manager.is_ready():
            Logger.log('L-0245')
            self.__init_success = True
            return
        Logger.log('L-0246')

    def __add_model(self, model):
        """
        Agrega un modelo (aplicable en los casos que se añade un nuevo modelo al sistema).

        :model: [Model] - Modelo a agregar.
        """
        self.__train_data_manager.insert_new_model(model)

    def __remove_model(self, model_id):
        """
        Elimina un modelo del TrainDataManager cuando este es eliminado desde el modulo de
        administración de modelos.

        :model_id: [String] - Id del modelo a eliminar.
        """
        self.__train_data_manager.remove_model(model_id)

    def retry_init(self):
        """
        Reintenta la inicialización del módulo
        """
        self.__init()

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
        Logger.log('L-0323')
        results = list([])
        pending_examples = self.__train_data_manager.get_examples_history(model_id)
        if pending_examples is None:
            return None
        for pending_example in pending_examples:
            results.append(pending_example.to_dict())
        Logger.log('L-0324')
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
        Logger.log('L-0331')
        model = self.__model_manager.get_model(model_id)
        if model is None:
            Logger.log('L-0332')
            return False
        approved_examples_list = self.__train_data_manager.get_approved_examples(model_id)
        if approved_examples_list is None or not approved_examples_list:
            Logger.log('L-0333')
            return False
        if self.__model_trainer.train_model(model, approved_examples_list):
            Logger.log('L-0334')
            self.__train_data_manager.set_applied_state(approved_examples_list)
            Logger.log('L-0335')
            Logger.log('L-0336')
            return True
        Logger.log('L-0337')
        return False

    def discard_training_examples(self, examples_id_list):
        """
        Rechaza el conjunto de ejemplos de entrenamiento que tienen los ids especificados en la lista
        de ids provista. Todos los ids provistos deben existir, de lo contrario, no se descartará
        ninguno.

        :examples_id_list: [List(int)] - Listado con los ids de los ejemplos a rechazar.

        :return: [List(dict)] - Listado indicando los ejemplos de entrenamiento que se han podido
        rechazar y los que no.
        """
        Logger.log('L-0314')
        results = list([])
        for example_id in examples_id_list:
            results.append({'example_id': example_id, 'status': self.__train_data_manager.discard_example(example_id)})
        Logger.log('L-0315')
        return results

    def add_training_examples(self, model_id, examples_list):
        """
        Agrega una lista de ejemplos de entrenamiento. Para que la operación sea exitosa todos los
        ejemplos deben poder ser validados correctamente, en caso contrario no se añadirá ninguno.

        :model_id: [String] - Id del modelo al cual se aplicará el ejemplo.

        :examples_list: [List(Dict)] - Listado de ejemplos de entrenamiento.

        :return: [boolean] - True si el listado pudo ser agregado exitosamente, False en caso
        contrario.
        """
        Logger.log('L-0292')
        if not self.is_ready():
            Logger.log('L-0293')
            return False
        model = self.__model_manager.get_model(model_id)
        if model is None:
            Logger.log('L-0294')
            return False
        if self.__train_data_manager.add_training_examples(model_id, examples_list):
            Logger.log('L-0295')
            return True
        Logger.log('L-0296')
        return False

    def approve_traning_examples(self, examples_id_list):
        """
        Aprueba un conjunto de ejemplos de entrenamiento cuyos ids se encuentran en la lista de 
        ids provista. Si alguno de los ids en la lista no existe la operación no se realizará para
        ningún ejemplo.

        :examples_id_list: [List(int)] - Lista con los ids de los ejemplos de entrenamiento a aprobar.

        :return: [List(dict)] - Listado indicando los ejemplos de entrenamiento que se han podido
        aceptar y los que no.
        """
        Logger.log('L-0305')
        results = list([])
        for example_id in examples_id_list:
            results.append({'example_id': example_id, 'status': self.__train_data_manager.approve_example(example_id)})
        Logger.log('L-0306')
        return results

    def add_custom_entity(self, name, description):
        """
        Agrega una nueva entidad personalizada. No debe existir previamente una entidad con el mismo
        nombre.

        :name: [String] - Nombre de la entidad, actuará como identificador de la misma.

        :description: [String] - Descripción de la entidad.

        :return: [boolean] - True si se ha agregado correctamente, False en caso contrario.
        """
        Logger.log('L-0264')
        if not self.is_ready():
            Logger.log('L-0265')
            return False
        Logger.log('L-0266')
        if not validate_data(TRAIN_MANAGER_SCHEMAS['CUSTOM_ENTITY'], {'name': name, 'description': description}):
            Logger.log('L-0267')
            return False
        Logger.log('L-0268')
        if self.__train_data_manager.add_custom_entity(name.upper(), description):
            Logger.log('L-0269')
            return True
        Logger.log('L-0270')
        return False

    def edit_custom_entity(self, name, description):
        """
        Edita la descripción de una entidad personalizada. La misma debe existir de lo contrario 
        fallará la operación.

        :name: [String] - Nombre de la entidad a modificar.

        :description: [String] - Descripción de la entidad.
        """
        Logger.log('L-0277', [{'text': name, 'color': HIGHLIGHT_COLOR}])
        if not self.is_ready():
            Logger.log('L-0278')
            return False
        Logger.log('L-0279')
        if not validate_data(TRAIN_MANAGER_SCHEMAS['CUSTOM_ENTITY'], {'name': name, 'description': description}):
            Logger.log('L-0280')
            return False
        Logger.log('L-0281')
        if self.__train_data_manager.edit_custom_entity(name.upper(), description):
            Logger.log('L-0282')
            return True
        Logger.log('L-0283')
        return False

    def get_available_entities(self):
        """
        Devuelve un listado con todas las entidades personalizadas disponibles.

        :return: [List(Dict)] - Listado con todas las entidades personalizadas disponibles.
        """
        if not self.is_ready():
            return None
        return self.__train_data_manager.get_available_entities()
