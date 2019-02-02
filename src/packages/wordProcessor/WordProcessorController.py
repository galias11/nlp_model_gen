# @Vendors
import copy

# @Utils
from src.utils.fileUtils import load_dict_from_json
from src.utils.dbUtils import (
    db_check_collection, 
    db_insert_item, 
    db_insert_items, 
    db_get_items, 
    db_get_item, 
    db_drop_collection,
    db_batch_operation
)
from .packageUtils.validations import validate_config

# @Contants
from src.constants.constants import (
    DB_OPERATION_DELETE,
    DB_OPERATION_INSERT,
    DB_OPERATION_INSERT_MANY,
    DB_OPERATION_UPDATE,
    WORD_PROCESSOR_CONFIG_DB,
    WORD_PROCESSOR_CONJ_CFG_COLLECTION,
    WORD_PROCESSOR_DEFAULT_CFG_OBJECT,
    WORD_PROCESSOR_DEFAULT_THEME,
    WORD_PROCESSOR_FUZZY_GEN_CFG_COLLECTION,
    WORD_PROCESSOR_GENERAL_SETTING_COLLECTION,
    WORD_PROCESSOR_NOUN_CONV_CFG_COLLECTION,
    WORD_PROCESSOR_VERB_EXCEPTIONS_COLLECTION,
    WORD_PROCESSOR_VERB_GROUPS_COLLECTION,
    WORD_PROCESSOR_SCHEMAS
)

# @Classes
from .spanishConjugator.Conjugator import Conjugator
from .spanishFuzzyTermsGenerator.FuzzyTermsGenerator import FuzzyTermsGenerator
from .spanishNounConversor.Conversor import Conversor

# @Configs
word_processor_default_cfg = load_dict_from_json('wordProcessor-default_config')

