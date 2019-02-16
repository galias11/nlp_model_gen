# @Vendors
import copy

# @Contants
from src.constants.constants import (
    DB_OPERATION_DELETE,
    DB_OPERATION_DELETE_MANY,
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

# @Utils
from src.utils.fileUtils import load_dict_from_json
from src.utils.objectUtils import (
    update_dict,
    remove_object_from_list
)
from src.utils.dbUtils import (
    db_check_collection,
    db_delete_items,
    db_insert_item,
    db_get_items,
    db_get_item,
    db_drop_collection,
    db_batch_operation,
    db_update_item
)
from .packageUtils.validations import validate_config

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
    def __init__(self, mode=0):
        self.__init_success = False
        self.__conjugator_active_theme = ''
        self.__fuzzy_gen_active_theme = ''
        self.__noun_conversor_active_theme = ''
        self.__conjugator_general_cfg = dict({})
        self.__conjugator_verb_exceptions = list([])
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
            self.__conjugator = Conjugator(mode, self.__conjugator_general_cfg, self.__conjugator_verb_groups, self.__conjugator_verb_exceptions)
            self.__fuzzy_generator = FuzzyTermsGenerator(self.__fuzzy_generator_cfg)
            self.__conversor = Conversor(self.__noun_conversor_cfg)
            self.__init_success = True
        except:
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
        """
        Reintenta la inicialización del controlador.
        """
        self.__initializate_cfg(self.mode)

    def get_conjugator_configs(self):
        """
        Devuelve la configuración activa del conjugador.

        :return: [Dict] - Objeto de configuración general activa del conjugador.
        """
        return self.__conjugator_general_cfg

    def get_conjugator_exceptions(self):
        """
        Devuelve el conjunto de excepciones activas para el conjugador.

        :return: [List(Dict)] - Lista de excepciones activa del conjugador.
        """
        return self.__conjugator_verb_exceptions

    def get_conjugator_irr_groups(self):
        """
        Devuelve la configuración de grupos irregulares activa para el conjugador.

        :return: [Dict] - Lista de grupos irregulares activa del conjugador. 
        """
        return self.__conjugator_verb_groups

    def get_noun_conversor_configs(self):
        """
        Devuelve la configuración activa para el conversor de sustantivos.

        :return: [Dict] - Objeto de configuración activa del conversor de sustantivos.
        """
        return self.__noun_conversor_cfg

    def get_fuzzy_generator_configs(self):
        """
        Devuelve la configuración activa para el generador fuzzy.

        :return: [Dict] - Objeto de configuración activa del generador fuzzy.
        """
        return self.__fuzzy_generator_cfg

    def map_conjugator_exception(self, exception):
        """
        Mapea el nombre del theme en una excepción

        :exception: [Dict] - Objeto con los datos de la excepción

        :return: [Dict] - Clon del objeto original con el theme name agregado.
        """
        exception_copy = copy.deepcopy(exception)
        del exception_copy['theme']
        return exception_copy

    def filter_theme_exceptions(self, theme_name, exception_list=None):
        """
        Filtra las excepciones correspondientes a un determinado theme de una lista de excepciones.

        :theme_name: [String] - Nombre del tema.

        :exception_list: [List(Dict)] - Lista de excepciones.

        :return: [List(Dict)] - Lista de excepciones filtradas.
        """
        if exception_list is not None:
            filtered_exceptions_list = copy.deepcopy(list(exception_list))
        else:
            filtered_exceptions_list = []
        filtered_exceptions_list = list(filter(lambda exception: exception['theme'] == theme_name, filtered_exceptions_list))
        return list(map(self.map_conjugator_exception, filtered_exceptions_list))

    def get_available_conjugator_configs(self):
        """
        Devuelve todas las configuraciones disponibles para el conjugador

        :return: [List(Dict)] - Lista con todos temas de configuración disponibles.
        """
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
                theme['irregular_verb_exceptions'] = self.filter_theme_exceptions(theme_name, available_exceptions)
                theme['irregular_verb_groups'] = dict(next((group for group in available_irr_groups if group['theme'] == theme_name), {}))
                del theme['general_settings']['theme']
                del theme['irregular_verb_groups']['theme']
                available_config_themes.append(theme)
            return available_config_themes
        except:
            return []

    def get_available_fuzzy_gen_configs(self):
        """
        Devuelve todas las configuraciones disponibles para el generador de terminos Fuzzy.

        :return: [List(Dict)] - Lista con todos los temas de configuración disponibles.
        """
        try:
            available_configs = db_get_items(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_FUZZY_GEN_CFG_COLLECTION, fields={'_id': 0})
            return available_configs
        except:
            return []

    def get_available_conversor_configs(self):
        """
        Devuelve todas las configuraciones disponibles para el conversor de sustantivos.

        :return: [List(Dict)] - Lista con todos los temas de configuración disponibles.
        """
        try:
            available_configs = db_get_items(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_NOUN_CONV_CFG_COLLECTION, fields={'_id': 0})
            return available_configs
        except:
            return []

    def __get_existing_themes(self, collection_name):
        """
        Obtiene todos los themes disponibles dentro de una collección de la base de datos

        :collection_name: Nombre de la colección de la base de datos donde buscar los temás disponibles

        :return: [List(String)] - Lista con los nombres de todos los temas disponibles.
        """
        return list(map(lambda theme: theme['theme'], db_get_items(WORD_PROCESSOR_CONFIG_DB, collection_name, fields={'_id': 0, 'theme': 1})))

    def add_conjugator_config(self, theme_name, theme_config, theme_irregular_groups):
        """
        Agrega un nuevo tema de configuración general y grupos de verbos irregulares a la base de datos.
        El nuevo tema no debe existir.

        :theme_name: [String] - Nombre del tema.

        :theme_config: [Dict] - Objeto de configuración con el nuevo tema de configuración general. Debe 
        validar con la schema de validación correspondiente.

        :theme_irregular_groups: [Dict] - Objeto de configuración con el la configuración de grupos irregulares
        para el nuevo tema. Debe validar con la schema de validación correspondiente.

        :return: [Bool] - True si se ha agregado exitosamente, False en caso contrario.
        """
        try:
            existing_theme = theme_name in self.__get_existing_themes(WORD_PROCESSOR_CONJ_CFG_COLLECTION)
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
        except Exception as e:
            print(e)
            return False

    def add_conjugator_exceptions(self, theme_name, exceptions):
        """
        Agrega un conjunto de excepciones nuevo para el conjugador a la base de datos para el theme indicado.
        El theme debe existir.

        :theme_name: [String] - Nombre del tema.

        :exceptions: [List(Dict)] - Arreglo de excepciones a registrar. Debe cumplir con la schema de validación.

        :return: [bool] - True si se ha agregado exitosamente, False en caso contrario.
        """
        try:
            if theme_name == WORD_PROCESSOR_DEFAULT_THEME or not theme_name in self.__get_existing_themes(WORD_PROCESSOR_CONJ_CFG_COLLECTION):
                return False
            transaction_data = []
            for exception in exceptions:
                if not validate_config(WORD_PROCESSOR_SCHEMAS['CONJ_EXCEPTIONS'], exception):
                    return False
                if self.__check_exception_existence(theme_name, exception['key']):
                    return False
                updated_exception = copy.deepcopy(exception)
                updated_exception['theme'] = theme_name
                transaction_data.append({'type': DB_OPERATION_INSERT, 'col_name': WORD_PROCESSOR_VERB_EXCEPTIONS_COLLECTION, 'data': updated_exception})
            db_batch_operation(WORD_PROCESSOR_CONFIG_DB, transaction_data)
            if theme_name == self.__conjugator_active_theme:
                updated_exceptions = self.get_conjugator_exceptions()
                updated_exceptions.extend(exceptions)
                self.__conjugator_verb_exceptions = updated_exceptions
                self.__conjugator.set_irregular_verb_exceptions_config(self.__conjugator_verb_exceptions)
            return True
        except:
            return False

    def add_fuzzy_gen_config(self, theme_name, config):
        """
        Agrega un nuevo theme de configuración para el generador fuzzy. No debe existir un theme con el nombre indicado
        registrado.

        :theme_name: [String] - Nombre del theme a agregar

        :config: [Dict] - Objeto de configuración para el nuevo theme. Debe cumplir con la schema de validación

        :return: [bool] - True si se ha agregado exitosamente, False en caso contrario.
        """
        try:
            existing_theme = theme_name in self.__get_existing_themes(WORD_PROCESSOR_FUZZY_GEN_CFG_COLLECTION)
            if existing_theme or not validate_config(WORD_PROCESSOR_SCHEMAS['FUZZY_GENERAL_CFG'], config):
                return False
            updated_config = copy.deepcopy(config)
            updated_config['theme'] = theme_name
            db_insert_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_FUZZY_GEN_CFG_COLLECTION, updated_config)
            return True
        except:
            return False
    
    def add_noun_conversor_config(self, theme_name, config):
        """
        Agrega un nuevo theme de configuración para el conversor de sustantivos. No debe existir un theme con el nombre
        indicado previamente registrado.

        :theme_name: [String] - Nombre del theme a agregar

        :config: [Dict] - Objeto de cponfiguración para el nuevo theme. Debe cumplir con la schema de validación.

        :return: [bool] - True si se ha agregado exitosamente, False en caso contrario.
        """
        try:
            existing_theme = theme_name in self.__get_existing_themes(WORD_PROCESSOR_NOUN_CONV_CFG_COLLECTION)
            if existing_theme or not validate_config(WORD_PROCESSOR_SCHEMAS['NOUN_CONV_GENERAL_CFG'], config):
                return False
            updated_config = copy.deepcopy(config)
            updated_config['theme'] = theme_name
            db_insert_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_NOUN_CONV_CFG_COLLECTION, updated_config)
            return True
        except:
            return False

    def __get_theme_data(self, theme_name, collection_name):
        """
        [Private] Obtiene los datos de configuración para un tema en particular en la colleción indicada.

        :theme_name: [String] - Nombre del tema a buscar.

        :collection_name: [String] - Nombre de la colección en la cual buscar

        :return: [Dict] - Objeto de configuración
        """
        theme_data = db_get_item(WORD_PROCESSOR_CONFIG_DB, collection_name, {'theme': theme_name}, {'_id': 0, 'theme': 0})
        return theme_data

    def update_conjugator_configs(self, theme_name, theme_config_mod, theme_irr_groups_mod):
        """
        Modifica la configuración y los grupos irregulares para un tema determinado. El tema a editar debe existir, 
        no se puede modificar el tema por defecto.

        :theme_name: [String] - Nombre del tema a editar

        :theme_config_mod: [Dict] - Objeto con los campos a actualizar de la configuración. Los campos que se editen 
        sobre el tema seleccionado deben cumplir con la schema de validación.

        :theme_irr_groups_mod: [Dict] - Objeto con los campos a actualizar de los grupos de verbos irregulares. Los 
        campos que se editen sobre el tema seleccionado deben cumplir con la schema de validación.

        :return: [Bool] - True si la edición fue exitosa, False en caso contrario.
        """
        try:
            config_data = self.__get_theme_data(theme_name, WORD_PROCESSOR_CONJ_CFG_COLLECTION)
            irr_groups_data = self.__get_theme_data(theme_name, WORD_PROCESSOR_VERB_GROUPS_COLLECTION)
            if theme_name == WORD_PROCESSOR_DEFAULT_THEME or config_data is None or irr_groups_data is None:
                return False
            updated_config_data = update_dict(config_data, theme_config_mod, ['theme'])
            updated_irr_groups_data = update_dict(irr_groups_data, theme_irr_groups_mod, ['theme'])
            if not validate_config(WORD_PROCESSOR_SCHEMAS['CONJ_GENERAL_CFG'], updated_config_data) or not validate_config(WORD_PROCESSOR_SCHEMAS['CONJ_IRR_GROUPS'], updated_irr_groups_data):
                return False
            db_batch_operation(WORD_PROCESSOR_CONFIG_DB, [
                {'type': DB_OPERATION_UPDATE, 'col_name': WORD_PROCESSOR_CONJ_CFG_COLLECTION, 'data': updated_config_data, 'query': {'theme': theme_name}},
                {'type': DB_OPERATION_UPDATE, 'col_name': WORD_PROCESSOR_VERB_GROUPS_COLLECTION, 'data': updated_irr_groups_data, 'query': {'theme': theme_name}}
            ])
            if theme_name == self.__conjugator_active_theme:
                self.__conjugator_general_cfg = updated_config_data
                self.__conjugator_verb_groups = updated_irr_groups_data
                self.__conjugator.set_general_config(updated_config_data)
                self.__conjugator.set_irregular_verb_exceptions_config(updated_config_data)
            return True
        except:
            return False

    def __check_exception_existence(self, theme_name, exception_key):
        """
        Valida que una excepción exista, en caso contrario devuelve false.

        :theme_name: [String] - Nombre del tema.

        :exception_key: [String] - Key de la excepción.

        :return: [Bool] - True si la excepción existe, False en caso contrario.
        """
        exception_data = db_get_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_VERB_EXCEPTIONS_COLLECTION, {'theme': theme_name, 'key': exception_key}, {'_id': 0})
        return exception_data is not None

    def update_conjugator_exception(self, theme_name, exception_key, exception_new_data):
        """
        Actualiza una excepción del conjunto de excepciones del conjugador para un tema. La key y el tema deben existir.
        No se pueden editar excepciones del tema por defecto. La excepción debe complir con la schema de validación.
        Por las caracteristicas de la excepción, se requiere que se provea el objeto completo y no solo los campos a
        modificar.

        :theme_name: [String] - Nombre del tema.

        :exception_key: [String] - Key o verbo del cual se eliminará la excepción.

        :return: [bool] - True si se elimino exitosamente, False en caso contrario.
        """
        try:
            if not self.__check_exception_existence(theme_name, exception_key) or theme_name == WORD_PROCESSOR_DEFAULT_THEME:
                return False
            updated_exception_data = update_dict(exception_new_data, {'key': exception_key})
            if not validate_config(WORD_PROCESSOR_SCHEMAS['CONJ_EXCEPTIONS'], updated_exception_data):
                return False
            updated_exception_data['theme'] = theme_name
            updated_entries = db_update_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_VERB_EXCEPTIONS_COLLECTION, {'theme': theme_name, 'key': exception_key}, updated_exception_data).matched_count
            if theme_name == self.__conjugator_active_theme:
                remove_object_from_list(self.__conjugator_verb_exceptions, {'theme': theme_name, 'key': exception_key})
                self.__conjugator_verb_exceptions.append(updated_exception_data)
                self.__conjugator.set_irregular_verb_exceptions_config(self.__conjugator_verb_exceptions)
            return updated_entries > 0
        except:
            return False

    def update_fuzzy_gen_config(self, theme_name, theme_config_mod):
        """
        Actualiza un tema de configuración para el generador de terminos fuzzy. El thema solicitado debe existir
        y no puede ser el tema por defecto. Además el tema actualizado debe cumplir con la schema de validación.

        :theme_name: [String] - Nombre del tema a actualizar.

        :theme_config_mod: [Dict] - Objeto con los campos a actualizar del theme.

        :return: [bool] - True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            existing_themes = self.__get_existing_themes(WORD_PROCESSOR_FUZZY_GEN_CFG_COLLECTION)
            if not theme_name in existing_themes or theme_name == WORD_PROCESSOR_DEFAULT_THEME:
                return False
            current_theme_data = db_get_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_FUZZY_GEN_CFG_COLLECTION, {'theme': theme_name}, {'_id': 0, 'theme': 0})
            updated_theme_data = update_dict(current_theme_data, theme_config_mod)
            if not validate_config(WORD_PROCESSOR_SCHEMAS['FUZZY_GENERAL_CFG'], updated_theme_data):
                return False
            updated_theme_data['theme'] = theme_name
            updated_entries = db_update_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_FUZZY_GEN_CFG_COLLECTION, {'theme': theme_name}, updated_theme_data).matched_count
            if theme_name == self.__fuzzy_gen_active_theme:
                self.__fuzzy_generator_cfg = updated_theme_data
                self.__fuzzy_generator.set_config(self.__fuzzy_generator_cfg)
            return updated_entries > 0
        except:
            return False

    def update_noun_conversor_config(self, theme_name, theme_config_mod):
        """
        Actualiza un tema de configuración para el conversor de sustantivos. El tema debe existir y no debe ser
        el tema por defecto. Además el tema debe cumplir con la schema de validación.

        :theme_name: [String] - Nombre del tema a actualizar.

        :theme_config_mod: [Dict] - Campos a modificar de la configuración actual.

        :return: [Bool] - True si la actualización es exitosa, False en caso contrario.
        """
        try:
            existing_themes = self.__get_existing_themes(WORD_PROCESSOR_NOUN_CONV_CFG_COLLECTION)
            if not theme_name in existing_themes or theme_name == WORD_PROCESSOR_DEFAULT_THEME:
                return False
            current_theme_data = db_get_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_NOUN_CONV_CFG_COLLECTION, {'theme': theme_name}, {'_id': 0, 'theme': 0})
            updated_theme_data = update_dict(current_theme_data, theme_config_mod)
            if not validate_config(WORD_PROCESSOR_SCHEMAS['NOUN_CONV_GENERAL_CFG'], updated_theme_data):
                return False
            updated_theme_data['theme'] = theme_name
            updated_entries = db_update_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_NOUN_CONV_CFG_COLLECTION, {'theme': theme_name}, updated_theme_data).matched_count
            if theme_name == self.__noun_conversor_active_theme:
                self.__noun_conversor_cfg = updated_theme_data
                self.__conversor.set_config(updated_theme_data)
            return updated_entries > 0
        except:
            return False

    def remove_conjugator_theme(self, theme_name):
        """
        Elimina completamente un tema de configuración para el conjugador. El tema debe existir, no se puede 
        eliminar el tema por defecto. Si el tema a a eliminar es el activo actualmente, se cambia el tema al tema por
        defecto.

        :theme_name: [String] - Nombre del tema.

        :return: [bool] - True si el borrado se realizó exitosamente, False en caso contrario.
        """
        try:
            existing_themes = self.__get_existing_themes(WORD_PROCESSOR_CONJ_CFG_COLLECTION)
            if not theme_name in existing_themes or theme_name == WORD_PROCESSOR_DEFAULT_THEME:
                return False
            theme_changed = True
            if theme_name == self.__conjugator_active_theme:
                theme_changed = self.set_conjugator_active_theme('default')
            if not theme_changed:
                return False
            db_batch_operation(WORD_PROCESSOR_CONFIG_DB, [
                {'type': DB_OPERATION_DELETE, 'col_name': WORD_PROCESSOR_CONJ_CFG_COLLECTION, 'query': {'theme': theme_name}},
                {'type': DB_OPERATION_DELETE_MANY, 'col_name': WORD_PROCESSOR_VERB_EXCEPTIONS_COLLECTION, 'query': {'theme': theme_name}},
                {'type': DB_OPERATION_DELETE, 'col_name': WORD_PROCESSOR_VERB_GROUPS_COLLECTION, 'query': {'theme': theme_name}}
            ])
            return True
        except:
            return False

    def remove_fuzzy_gen_theme(self, theme_name):
        """
        Elimina completamente un tema de configuración para el generador fuzzy. El tema debe existir, no se puede
        eliminar el tema por defecto.

        :theme_name: [String] - Nombre del tema

        :return: [bool] - True si el borrado se realizó exitosamente, False en caso contrario.
        """
        try:
            existing_themes = self.__get_existing_themes(WORD_PROCESSOR_FUZZY_GEN_CFG_COLLECTION)
            if not theme_name in existing_themes or theme_name == WORD_PROCESSOR_DEFAULT_THEME:
                return False
            theme_changed = True
            if theme_name == self.__fuzzy_gen_active_theme:
                theme_changed = self.set_fuzzy_generator_active_theme('default')
            if not theme_changed:
                return False
            db_delete_items(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_FUZZY_GEN_CFG_COLLECTION, {'theme': theme_name})
            return True
        except:
            return False

    def remove_noun_conversor_theme(self, theme_name):
        """
        Elimina completamente un tema de configuración para el conversor de sustantivos. El tema debe existir, no se puede
        elimnar el tema por defecto.

        :theme_name: [String] - Nombre del tema

        :return: [bool] - True si el borrado se realizó exitosamente, False en caso contrario.
        """
        try:
            existing_themes = self.__get_existing_themes(WORD_PROCESSOR_NOUN_CONV_CFG_COLLECTION)
            if not theme_name in existing_themes or theme_name == WORD_PROCESSOR_DEFAULT_THEME:
                return False
            theme_changed = True
            if theme_name == self.__noun_conversor_active_theme:
                theme_changed = self.set_noun_conversor_active_theme('default')
            if not theme_changed:
                return False
            db_delete_items(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_NOUN_CONV_CFG_COLLECTION, {'theme': theme_name})
            return True
        except:
            return False

    def set_conjugator_active_theme(self, theme_name):
        """
        Cambia el tema de configuración activo del conjugador. En primera instancia guarda los cambios en la base de datos. El
        tema debe existir y no debe ser el tema actual.

        :theme_name: [String] - Nombre del tema

        :return: [Bool] - True si el cambio se realizó con exito, False en caso contrario.
        """
        try:
            if theme_name == self.__conjugator_active_theme:
                return False
            existing_themes = self.__get_existing_themes(WORD_PROCESSOR_CONJ_CFG_COLLECTION)
            if not theme_name in existing_themes:
                return False
            next_config_theme = db_get_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_CONJ_CFG_COLLECTION, {'theme': theme_name}, {'_id': 0})
            next_verb_exceptions = db_get_items(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_VERB_EXCEPTIONS_COLLECTION, {'theme': theme_name}, {'_id': 0})
            next_verb_groups = db_get_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_VERB_GROUPS_COLLECTION, {'theme': theme_name}, {'_id': 0})
            db_update_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_GENERAL_SETTING_COLLECTION, None, {'conjugator_active_theme': theme_name})
            self.__conjugator_active_theme = theme_name
            self.__conjugator_general_cfg = next_config_theme
            self.__conjugator_verb_exceptions = next_verb_exceptions
            self.__conjugator_verb_groups = next_verb_groups
            self.__conjugator.set_general_config(next_config_theme)
            self.__conjugator.set_irregular_verb_exceptions_config(next_verb_exceptions)
            self.__conjugator.set_irregular_verb_groups_config(next_verb_groups)
            return True
        except:
            return False

    def set_fuzzy_generator_active_theme(self, theme_name):
        """
        Cambia el tema de configuración activo del generador fuzzy. En primera instancia guarda los cambios en la base de datos. El
        tema debe existir y no debe ser el tema actual.

        :theme_name: [String] - Nombre del tema

        :return: [Bool] - True si el cambio se realizó con exito. False en caso contrario.
        """
        try:
            if theme_name == self.__fuzzy_gen_active_theme:
                return False
            existing_themes = self.__get_existing_themes(WORD_PROCESSOR_FUZZY_GEN_CFG_COLLECTION)
            if not theme_name in existing_themes:
                return False
            next_config_theme = db_get_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_FUZZY_GEN_CFG_COLLECTION, {'theme': theme_name}, {'_id': 0})
            db_update_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_GENERAL_SETTING_COLLECTION, None, {'fuzzy_gen_active_theme': theme_name})
            self.__fuzzy_gen_active_theme = theme_name
            self.__fuzzy_generator_cfg = next_config_theme
            self.__fuzzy_generator.set_config(next_config_theme)
            return True
        except:
            return False

    def set_noun_conversor_active_theme(self, theme_name):
        """
        Cambia el tema de configuración activo del conversor de sustantivos. En primera instancia guarda los cambios en la base de
        datos. El tema debe existir y no debe ser el tema actual.

        :theme_name: [String] - Nombre del tema.

        :return: [Bool] - True si el cambio se realizó con exito. False en caso contrario.
        """
        try:
            if theme_name == self.__noun_conversor_active_theme:
                return False
            existing_themes = self.__get_existing_themes(WORD_PROCESSOR_NOUN_CONV_CFG_COLLECTION)
            if not theme_name in existing_themes:
                return False
            next_config_theme = db_get_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_NOUN_CONV_CFG_COLLECTION, {'theme': theme_name}, {'_id': 0})
            db_update_item(WORD_PROCESSOR_CONFIG_DB, WORD_PROCESSOR_GENERAL_SETTING_COLLECTION, None, {'fuzzy_gen_active_theme': theme_name})
            self.__noun_conversor_active_theme = theme_name
            self.__noun_conversor_cfg = next_config_theme
            self.__conversor.set_config(next_config_theme)
            return True
        except:
            return False

    def conjugate_verb(self, verb=''):
        """
        Obtiene el objeto de conjugación para el verbo solicitado utilizando el conjugador. Si la inicialización no
        se hubiese realizado exitosamente no realiza la conjugación.

        :verb: [String] - verbo a conjugar.

        :return: [Dict] - Objeto de conjugación con las conjugaciones realizadas al verbo seleccionado. Si el objeto de
        configuración no esta correctamente inicializado devuelve None.
        """
        if not self.__init_success:
            return None
        return self.__conjugator.generar_conjugaciones(verb.lower())

    def conjugate_verb_table_view(self, verb=''):
        """
        Variación de conjugate_verb. Imprime por consola una tabla con la conjugación. Usar solo para testing. Si
        la inicialización no se ha realizado correctamente se sale prematuramente del método.

        :verb: [String] - Verbo a conjugar.
        """
        if not self.__init_success:
            return
        self.__conjugator.table_view(verb.lower())

    def get_fuzzy_set(self, term='', max_distance=1):
        """
        Obtiene un set de deformaciones para un termino que cumplan con la distancia máxima indicada. Si la inicialización
        no se ha realizado correctamente no se realiza la operación.

        :term: [String] - Termino a deformar.

        ;max_distanca: [Int] - Distancia de demerau-levenshtein máxima que puede tener el término deformado con el original,
        si no es provisto, por defecto será 1.

        :return: [Dict] - Si no se ha inicializado correctamente el controlador: None, En caso contrario devuelve un objeto
        con todas las deformaciones obtenidas.
        """
        if not self.__init_success:
            return None
        return self.__fuzzy_generator.get_fuzzy_tokens(term.lower(), max_distance)

    def get_plural(self, noun=''):
        """
        Obtiene el plural de un sustantivo. Si la inicialización no se ha completado correctamente no se realiza la operación.

        :noun: [String] - Sustantivo a partir del cual obtener el plural.

        :return: [String] - Si no se ha inicializado correctamente el controlado: None. En caso contrario, una cadena con el
        plural del sustantivo.
        """
        if not self.__init_success:
            return None
        return self.__conversor.a_plural(noun.lower())