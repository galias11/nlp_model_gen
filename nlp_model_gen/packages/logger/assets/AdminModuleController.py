# @Utils
from src.utils.fileUtils import remove_dir

# @Classes
from src.packages.modelManager.ModelManagerController import ModelManagerController
from src.packages.wordProcessor.WordProcessorController import WordProcessorController
from .tokenizerRulesGenerator.TokenizerRulesGenerator import TokenizerRulesGenerator
from .analyzerRulesGenerator.AnalyzerRulesGenerator import AnalyzerRulesGerator

# @Logger
from src.packages.logger.Logger import Logger

class AdminModuleController:
    __analyzer_rules_generator = None
    __model_manager = None
    __tokenizer_rules_generator = None
    __word_processor = None
    __init_success = False

    def __init__(self):
        self.__initialize()

    def __initialize(self):
        """
        Inicializa el modulo. Si la inicialización es exitosa, setea el atributo ready a True.
        En caso contrario se pasará (si no estuviese ya) a False
        """
        Logger.log('L-0036')
        self.__init_success = False
        self.__word_processor = WordProcessorController()
        if not self.__word_processor.is_ready():
            return # TODO: Normalize when error handler is ready.
        self.__tokenizer_rules_generator = TokenizerRulesGenerator()
        self.__model_manager = ModelManagerController()
        if not self.__model_manager.is_ready():
            return # TODO: Normalize when error handler is ready.
        self.__analyzer_rules_generator = AnalyzerRulesGerator()
        self.__init_success = True
        Logger.log('L-0037')

    def retry_initialization(self):
        """
        Reintenta la reinicialización del modulo.
        """
        self.__initialize()

    def generate_model(self, model_name, description, author, tokenizer_exceptions, max_dist):
        """
        Crea un nuevo modelo a partir de los datos provistos. El modelo no debe existir previamente.

        :model_name: [String] - Nombre del modelo (actua como Id).

        :model_path: [String] - Directorio base para el modelo.

        :descripcion: [String] - Descripcion del modelo.

        :author: [String] - Nombre del autor del modelo.

        :tokenizer_exceptions: [Dict] - Conjunto de excepciones a agregar al tokenizer del nuevo modelo.
        """
        if not self.__init_success:
            Logger.log('L-0094')
            return None
        Logger.log('L-0001')
        if self.__model_manager.get_model(model_name):
            Logger.log('L-0002')
            return False
        tokenizer_exceptions_path = self.__tokenizer_rules_generator.generate_model_data(tokenizer_exceptions, model_name, max_dist)
        analyzer_rule_set = self.__analyzer_rules_generator.create_analyzer_rule_set(tokenizer_exceptions)
        if not tokenizer_exceptions_path or analyzer_rule_set is None:
            return False
        model_creation_success = self.__model_manager.create_model(model_name, description, author, tokenizer_exceptions_path, analyzer_rule_set)
        Logger.log('L-0034')
        if remove_dir(tokenizer_exceptions_path):
            Logger.log('L-0035')
        return model_creation_success

    def get_available_models(self):
        """
        Devuelve una lista con todos los modelos disponibles en el sistema (esten cargados o no).

        :return: [List] - Listado de los modelos disponibles en el sistema.
        """
        if not self.__init_success:
            Logger.log('L-0095')
            return None
        return self.__model_manager.get_available_models_dict()

    def load_model(self, model_name):
        """
        Carga un modelo en memoria para poder tener un acceso más rapido al mismo. Solo se aconseja su uso para
        la realización de pruebas.

        :model_name: [String] - Nombre del modelo a cargar.

        :return: [bool] - True si el modelo ha sido exitosamente cargado, False en caso contrario.
        """
        if not self.__init_success:
            Logger.log('L-0096')
            return None
        return self.__model_manager.load_model(model_name)

    def edit_model_data(self, model_name, new_model_name=None, new_description=None):
        """
        Edita los datos de un modelo existente. Si el modelo no existe u ocurre algún error durante
        la edición de sus datos devolverá false.

        :model_name: [String] - Nombre actual del modelo.

        :new_model_name: [String] - Nuevo nombre a asignar al modelo.

        :new_description: [String] - Nueva descripción para el modelo.

        :return: [bool] - True si la edición se realizó correctamente, False en caso contrario.
        """
        if not self.__init_success:
            Logger.log('L-0097')
            return None
        Logger.log('L-0074')
        current_model = self.__model_manager.get_model(model_name)
        if current_model is None:
            Logger.log('L-0075')
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
            Logger.log('L-0076')
            return False
        return self.__model_manager.edit_model(model_name, edited_model_name, edited_description)

    def delete_model_data(self, model_name):
        """
        Elimina un modelo del sistema. Al eliminar los modelos se eliminará todo registro del mismo
        tanto en la base de datos como en la carpeta de modelos del sistema.
        """
        return self.__model_manager.remove_model(model_name)

    def analyse_text(self, model_name, text, only_positives=False):
        """
        Analiza un texto aplicandole el modelo solicitado. El modelo debe existir.

        :model_name: [String] - Nombre del modelo a utilizar.

        :text: [String] - Texto a analizar.

        :only_positives: [boolean] - Si esta activado, devuelve solo los resultados positivos.

        :return: [List(Dict)] - Resultados del analisis, None si ha ocurrido un error.
        """
        return self.__model_manager.analyze_text(model_name, text, only_positives)
