# @Utils
from src.utils.fileUtils import remove_dir

# @Classes
from src.packages.modelManager.ModelManagerController import ModelManagerController
from src.packages.wordProcessor.WordProcessorController import WordProcessorController
from .tokenizerRulesGenerator.TokenizerRulesGenerator import TokenizerRulesGenerator

class AdminModuleController:
    __word_processor = None
    __tokenizer_rules_generator = None

    def __init__(self):
        self.__word_processor = WordProcessorController()
        self.__tokenizer_rules_generator = TokenizerRulesGenerator()
        self.__model_manager = ModelManagerController()

    def generate_model(self, model_name, description, author, tokenizer_exceptions, max_dist):
        """
        Crea un nuevo modelo a partir de los datos provistos. El modelo no debe existir previamente.

        :model_name: [String] - Nombre del modelo (actua como Id).

        :model_path: [String] - Directorio base para el modelo.

        :descripcion: [String] - Descripcion del modelo.

        :author: [String] - Nombre del autor del modelo.

        :tokenizer_exceptions: [Dict] - Conjunto de excepciones a agregar al tokenizer del nuevo modelo.
        """
        if self.__model_manager.get_model(model_name):
            return False
        tokenizer_exceptions_path = self.__tokenizer_rules_generator.generate_model_data(tokenizer_exceptions, model_name, max_dist)
        if not tokenizer_exceptions_path:
            return False
        model_creation_success = self.__model_manager.create_model(model_name, description, author, tokenizer_exceptions_path)
        remove_dir(tokenizer_exceptions_path)
        return model_creation_success

    def get_available_models(self):
        """
        Devuelve una lista con todos los modelos disponibles en el sistema (esten cargados o no).

        :return: [List] - Listado de los modelos disponibles en el sistema.
        """
        return self.__model_manager.get_available_models_dict()

    def edit_model_data(self, model_name, new_model_name=None, new_description=None):
        """
        Edita los datos de un modelo existente. Si el modelo no existe u ocurre algún error durante
        la edición de sus datos devolverá false.

        :model_name: [String] - Nombre actual del modelo.

        :new_model_name: [String] - Nuevo nombre a asignar al modelo.

        :new_description: [String] - Nueva descripción para el modelo.

        :return: [bool] - True si la edición se realizó correctamente, False en caso contrario.
        """
        current_model = self.__model_manager.get_model(model_name)
        if current_model is None:
            return False
        current_model_name = current_model.get_model_name()
        edited_model_name = new_model_name
        current_description = current_model.get_description()
        edited_description = new_description
        if new_model_name is None or new_model_name == '':
            edited_model_name = current_model_name
        if new_description is None or new_description == '':
            edited_description = current_description
        if edited_model_name == current_model_name and edited_description == current_description:
            return False
        return self.__model_manager.edit_model(model_name, edited_model_name, edited_description)
