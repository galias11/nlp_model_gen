# @Utils
from nlp_model_gen.utils.fileUtils import remove_dir

# @Logger
from nlp_model_gen.packages.logger.Logger import Logger

# @Constants
from nlp_model_gen.constants.constants import (
    TRAIN_EXAMPLE_STATUS_APPROVED,
    TRAIN_EXAMPLE_STATUS_HISTORIC,
    TRAIN_EXAMPLE_STATUS_SUBMITTED,
    WORD_PROCESSOR_MODULE_KEY_CONJUGATOR,
    WORD_PROCESSOR_MODULE_KEY_FUZZY_GEN,
    WORD_PROCESSOR_MODULE_KEY_NOUN_CONV
)

# @Classes
from nlp_model_gen.utils.classUtills import Singleton
from nlp_model_gen.packages.modelManager.ModelManagerController import ModelManagerController
from nlp_model_gen.packages.wordProcessor.WordProcessorController import WordProcessorController
from nlp_model_gen.packages.trainingModule.ModelTrainingController import ModelTrainingController
from .tokenizerRulesGenerator.TokenizerRulesGenerator import TokenizerRulesGenerator
from .analyzerRulesGenerator.AnalyzerRulesGenerator import AnalyzerRulesGerator

class AdminModuleController(metaclass=Singleton):
    def __init__(self):
        self.__analyzer_rules_generator = None
        self.__model_manager = None
        self.__tokenizer_rules_generator = None
        self.__train_manager = None
        self.__word_processor = None
        self.__init_success = False
        self.__initialize()

    def __initialize(self, is_retry=False):
        """
        Inicializa el modulo. Si la inicialización es exitosa, setea el atributo ready a True.
        En caso contrario se pasará (si no estuviese ya) a False

        :is_retry: [Bool] - Indica si es un reintento de inicialización
        """
        Logger.log('L-0036')
        self.__init_success = False
        self.__word_processor = WordProcessorController()
        if is_retry:
            self.__word_processor.retry_initialization()
        if not self.__word_processor.is_ready():
            return # Normalize when error handler is ready.
        self.__tokenizer_rules_generator = TokenizerRulesGenerator()
        self.__model_manager = ModelManagerController()
        if not self.__model_manager.is_ready():
            return # Normalize when error handler is ready.
        self.__train_manager = ModelTrainingController()
        if not self.__train_manager.is_ready():
            return # Normalize when error handler is ready.
        self.__analyzer_rules_generator = AnalyzerRulesGerator()
        self.__init_success = True
        Logger.log('L-0037')

    def retry_initialization(self):
        """
        Reintenta la reinicialización del modulo.
        """
        self.__initialize(True)

    def generate_model(self, model_id, model_name, description, author, tokenizer_exceptions, max_dist):
        """
        Crea un nuevo modelo a partir de los datos provistos. El modelo no debe existir previamente.

        :model_id: [String] - Id. del modelo.

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
        if self.__model_manager.get_model(model_id):
            Logger.log('L-0002')
            return False
        tokenizer_exceptions_path = self.__tokenizer_rules_generator.generate_model_data(tokenizer_exceptions, model_id, max_dist)
        analyzer_rule_set = self.__analyzer_rules_generator.create_analyzer_rule_set(tokenizer_exceptions)
        if not tokenizer_exceptions_path or analyzer_rule_set is None:
            return False
        model_creation_success = self.__model_manager.create_model(model_id, model_name, description, author, tokenizer_exceptions_path, analyzer_rule_set)
        Logger.log('L-0034')
        if remove_dir(tokenizer_exceptions_path, True):
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

    def load_model(self, model_id):
        """
        Carga un modelo en memoria para poder tener un acceso más rapido al mismo. Solo se aconseja su uso para
        la realización de pruebas.

        :model_id: [String] - Nombre del modelo a cargar.

        :return: [bool] - True si el modelo ha sido exitosamente cargado, False en caso contrario.
        """
        if not self.__init_success:
            Logger.log('L-0096')
            return None
        return self.__model_manager.load_model(model_id)

    def edit_model_data(self, model_id, new_model_name=None, new_description=None):
        """
        Edita los datos de un modelo existente. Si el modelo no existe u ocurre algún error durante
        la edición de sus datos devolverá false.

        :model_id: [String] - Nombre actual del modelo.

        :new_model_name: [String] - Nuevo nombre a asignar al modelo.

        :new_description: [String] - Nueva descripción para el modelo.

        :return: [bool] - True si la edición se realizó correctamente, False en caso contrario.
        """
        if not self.__init_success:
            Logger.log('L-0097')
            return None
        Logger.log('L-0074')
        current_model = self.__model_manager.get_model(model_id)
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
        return self.__model_manager.edit_model(model_id, edited_model_name, edited_description)

    def delete_model_data(self, model_id):
        """
        Elimina un modelo del sistema. Al eliminar los modelos se eliminará todo registro del mismo
        tanto en la base de datos como en la carpeta de modelos del sistema.

        :model_id: [String] - Id del modelo.

        :return: [boolean] - True si el modelo fue borrado exitosamente, False en caso contrario
        """
        if not self.__init_success:
            Logger.log('L-0097')
            return None
        return self.__model_manager.remove_model(model_id)

    def get_word_processor_available_configs(self, module_key):
        """
        Devuelve una lista con las configuraciones disponibles para el modulo solicitado del
        del word procesor.

        :module_key: [String] - Clave del modulo a consultar

        :return: [List(Dict)] - Lista con las configuraciones disponibles para el conjugador
        """
        if module_key == WORD_PROCESSOR_MODULE_KEY_CONJUGATOR:
            return self.__word_processor.get_available_conjugator_configs()
        if module_key == WORD_PROCESSOR_MODULE_KEY_FUZZY_GEN:
            return self.__word_processor.get_available_fuzzy_gen_configs()
        if module_key == WORD_PROCESSOR_MODULE_KEY_NOUN_CONV:
            return self.__word_processor.get_available_conversor_configs()
        return []

    def add_word_processor_config_theme(self, module_key, theme_name, configs, irregular_groups=None):
        """
        Agrega un nuevo tema para sub modulo solicitado del modulo de procesamiento de palabras.

        :module_key: [String] - Modulo a agregar el nuevo tema de configuración

        :theme_name: [String] - Nombre del nuevo tema a agregar.

        :configs: [Dict] - Configuraciones básicas del tema.

        :irregular_groups: [Dict] - Grupos irregulares del tema. 

        :return: [boolean] - True si la operación fue exitosa, False en caso contrario
        """
        if module_key == WORD_PROCESSOR_MODULE_KEY_CONJUGATOR:
            return self.__word_processor.add_conjugator_config(theme_name, configs, irregular_groups)
        if module_key == WORD_PROCESSOR_MODULE_KEY_FUZZY_GEN:
            return self.__word_processor.add_fuzzy_gen_config(theme_name, configs)
        if module_key == WORD_PROCESSOR_MODULE_KEY_NOUN_CONV:
            return self.__word_processor.add_noun_conversor_config((theme_name, configs))
        return False

    def add_theme_conjugator_exceptions(self, theme_name, exceptions):
        """
        Agrega un set de excepciones al conjugador de verbos de un tema determinado.

        :theme_name: [String] - Nombre del tema.

        :exceptions: [List(Dict)] - Set de excepciones a agregar.

        :return: [boolean] - True si las excepciones se agregaron exitosamente, False en caso contrario.
        """
        return self.__word_processor.add_conjugator_exceptions(theme_name, exceptions)

    def get_word_processor_active_themes(self):
        """
        Devuelve los temas de configuración activos para cada modulo del modulo de procesamiento
        de palabras.

        :return: [Dict] - Diccionario con los temas activos para cada modulo.
        """
        return {
            'conjugator': self.__word_processor.get_conjugator_active_theme(),
            'fuzzy_generator': self.__word_processor.get_fuzzy_gen_active_theme(),
            'noun_conversor': self.__word_processor.get_noun_converseor_active_theme()
        }

    def set_word_processor_active_theme(self, module_key, theme_name):
        """
        Cambia el tema a utilizar para el submodulo solicitado del modulo de procesamiento de palabras,
        el tema debe existir y no ser el actual.

        :module_key: [String] - Nombre del submodulo del modulo de procesamiento a cambiar.

        :theme_name: [String] - Nombre del tema a activar para el conjugador.

        :return: [boolean] - True si el tema se ha cambiado exitosamente, False en caso contrario.
        """
        if module_key == WORD_PROCESSOR_MODULE_KEY_CONJUGATOR:
            return self.__word_processor.set_conjugator_active_theme(theme_name)
        if module_key == WORD_PROCESSOR_MODULE_KEY_FUZZY_GEN:
            return self.__word_processor.set_fuzzy_generator_active_theme(theme_name)
        if module_key == WORD_PROCESSOR_MODULE_KEY_NOUN_CONV:
            return self.__word_processor.set_noun_conversor_active_theme(theme_name)
        return False

    def update_word_processor_config_theme(self, module_key, theme_name, config_mod, irregular_groups_mod=None):
        """
        Modifica un tema de configuración con los datos provistos. El tema debe existir y no ser el tema
        por defecto. Se modificarse el tema activo actual el comportamiento del modulo se adaptará
        inmediatamente.

        :module_key: [String] - Nombre del submodule del modulo de procesamiento a modificar.

        :theme_name: [String] - Nombre del tema a modificar.

        :config_mod: [Dict] - Opciones actualizadas de la configuración general (no es necesario incluir las
        que no tienen cambio alguno).

        :irregular_groups_mod: [Dict] - Opciones actualizadas de los grupos de verbos irregulares (no es
        necesario incluir los grupos que no tienen cambios).

        :return: [boolean] - True si la operación fue exitosa, False en caso contrario.
        """
        if module_key == WORD_PROCESSOR_MODULE_KEY_CONJUGATOR:
            return self.__word_processor.update_conjugator_configs(theme_name, config_mod, irregular_groups_mod)
        if module_key == WORD_PROCESSOR_MODULE_KEY_FUZZY_GEN:
            return self.__word_processor.update_fuzzy_gen_config(theme_name, config_mod)
        if module_key == WORD_PROCESSOR_MODULE_KEY_NOUN_CONV:
            return self.__word_processor.update_noun_conversor_config(theme_name, config_mod)
        return False

    def update_theme_conjugator_exceptions(self, theme_name, exception_key, exception_data):
        """
        Modifica una excepción irregular del conjugador para un tema particular. Tanto el tema como la excepción
        deben existir y los nuevos datos de la excepción deben ser completos.

        :theme_name: [String] - Nombre del tema.

        :exception_key: [String] - Clave de la excepción a modificar.

        :exception_data: [Dict] - Nueva configuración de la expceción irregular.

        :returns: [boolean] - True si la operación fue exitosa, False en caso contrario.
        """
        return self.__word_processor.update_conjugator_exception(theme_name, exception_key, exception_data)

    def delete_word_processor_theme(self, module_key, theme_name):
        """
        Elimina un tema de configuración para el submodulo del modulo procesamiento de palabras seleccionado.
        El tema debe existir y no puede ser el tema por defecto.

        :module_key: [String] - Clave del modulo.

        :theme_name: [String] - Nombre del tema a eliminar.

        :return: [boolean] - True si el modulo pudo ser eliminado, False en caso contrario.
        """
        if module_key == WORD_PROCESSOR_MODULE_KEY_CONJUGATOR:
            return self.__word_processor.remove_conjugator_theme(theme_name)
        if module_key == WORD_PROCESSOR_MODULE_KEY_FUZZY_GEN:
            return self.__word_processor.remove_fuzzy_gen_theme(theme_name)
        if module_key == WORD_PROCESSOR_MODULE_KEY_NOUN_CONV:
            return self.__word_processor.remove_noun_conversor_theme(theme_name)
        return False

    def submit_training_examples(self, model_id, training_examples_list):
        """
        Agrega una lista de nuevos ejemplos de entrenamiento para un modelo particular. El
        modelo debe existir y los ejemplos deben validar la schema de validación.

        :model_id: [String] - Id del modelo.

        :training_examples_list: [List(dict)] - Lista de ejemplos a agregar.

        :return: [List] - Estado particular para cada ejemplo que inidica si pudo ser agregado.
        """
        return self.__train_manager.add_training_examples(model_id, training_examples_list)

    def get_submitted_training_examples(self, model_id, status):
        """
        Obtiene un listado de los ejemplos de un modelo para un estado particular. Los estados posibles
        son: submitted, approved, historic.

        :model_id: [String] - Id del modelo.

        :status: [String] - Estado de los ejemplos.

        :return: [List(Dict)] - Listado de los ejemplos
        """
        if status == TRAIN_EXAMPLE_STATUS_APPROVED:
            return self.__train_manager.get_approved_training_examples(model_id)
        if status == TRAIN_EXAMPLE_STATUS_HISTORIC:
            return self.__train_manager.get_training_examples_history(model_id)
        if status == TRAIN_EXAMPLE_STATUS_SUBMITTED:
            return self.__train_manager.get_pending_training_examples(model_id)
        return None
    
    def approve_training_examples(self, training_examples_list):
        """
        Aprueba una lista de ejemplos de entrenamiento. La lista de ejemplo debe contener los ids de
        los mismos. Los resultados se verificarán uno por uno, por lo que la operación retornará
        los resultados de la misma a nivel ejemplo.

        :training_examples_list: [List(int)] - Lista de los ids, de los ejemplos a aprobar.

        :return: [List(Dict)] - Lista con el resultado para cada ejemplo particular.
        """
        return self.__train_manager.approve_traning_examples(training_examples_list)

    def discard_training_examples(self, training_examples_list):
        """
        Descarta una lista de ejemplos de entrenamiento. La lista debe contener los ids de los mismos.
        Los resultados se verificarán uno por uno, por lo que la operación retornará los resultados
        de la misma a nivel ejemplo.

        :training_examples_list: [List(int)] - Lista de los ids, de los ejemplos a descartar.

        :return: [List(Dict)] - Lista con el resultado para cada ejemplo particular.
        """
        return self.__train_manager.discard_training_examples(training_examples_list)

    def apply_approved_examples(self, model_id):
        """
        Aplica todos los ejemplos de entrenamiento aprobados para un modelo y realiza la rutina de 
        entrenamiento. Al finalizar la operación los ejemplos utilizados se marcarán como 
        aplicados.

        :model_id: [String] - Id del modelo.

        :return: [boolean] - True si la operación ha sido exitosa, False en caso contrario.
        """
        return self.__train_manager.apply_training_approved_examples(model_id)

    def get_available_entities(self):
        """
        Devuelve una lista con todas las entidades personalizadas registradas en el sistema.

        :return: [List(Dict)] - Listado con todas las entidades personalizadas.
        """
        available_entities_list = list([])
        available_entities = self.__train_manager.get_available_entities()
        for entity in available_entities:
            available_entities_list.append(entity.to_dict())
        return available_entities_list

    def add_custom_entity(self, name, description):
        """
        Agrega una nueva entidad personalizada. La misma no debe existir previeamente.

        :name: [String] - Nombre de la entidad personalizada, se utilizará como identificador.

        :description: [String] - Descripción de la entidad.

        :return: [boolean] - True si la operación fue exitosa, False en caso contrario.
        """
        return self.__train_manager.add_custom_entity(name, description)

    def edit_custom_entity(self, name, description):
        """
        Edita una entidad personalizada. La misma debe existir previamente.

        :name: [String] - Nombre de la entidad personalizada, debe existir.

        :description: [String] - Descripción de la entidad.

        :return: [boolean] - True si la operación fue exitosa, False en caso contrario
        """
        return self.__train_manager.edit_custom_entity(name, description)
