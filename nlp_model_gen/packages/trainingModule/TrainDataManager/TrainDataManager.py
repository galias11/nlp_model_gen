# @Constants
from nlp_model_gen.constants.constants import (
    TRAIN_DATA_EXAMPLES_COLLECTION, 
    TRAIN_EXAMPLE_STATUS_APPLIED,
    TRAIN_EXAMPLE_STATUS_APPROVED,
    TRAIN_EXAMPLE_STATUS_REJECTED,
    TRAIN_EXAMPLE_STATUS_SUBMITTED,
    TRAIN_MANAGER_DB,
    TRAIN_MANAGER_SCHEMAS
)

# @Utils
from nlp_model_gen.utils.dbUtils import db_get_items, db_insert_items, db_get_autoincremental_id, db_update_item
from nlp_model_gen.packages.trainingModule.packageUtils.validations import validate_data

# @Classes
from ..TrainExample.TrainExample import TrainExample
from ..CustomEntityTagManager.CustomEntityTagManager import CustomEntityTagManager
from ..ModelTrainData.ModelTrainData import ModelTrainData

class TrainDataManager:
    def __init__(self, available_models):
        self.__custom_entity_manager = None
        self.__models = list([])
        self.__init_success = False
        self.__init(available_models)

    def is_ready(self):
        return self.__init_success

    def __find_model(self, model_id):
        """
        Encuentra el modelo identificado con el id de modelo indicado en la lista
        de modelos del controlador.

        :model_id: [String] - Id del modelo

        :return: [ModelTrainData] - Modelo encontrado o None en su defecto.
        """
        try:
            model = next(model_data for model_data in self.__models if model_data.check_model(model_id))
            return model
        except:
            return None
    
    def __find_example(self, example_id):
        """
        Busca un ejemplo de entrenamiento con el id solicitado en los modelos activos.
        Si no lo encuentra devuelve None.

        :example_id: [Int] - Id del ejemplo.

        :return: [TrainingExample] - Ejemplo encontrado, None si no existe.
        """
        for model in self.__models:
            example = model.get_example_by_id(example_id)
            if example is not None:
                return example
        return None

    def __init(self, available_models):
        """
        Inicializa el modulo.
        """
        try:
            for model in available_models:
                model_train_data = ModelTrainData(model, [])
                self.__models.append(model_train_data)
            examples_query = {'$and': [
                {'status': {'$ne': TRAIN_EXAMPLE_STATUS_APPLIED}}, 
                {'status': {'$ne': TRAIN_EXAMPLE_STATUS_REJECTED}}
            ]}
            training_examples = db_get_items(TRAIN_MANAGER_DB, TRAIN_DATA_EXAMPLES_COLLECTION, examples_query)
            for training_example in training_examples:
                model_id = training_example['model_id']
                model_train_data = self.__find_model(model_id)
                if model_train_data is not None:
                    model_train_data.add_training_example(training_example)
            self.__custom_entity_manager = CustomEntityTagManager()
            self.__init_success = self.__custom_entity_manager.is_ready()
        except:
            self.__init_success = False

    def __validate_examples(self, examples):
        """
        Valida un ejemplo de entrenamiento.

        :example: [List] - Ejemplo de entrenamiento a validar.

        :return: [boolean] - True si el ejemplo es válido. False en caso contrario.
        """
        for example in examples:
            for tag in example['tags']:
                tag_entity = tag['entity']
                if not self.__custom_entity_manager.validate_tag(tag_entity):
                    return False
            example_data = {'sentence': example['sentence'], 'tags': example['tags'], 'type': example['type']}
            if not validate_data(TRAIN_MANAGER_SCHEMAS['TRAIN_DATA'], example_data):
                return False
        return True

    def __create_new_example_data(self, examples, model_id):
        """
        Valida y genera los datos para una nueva entrada de un objeto a partir de 
        los datos del set de ejemplos provistos.

        :examples: [List(dict)] - Set de ejemplos de entrenamiento a partir del cual 
        obtener los datos.

        :model_id: [String] - Id del mo

        :return: [List(dict)] - Datos de entrenamiento para insertar en la base de 
        datos.
        """
        if not self.__validate_examples(examples):
            raise Exception()
        examples_data = list([])
        for example in examples:
            examples_data.append({
                'example_id': db_get_autoincremental_id(TRAIN_DATA_EXAMPLES_COLLECTION),
                'model_id': model_id,
                'sentence': example['sentence'],
                'tags': example['tags'],
                'type': example['type'],
                'status': TRAIN_EXAMPLE_STATUS_SUBMITTED
            })
        return examples_data

    def retry_init(self, available_models):
        """
        Reintenta la inicialización del módulo.

        :available_models: [List(Model)] - Lista con los modelos disponibles.
        """
        self.__init(available_models)

    def insert_new_model(self, new_model):
        """
        Inserta un nuevo contenedor de ejemplos para modelo y lo agrega a la lista.

        :new_model: [Model] - Modelo a agregar.
        """
        new_model_train_data = ModelTrainData(new_model, [])
        self.__models.append(new_model_train_data)

    def add_training_examples(self, model_id, examples):
        """
        Agrega un nuevo ejemplo de entrenamiento. El ejemplo debe ser válido.

        :model_id: [String] - Id. del modelo al cual se aplicará el ejemplo 

        :examples: [List(Dict)] - Datos del ejemplo de entrenamiento.

        :return: [boolean] - True si el ejemplo es válido, False en caso contrario.
        """
        try:
            model_train_data = self.__find_model(model_id)
            if model_train_data is None:
                return False
            examples_data = self.__create_new_example_data(examples, model_id)
            db_insert_items(TRAIN_MANAGER_DB, TRAIN_DATA_EXAMPLES_COLLECTION, examples_data)
            for example in examples_data:
                model_train_data.add_training_example(example)
            return True
        except:
            return False

    def approve_example(self, example_id):
        """
        Aprueba el ejemplo de entrenamiento identificado on el id solicitado. El 
        ejemplo debe existir y no estar ya aprobado o aplicado.

        :example_id: [int] - Id del ejemplo de entrenamiento.

        :return: [boolean] - True si el ejemplo fue aprobado, False en caso contrario.
        """
        example = self.__find_example(example_id)
        if example is None:
            return False
        example_id = example.get_example_id()
        updated_items = db_update_item(TRAIN_MANAGER_DB, TRAIN_DATA_EXAMPLES_COLLECTION, {'example_id': example_id}, {'status': TRAIN_EXAMPLE_STATUS_APPROVED})
        if updated_items.matched_count > 0:
            example.approve()
            return True
        return False

    def discard_example(self, example_id):
        """
        Rechaza el ejemplo de entrenamiento. El ejemplo solicitado debe existir y no
        estar ya rechazado o aplicado.

        :example_id: [int] - Id del ejemplo de entrenamiento.

        :return: [boolean] - True si el ejemplo fue rechazado, False en caso contrario.
        """
        example = self.__find_example(example_id)
        if example is None:
            return False
        example_id = example.get_example_id()
        updated_items = db_update_item(TRAIN_MANAGER_DB, TRAIN_DATA_EXAMPLES_COLLECTION, {'example_id': example_id}, {'status': TRAIN_EXAMPLE_STATUS_REJECTED})
        if updated_items.matched_count > 0:
            example.reject()
            return True
        return False

    def get_pending_examples(self, model_id):
        """
        Retorna un listado con todos los ejemplos que tienen su aprobación / rechazo aún
        pendiente para un determinado modelo.

        :model_id: [String] - Id del modelo.

        :return: [List] - Lista de los ejemplos pendientes de una decisión.
        """
        model_train_data = self.__find_model(model_id)
        if not model_train_data:
            return None
        return model_train_data.get_pending_examples()

    def get_approved_examples(self, model_id):
        """
        Retorna un listado con todos los ejemplos aprobados para un determinado modelo.

        :model_id: [String] - Id del modelo.

        :return: [List] - Lista de los ejemplos aprobados.
        """
        model_train_data = self.__find_model(model_id)
        if not model_train_data:
            return None
        return model_train_data.get_approved_examples()

    def get_examples_history(self, model_id):
        """
        Retorna un listado con todos los ejemplos, sin importar su estado, para un determinado
        modelo.

        :model_id: [String] - Id del modelo.

        :return: [List] - Listado de todos los ejemplos para el modelo solicitado.
        """
        if not self.__find_model(model_id):
            return None
        results = list([])
        examples_data = db_get_items(TRAIN_MANAGER_DB, TRAIN_DATA_EXAMPLES_COLLECTION, {'model_id': model_id})
        for example_data in examples_data:
            example = TrainExample(example_data['example_id'], example_data['sentence'], example_data['tags'], example_data['type'], example_data['status'])
            results.append(example)
        return results

    def add_custom_entity(self, name, description):
        """
        Agrega una nueva entidad personalizada para el NER. No debe existir previamente una
        entidad ya registrada con el nombre deseado.

        :name: [String] - Nombre de la entidad.

        :description: [String] - Descripcion de la entidad.

        :return: [boolean] - True si la entidad ha sido agregada exitosamente, False en caso
        contrario.
        """
        return self.__custom_entity_manager.add_custom_entity(name, description)

    def edit_custom_entity(self, name, description):
        """
        Edita la descripcioón de una entidad personalizada para el NER. La entidad debe existir
        previamente.

        :name: [String] - Nombre de la entidad.

        :description: [String] - Nueva descripción de la entidad.

        :return: [boolean] - True si la entidad ha sido editada correctamente, False en caso
        contrario.
        """
        return self.__custom_entity_manager.edit_custom_tag_entity(name, description)

    def get_available_entities(self):
        """
        Devuelve un listado con todas las entidades personalizadas disponibles.

        :return: [List] - Listado de todas las entidades personalizadas disponibles.
        """
        return self.__custom_entity_manager.get_available_entities()
