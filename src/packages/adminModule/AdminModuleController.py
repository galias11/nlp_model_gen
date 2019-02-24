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
        return model_creation_success
