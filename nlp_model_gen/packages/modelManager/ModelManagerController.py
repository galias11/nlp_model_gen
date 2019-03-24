# @Utils
from nlp_model_gen.utils.fileUtils import get_files_in_dir, load_json_file

# @Contants
from nlp_model_gen.constants.constants import TOKEN_RULES_GEN_RULES_EXT, EVENT_MODEL_CREATED, EVENT_MODEL_DELETED

# @Log colors
from nlp_model_gen.packages.logger.assets.logColors import ERROR_COLOR

# @Classes
from nlp_model_gen.utils.classUtills import ObservableSingleton
from nlp_model_gen.packages.logger.Logger import Logger
from .modelDataManager.ModelDataManager import ModelDataManager
from .modelLoader.ModelLoader import ModelLoader
from .model.Model import Model

class ModelManagerController(ObservableSingleton):
    def __init__(self):
        ObservableSingleton.__init__(self)
        self.__models = list([])
        self.__init_success = False
        self.__initialize()

    def __initialize(self):
        """
        Inicializa el modulo.
        """
        try:
            Logger.log('L-0051')
            stored_models_data = ModelDataManager.get_models()
            for model in stored_models_data:
                model_object = Model(model['model_id'], model['model_name'], model['description'], model['author'], model['path'], model['analyzer_rules_set'])
                self.__models.append(model_object)
            Logger.log('L-0052')
            self.__init_success = True
        except Exception as e:
            Logger.log('L-0053', [{'text': e, 'color': ERROR_COLOR}])
            self.__init_success = False

    def is_ready(self):
        return self.__init_success

    def get_model(self, model_id):
        """
        Obtiene un modelo de la lista de modelos disponibles.

        :model_id: [String] - Id del modelo.

        :return: [Model] - Modelo encontrado, None si el modelo no existe
        """
        for model in self.__models:
            if model.get_model_id() == model_id:
                return model
        return None

    def __initialize_custom_model(self):
        """
        Inicializa un nuevo modelo de spacy, cargando lo en memoria.

        :return: [SpacyModelRef] - Referencia al nuevo modelo de spacy creado.
        """
        return ModelLoader.initiate_default_model()

    def load_model(self, model_id):
        """
        Carga el modelo requerido en memoria.

        :model_id: [String] - Id del modelo.

        :return: [boolean] - True si fue exitoso, false en caso contrario.
        """
        selected_model = self.get_model(model_id)
        if selected_model is None:
            return False
        selected_model.load()
        return selected_model.is_loaded()

    def get_available_models(self):
        """
        Devuelve una lista de los modelos disponibles y sus caracteristicas.

        :return: [List(Model)] - Lista de los modelos disponibles y sus caracteristicas.
        """
        return self.__models

    def get_available_models_dict(self):
        """
        Devuelve la lista de modelos disponibles y sus caracteristicas convertidos a formato dict.
        
        :return: [List(Dict)] - Lista de los modelos disponibles y sus caracteristicas.
        """
        models_list = list([])
        for model in self.__models:
            models_list.append(model.to_dict())
        return models_list

    def analyze_text(self, model_id, text='', only_positives=False):
        """
        Analiza un texto con el modelo solicitado.

        :model_id: [String] - Id del modelo a utilizar.

        :text: [String] - Texto a analizar.

        :only_positives: [boolean] - Si se activa solo se devolveran los resultados positivos del 
        análisis.

        :return: [List(Dict)] - Resultados del análisis.
        """
        Logger.log('L-0054')
        selected_model = self.get_model(model_id)
        if selected_model is None or text is None:
            Logger.log('L-0055')
            return None
        if not selected_model.is_loaded():
            selected_model.load()
        if not selected_model.is_loaded():
            Logger.log('L-0058')
            return None
        return selected_model.analyse_text(text, only_positives)    

    def train_model(self, model_id, training_data):
        """
        Aplica un set de datos de entrenamiento al modelo solicitado.

        :model_id: [String] - Nombre del modelo a entrenar.

        :training_data: [List(Dict)] - Set de datos de entrenamiento.

        :return: [boolean] - True si el proceso ha sido exitoso, False en caso contrario.
        """
        pass

    def __apply_tokenizer_exceptions(self, model, tokenizer_exceptions_path):
        """
        Aplica todas las excepciones contenidas en el directorio de excepciones al modelo.

        :model: [SpacyModelRef] - Modelo sobre el cual aplicar las excepc¡ones.

        :tokenizer_exceptions_path: [String] - Ruta al directorio de excepciones para el modelo.

        :return: [bool] - True si la operación fue exitosa, False en caso contrario.
        """
        Logger.log('L-0023')
        tokenizer_exceptions_files = get_files_in_dir(tokenizer_exceptions_path, TOKEN_RULES_GEN_RULES_EXT)
        for source_file in tokenizer_exceptions_files:
            rule_set = load_json_file(source_file)
            for key in rule_set:
                model.add_tokenizer_rule_set(rule_set[key])
        Logger.log('L-0024')

    def create_model(self, model_id, model_name, description, author, tokenizer_exceptions_path, analyzer_rule_set):
        """
        Crea un nuevo modelo. Crea los datos necesarios y lo guarda tanto en disco como su
        referencia en la base de datos.

        :model_id: [String] - Identificador del modelo (se usará también como path para buscar el modelo)

        :model_name: [String] - Nombre del modelo.

        :description: [String] - Descripción.

        :author: [String] - Referencia del autor del modelo.

        :tokenizer_exceptions_path: [List(Dict)] - Lista de excepciones del modulo tokenizer del modelo.

        :analyzer_rule_set: [List(Dict)] - Lista de reglas para el analizador.

        :return: [boolean] - True si el proceso ha sido exitoso, False en caso contrario.
        """
        if self.get_model(model_id) is not None:
            Logger.log('L-0019')
            return False
        try:
            Logger.log('L-0021')
            custom_model = self.__initialize_custom_model()
            new_model = Model(model_id, model_name, description, author, model_id, analyzer_rule_set)
            new_model.set_reference(custom_model)
            Logger.log('L-0022')
            self.__apply_tokenizer_exceptions(new_model, tokenizer_exceptions_path)
            ModelDataManager.save_model_data(model_id, model_name, description, author, model_id, analyzer_rule_set)
            ModelLoader.save_model(custom_model, model_id, tokenizer_exceptions_path)
            self.__models.append(new_model)
            Logger.log('L-0025')
            self.notify({'event': EVENT_MODEL_CREATED, 'payload': new_model})
            return True
        except Exception as e:
            Logger.log('L-0020', [{'text': e, 'color': ERROR_COLOR}])
            return False

    def edit_model(self, model_id, model_name, description):
        """
        Permite editar la descripción de un modelo. El modelo debe existir.

        :model_id: [String] - Id del modelo.

        :model_name: [String] - Nuevo nombre para el modelo.

        :description: [String] - Nueva descripción para el modelo.

        :return: [boolean] - True si la modificación se ha realizado correctamente, False en caso contrario.
        """
        selected_model = self.get_model(model_id)
        if selected_model is None:
            Logger.log('L-0077')
            return False
        if not ModelDataManager.modify_model_data(model_id, model_name, description):
            Logger.log('L-0078')
            return False
        selected_model.set_model_name(model_name)
        selected_model.set_description(description)
        Logger.log('L-0082')
        return True

    def remove_model(self, model_id):
        """
        Elimina un modelo del sistema. Borra los datos del mismo de la base de datos y elimina los archivos
        del mismo del disco.

        :model_id: [String] - Id del modelo.

        :return: [boolean] - True si el modelo fue exitosamente borrado, False en caso contrario.
        """
        Logger.log('L-0064')
        selected_model = self.get_model(model_id)
        if selected_model is None:
            Logger.log('L-0065')
            return False
        if not ModelDataManager.remove_model_data(selected_model.get_model_id()):
            Logger.log('L-0068')
            return False
        Logger.log('L-0069')
        if not ModelLoader.delete_model_files(selected_model.get_path()):
            Logger.log('L-0071')
            return False
        Logger.log('L-0072')
        self.__models.remove(selected_model)
        self.notify({'event': EVENT_MODEL_DELETED, 'payload': model_id})
        Logger.log('L-0073')
        return True