class WordProcessorController:
    """
    Controlador del modulo de procesamiento de palabras. Administra los modulos y 
    permite crear, modificar y establecer diferentes configuraciones para los modulos.

    Al iniciar se conecta a la base de datos para obtener tanto la configuración activa
    como los perfiles correspondientes a dicho tema.
    """
    def __init__(self, mode = 0):
        self.__init_success = False
        self.__conjugator_active_theme = ''
        self.__fuzzy_gen_active_theme = ''
        self.__noun_conversor_active_theme = ''
        self.__conjugator_general_cfg = dict({})
        self.__conjugator_verb_exceptions = dict({})
        self.__conjugator_verb_groups = dict({})
        self.__fuzzy_generator_cfg = dict({})
        self.__noun_conversor_cfg = dict({})
        self.__initializate_cfg(mode)

    def __initializate_cfg(self, mode):
        """
        [private] Obtiene el tema de configuración activa para cada modulo y carga cada perfil
        de configuración.
        """
        try:
            self.__initialize_controller()
            self.__initialize_conjugator()
            self.__initialize_fuzzy_generator()
            self.__initialize_noun_conversor()
            self.conjugator = Conjugator(mode, self.__conjugator_general_cfg, self.__conjugator_verb_groups, self.__conjugator_verb_exceptions)
            self.fuzzy_generator = FuzzyTermsGenerator(self.__fuzzy_generator_cfg)
            self.conversor = Conversor(self.__noun_conversor_cfg)
            self.__init_success = True
        except Exception as e:
            print(str(e)) # TODO: Logs
            self.__init_success = False

    def __initialize_controller(self):
        """
        [private] Inicializa el controlador cargando los perfiles de configuración activos
        para cada modulo.
        """
        if not db_check_collection(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_GENERAL_SETTING_COLLECTION):
            db_insert_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_GENERAL_SETTING_COLLECTION, WORD_PROCESSOR_DEFAULT_CFG_OBJECT)
            self.__conjugator_active_theme = WORD_PROCESSOR_DEFAULT_CFG_OBJECT['conjugator_active_theme']
            self.__fuzzy_gen_active_theme = WORD_PROCESSOR_DEFAULT_CFG_OBJECT['fuzzy_gen_active_theme']
            self.__noun_conversor_active_theme = WORD_PROCESSOR_DEFAULT_CFG_OBJECT['noun_conversor_active_theme']
        else:
            db_data = db_get_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_GENERAL_SETTING_COLLECTION, None, {'_id': 0 })
            self.__conjugator_active_theme = db_data['conjugator_active_theme']
            self.__fuzzy_gen_active_theme = db_data['fuzzy_gen_active_theme']
            self.__noun_conversor_active_theme = db_data['noun_conversor_active_theme']

    def __initialize_conjugator(self):
        """
        [private] Verifica si ya existen entradas para los perfiles de configuración en la 
        base de datos e inicializa el conjugador.

        Si no existen perfiles, carga el archivo de configuración por defecto y lo almacena en la 
        base de datos. En caso contrario, obtiene la configuración activa desde la base de datos.
        """
        if not db_check_collection(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_CONJ_CFG_COLLECTION):
            self.__initialize_conjugator_cfg()
        else:
            self.__get_conjugator_cfg()

    def __initialize_conjugator_cfg(self):
        """
        [private] Inicializa la configuración del conjugador cuando aun no hay entradas en la 
        base de datos. Obtiene los datos del archivo de configuración por defecto y 
        almacena las entradas.
        """
        db_drop_collection(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_CONJ_CFG_COLLECTION)
        db_drop_collection(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_VERB_EXCEPTIONS_COLLECTION)
        db_drop_collection(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_VERB_GROUPS_COLLECTION)
        conjugator_verb_exceptions = self.__generate_verb_exceptions()
        db_batch_operation(WORD_PROCESSOR_CONFIG_DB, [
            {'type': DB_OPERATION_INSERT, 'col_name': WORD_PROCESSOR_CONJ_CFG_COLLECTION, 'data': word_processor_default_cfg['conjugator_config']},
            {'type': DB_OPERATION_INSERT_MANY, 'col_name': WORD_PROCESSOR_VERB_EXCEPTIONS_COLLECTION, 'data': conjugator_verb_exceptions},
            {'type': DB_OPERATION_INSERT, 'col_name': WORD_PROCESSOR_VERB_GROUPS_COLLECTION, 'data': word_processor_default_cfg['conjugator_irregular_groups']}
        ])
        self.__conjugator_general_cfg = word_processor_default_cfg['conjugator_config']
        self.__conjugator_verb_exceptions = conjugator_verb_exceptions
        self.__conjugator_verb_groups = word_processor_default_cfg['conjugator_irregular_groups']

    def __generate_verb_exceptions(self):
        """
        [private] A partir de las excepciones almacenadas en el archivo de configuraciones por defecto
        crea una lista con todas las expceciones para insertar en la base de datos.
        """
        verb_exceptions = list([])
        for verb_exception in word_processor_default_cfg['conjugator_verb_exceptions']['exceptions']:
            verb_exception['theme'] = WORD_PROCESSOR_DEFAULT_THEME
            verb_exceptions.append(verb_exception)
        return verb_exceptions

    def __get_conjugator_cfg(self):
        """
        [private] Obtiene las configuraciones del conjugador almacenadas en la base de datos para el
        tema activo.
        """
        self.__conjugator_general_cfg = db_get_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_CONJ_CFG_COLLECTION, {'theme': self.__conjugator_active_theme}, {'_id': 0, 'theme': 0})
        self.__conjugator_verb_exceptions = []
        for exception in db_get_items(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_VERB_EXCEPTIONS_COLLECTION, {'theme': self.__conjugator_active_theme}, {'_id': 0, 'theme': 0}):
            self.__conjugator_verb_exceptions.append(exception)
        self.__conjugator_verb_groups = db_get_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_VERB_GROUPS_COLLECTION, {'theme': self.__conjugator_active_theme}, {'_id': 0, 'theme': 0})

    def __initialize_fuzzy_generator(self):
        """
        [private] Verifica si existen entradas en la base de datos para el generador de terminos
        distorcionados. De existir obtiene las configuraciones de la base de datos. En caso
        contrario, almacena en la base de datos las configuraciones almacenadas en el archivo
        de configuración por defecto.
        """
        if not db_check_collection(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_FUZZY_GEN_CFG_COLLECTION):
            self.__initialize_fuzzy_generator_cfg()
        else:
            self.__get_fuzzy_generator_cfg()

    def __initialize_fuzzy_generator_cfg(self):
        """
        [private] A partir del archivo de configuraciones, inicializa la configuracion por defecto
        en la base de datos.
        """
        db_drop_collection(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_FUZZY_GEN_CFG_COLLECTION)
        db_insert_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_FUZZY_GEN_CFG_COLLECTION, word_processor_default_cfg['fuzzy_terms_generator_config'])
        self.__fuzzy_generator_cfg = word_processor_default_cfg['fuzzy_terms_generator_config']

    def __get_fuzzy_generator_cfg(self):
        """
        [private] Obtiene las configuraciones del generador de terminos distoricionados para
        el tema activo desde la base de datos
        """
        self.__fuzzy_generator_cfg = db_get_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_FUZZY_GEN_CFG_COLLECTION, {'theme': self.__fuzzy_gen_active_theme}, {'_id': 0, 'theme': 0})

    def __initialize_noun_conversor(self):
        """
        [private] Inicializa el conversor de sustantivos. Si ya existe la información en la base
        de datos, obtiene los datos para el tema activo desde la misma. En caso contario, obtiene
        la configuración por defecto del archivo de configuraciones y almacena las mismas
        en la base de datos 
        """
        if not db_check_collection(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_NOUN_CONV_CFG_COLLECTION):
            self.__initialize_noun_conversor_cfg()
        else:
            self.__get_noun_conversor_cfg()

    def __initialize_noun_conversor_cfg(self):
        """
        [private] Obtiene la configuración por defecto del conversor de sustantivos y hace el 
        almacenamiento inicial de dicha configuración en la base de datos.
        """
        db_drop_collection(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_NOUN_CONV_CFG_COLLECTION)
        db_insert_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_NOUN_CONV_CFG_COLLECTION, word_processor_default_cfg['noun_conversor_config'])
        self.__noun_conversor_cfg = word_processor_default_cfg['noun_conversor_config']

    def __get_noun_conversor_cfg(self):
        """
        [private] Obtiene de la base de datos la configuración del conversor de sustantivos para
        el tema activo.
        """
        self.__noun_conversor_cfg = db_get_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_NOUN_CONV_CFG_COLLECTION, {'theme': self.__noun_conversor_active_theme}, {'_id': 0, 'theme': 0})

    def retry_initialization(self):
        self.__initializate_cfg(self.mode)

    def get_conjugator_configs(self):
        return self.__conjugator_general_cfg

    def get_conjugator_exceptions(self):
        return self.__conjugator_verb_exceptions

    def get_conjugator_irr_groups(self):
        return self.__conjugator_verb_groups

    def get_noun_conversor_configs(self):
        return self.__noun_conversor_cfg

    def get_fuzzy_generator_configs(self):
        return self.__fuzzy_generator_cfg

    def map_conjugator_exception(self, exception):
        exception_copy = exception
        del exception_copy['theme']
        return exception_copy

    def get_available_conjugator_configs(self):
        try:
            available_configs = db_get_items(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_CONJ_CFG_COLLECTION, fields={'_id': 0})
            available_exceptions = db_get_items(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_VERB_EXCEPTIONS_COLLECTION, fields={'_id': 0})
            available_irr_groups = db_get_items(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_VERB_GROUPS_COLLECTION, fields={'_id': 0})
            available_config_themes = []
            for config_theme in available_configs:
                theme_name = config_theme['theme']
                theme = dict({})
                theme['theme'] = theme_name
                theme['general_settings'] = config_theme
                theme['irregular_verb_exceptions'] = list(map(self.map_conjugator_exception, list(filter(lambda exception: exception['theme'] == theme_name, available_exceptions))))
                theme['irregular_verb_groups'] = next((group for group in available_irr_groups if group['theme'] == theme_name), {})
                del theme['general_settings']['theme']
                del theme['irregular_verb_groups']['theme']
                available_config_themes.append(theme)
            return available_config_themes
        except:
            return []

    def get_available_fuzzy_gen_configs(self):
        try:
            available_configs = list(db_get_items(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_FUZZY_GEN_CFG_COLLECTION, fields={'_id': 0}))
            return available_configs
        except:
            return []

    def get_available_conversor_configs(self):
        try:
            available_configs = list(db_get_items(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_NOUN_CONV_CFG_COLLECTION, fields={'_id': 0}))
            return available_configs
        except:
            return []

    def get_existing_themes(self, collection_name):
        return list(map(lambda theme: theme['theme'], list(db_get_items(WORD_PROCESSOR_CONFIG_DB, collection_name, fields={'_id': 0, 'theme': 1}))))

    def add_conjugator_config(self, theme_name, theme_config, theme_irregular_groups):
        try:
            existing_theme = theme_name in self.get_existing_themes(WORD_PROCESSOR_CONJ_CFG_COLLECTION)
            if existing_theme or not validate_config(WORD_PROCESSOR_SCHEMAS['CONJ_GENERAL_CFG'], theme_config) or not validate_config(WORD_PROCESSOR_SCHEMAS['CONJ_IRR_GROUPS'], theme_irregular_groups):
                return False
            updated_theme_config = copy.deepcopy(theme_config)
            updated_irregular_groups = copy.deepcopy(theme_irregular_groups)
            updated_theme_config['theme'] = theme_name
            updated_irregular_groups['theme'] = theme_name
            db_batch_operation(WORD_PROCESSOR_CONFIG_DB, [
                {'type': DB_OPERATION_INSERT, 'col_name': WORD_PROCESSOR_CONJ_CFG_COLLECTION, 'data': updated_theme_config},
                {'type': DB_OPERATION_INSERT, 'col_name': WORD_PROCESSOR_VERB_GROUPS_COLLECTION, 'data': updated_irregular_groups}
            ])
            return True
        except:
            return False

    def add_conjugator_exceptions(self, theme_name, exceptions):
        try:
            if not theme_name in self.get_existing_themes(WORD_PROCESSOR_CONJ_CFG_COLLECTION):
                return False
            transaction_data = []
            for exception in exceptions:
                if not validate_config(WORD_PROCESSOR_SCHEMAS['CONJ_EXCEPTIONS'], exception):
                    return False
                updated_exception = copy.deepcopy(exception)
                updated_exception['theme'] = theme_name
                transaction_data.append({'type': DB_OPERATION_INSERT, 'col_name': WORD_PROCESSOR_VERB_EXCEPTIONS_COLLECTION, 'data': updated_exception})
            db_batch_operation(WORD_PROCESSOR_CONFIG_DB, transaction_data)
            return True
        except Exception as e:
            print(e)
            return False

    def add_fuzzy_gen_config(self, theme_name, config):
        try:
            existing_theme = theme_name in self.get_existing_themes(WORD_PROCESSOR_FUZZY_GEN_CFG_COLLECTION)
            if existing_theme or not validate_config(WORD_PROCESSOR_SCHEMAS['FUZZY_GENERAL_CFG'], config):
                return False
            updated_config = copy.deepcopy(config)
            updated_config['theme'] = theme_name
            db_insert_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_FUZZY_GEN_CFG_COLLECTION, updated_config)
            return True
        except:
            return False
    
    def add_noun_conversor_config(self, theme_name, config):
        try:
            existing_theme = theme_name in self.get_existing_themes(WORD_PROCESSOR_NOUN_CONV_CFG_COLLECTION)
            if existing_theme or not validate_config(WORD_PROCESSOR_SCHEMAS['NOUN_CONV_GENERAL_CFG'], config):
                return False
            updated_config = copy.deepcopy(config)
            updated_config['theme'] = theme_name
            db_insert_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_NOUN_CONV_CFG_COLLECTION, updated_config)
            return True
        except Exception as e:
            print(e)
            return False

    def conjugate_verb(self, verb=''):
        if not self.__init_success:
            return
        return self.conjugator.generar_conjugaciones(verb.lower())

    def conjugate_verb_table_view(self, verb=''):
        if not self.__init_success:
            return
        self.conjugator.table_view(verb.lower())

    def get_fuzzy_set(self, term='', max_distance=1):
        if not self.__init_success:
            return
        return self.fuzzy_generator.get_fuzzy_tokens(term.lower(), max_distance)

    def get_plural(self, noun=''):
        if not self.__init_success:
            return
        return self.conversor.a_plural(noun.lower())
