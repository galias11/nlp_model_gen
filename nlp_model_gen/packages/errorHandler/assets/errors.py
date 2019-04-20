GENERIC_ERROR = {
    'error_code': 'E-0001', 
    'description': 'Error generico', 
    'source': {'class': 'N/A', 'method': 'N/A'},
    'log': None
}
ERROR_DATA = {
    'E-0002': {
        'description': 'Error al obtener colección de datos en la base de datos',
        'source': {'class': '', 'method': 'db_check_collection'},
        'log': 'L-0085'
    },
    'E-0003': {
        'description': 'Error al obtener elementos de la base de datos',
        'source': {'class': '', 'method': 'db_get_item'},
        'log': 'L-0086'
    },
    'E-0004': {
        'description': 'Error al obtener elementos de la base de datos',
        'source': {'class': '', 'method': 'db_get_items'},
        'log': 'L-0087'
    },
    'E-0005': {
        'description': 'Error al insertar elementos en la base de datos',
        'source': {'class': '', 'method': 'db_insert_item'},
        'log': 'L-0088'
    },
    'E-0006': {
        'description': 'Error al insertar elementos en la base de datos',
        'source': {'class': '', 'method': 'db_insert_items'},
        'log': 'L-0089'
    },
    'E-0007': {
        'description': 'Error al actualizar elementos en la base de datos',
        'source': {'class': '', 'method': 'db_update_item'},
        'log': None
    },
    'E-0008': {
        'description': 'Error al actualizar elementos en la base de datos',
        'source': {'class': '', 'method': 'db_update_many'},
        'log': None
    },
    'E-0009': {
        'description': 'Error al eliminar elemento de la base de datos',
        'source': {'class': '', 'method': 'db_delete_item'},
        'log': 'L-0090'
    },
    'E-0010': {
        'description': 'Error al eliminar elementos de la base de datos',
        'source': {'class': '', 'method': 'db_delete_items'},
        'log': 'L-0091'
    },
    'E-0011': {
        'description': 'Error al eliminar colección de la base de datos',
        'source': {'class': '', 'method': 'db_drop_collection'},
        'log': 'L-0092'
    },
    'E-0012': {
        'description': 'Error al procesar operación en batch',
        'source': {'class': '', 'method': 'db_batch_operation'},
        'log': 'L-0093'
    },
    'E-0013': {
        'description': 'Error al leer archivo JSON',
        'source': {'class': '', 'method': 'load_json_file'},
        'log': 'L-0357'
    },
    'E-0014': {
        'description': 'Error al escribir archivo JSON',
        'source': {'class': '', 'method': 'overwrite_json_file'},
        'log': 'L-0358'
    },
    'E-0015': {
        'description': 'Error al escribir archivo JSON',
        'source': {'class': '', 'method': 'remove_dir'},
        'log': 'L-0083'
    },
    'E-0016': {
        'description': 'Error al escribir archivo',
        'source': {'class': '', 'method': 'dictionary_to_disk'},
        'log': 'L-0359'
    },
    'E-0017': {
        'description': 'Error al obtener archivos',
        'source': {'class': '', 'method': 'get_files_in_dir'},
        'log': 'L-0360'
    },
    'E-0018': {
        'description': 'Error al copiar archivos',
        'source': {'class': '', 'method': 'copy_file'},
        'log': 'L-0361'
    },
    'E-0019': {
        'description': 'Error generico en el controlador de sistema',
        'source': {'class': 'SystemController', 'method': 'build_response_object'},
        'log': None
    },
    'E-0020': {
        'description': 'Error al inicializar modulo de procesamiento de palabras',
        'source': {'class': 'WordProcessorController', 'method': 'initializate_cfg'},
        'log': 'L-0040'
    },
    'E-0021': {
        'description': 'Error al inicializar modulo de gestión de modelos',
        'source': {'class': 'ModelManagerController', 'method': 'initialize'},
        'log': 'L-0053'
    },
    'E-0022': {
        'description': 'Error al inicializar modulo de gestión de modelos desde modulo de entrenamiento',
        'source': {'class': 'ModelTrainingController', 'method': 'init'},
        'log': 'L-0244'
    },
    'E-0023': {
        'description': 'Error al incializar modulo de datos de entrenamiento',
        'source': {'class': 'TrainDataManager', 'method': 'init'},
        'log': 'L-0256'
    },
    'E-0024': {
        'description': 'Error al inicializar el modulo de etiquetas personalizadas',
        'source': {'class': 'CustomEntityTagManager', 'method': 'init'},
        'log': 'L-0263'
    },
    'E-0025': {
        'description': 'Ya existe un modelo con el id deseado',
        'source': {'class': 'AdminModuleController', 'method': 'generate_model'},
        'log': None
    },
    'E-0026': {
        'description': 'La semilla de excepciones del tokenizer no es valida',
        'source': {'class': 'AdminModuleController', 'method': 'generate_model'},
        'log': None
    },
    'E-0027': {
        'description': 'El directorio temporal requerido para el modelo se encuentra ocupado',
        'source': {'class': 'TokenizerRulesGenerator', 'method': 'generate_model_data'},
        'log': None
    },
    'E-0028': {
        'description': 'Error al cargar modelo base de Spacy',
        'source': {'class': 'ModelLoader', 'method': 'initiate_default_model'},
        'log': None
    },
    'E-0029': {
        'description': 'El modelo ya existe en la base de datos',
        'source': {'class': 'ModelDataManager', 'method': 'save_model_data'},
        'log': 'L-0027'
    },
    'E-0030': {
        'description': 'El directorio donde debe guardarse el modelo ya existe',
        'source': {'class': 'ModelLoader', 'method': 'save_model'},
        'log': 'L-0031'
    },
    'E-0031': {
        'description': 'Hay una tarea de creación de modelos en curso',
        'source': {'class': 'SystemController', 'method': 'delete_word_processor_theme'},
        'log': None
    },
    'E-0032': {
        'description': 'El tema seleccionado no existe o es el tema por defecto',
        'source': {'class': 'WordProcessorController', 'method': 'remove_conjugator_theme'},
        'log': 'L-0199'
    },
    'E-0033': {
        'description': 'El tema seleccionado no existe o es el tema por defecto',
        'source': {'class': 'WordProcessorController', 'method': 'remove_fuzzy_gen_theme'},
        'log': 'L-0208'
    },
    'E-0034': {
        'description': 'El tema seleccionado no existe o es el tema por defecto',
        'source': {'class': 'WordProcessorController', 'method': 'remove_noun_conversor_theme'},
        'log': 'L-0217'
    },
    'E-0035': {
        'description': 'El tema seleccionado ya es el tema activo',
        'source': {'class': 'WordProcessorController', 'method': 'set_conjugator_active_theme'},
        'log': 'L-0142'
    },
    'E-0036': {
        'description': 'El tema seleccionado no existe',
        'source': {'class': 'WordProcessorController', 'method': 'set_conjugator_active_theme'},
        'log': 'L-0143'
    },
    'E-0037': {
        'description': 'El tema seleccionado ya es el tema activo',
        'source': {'class': 'WordProcessorController', 'method': 'set_fuzzy_generator_active_theme'},
        'log': 'L-0149'
    },
    'E-0038': {
        'description': 'El tema seleccionado no existe',
        'source': {'class': 'WordProcessorController', 'method': 'set_fuzzy_generator_active_theme'},
        'log': 'L-0150'
    },
    'E-0039': {
        'description': 'El tema seleccionado ya es el tema activo',
        'source': {'class': 'WordProcessorController', 'method': 'set_noun_conversor_active_theme'},
        'log': 'L-0156'
    },
    'E-0040': {
        'description': 'El tema seleccionado no existe',
        'source': {'class': 'WordProcessorController', 'method': 'set_noun_conversor_active_theme'},
        'log': 'L-0157'
    },
    'E-0041': {
        'description': 'Hay una tarea de creación de modelos en curso',
        'source': {'class': 'SystemController', 'method': 'update_word_processor_config_theme'},
        'log': None
    },
    'E-0042': {
        'description': 'El modulo del procesador de palabras especificado no existe',
        'source': {'class': 'AdminModuleController', 'method': 'set_word_processor_active_theme'},
        'log': None
    },
    'E-0043': {
        'description': 'El modulo del procesador de palabras especificado no existe',
        'source': {'class': 'AdminModuleController', 'method': 'delete_word_processor_theme'},
        'log': None
    },
    'E-0044': {
        'description': 'Hay una tarea de creación de modelos en curso',
        'source': {'class': 'SystemController', 'method': 'update_theme_conjugator_exceptions'},
        'log': None
    },
    'E-0045': {
        'description': 'Hay una tarea de creación de modelos en curso',
        'source': {'class': 'SystemController', 'method': 'update_word_processor_config_theme'},
        'log': None
    },
    'E-0046': {
        'description': 'La excepción no existe o se esta intentando modificar el tema por defecto',
        'source': {'class': 'WordProcessorController', 'method': 'update_conjugator_exception'},
        'log': 'L-0190'
    },
    'E-0047': {
        'description': 'La configuración de la excepción no tiene la estructura correcta',
        'source': {'class': 'WordProcessorController', 'method': 'update_conjugator_exception'},
        'log': 'L-0191'
    },
    'E-0048': {
        'description': 'No se ha podido actualizar la excepción en la base de datos',
        'source': {'class': 'WordProcessorController', 'method': 'update_conjugator_exception'},
        'log': None
    },
    'E-0049': {
        'description': 'El modulo del procesador de palabras especificado no existe',
        'source': {'class': 'AdminModuleController', 'method': 'update_word_processor_config_theme'},
        'log': None
    },
    'E-0050': {
        'description': 'El tema a actualizar no existe o es el tema por defecto',
        'source': {'class': 'WordProcessorController', 'method': 'update_conjugator_configs'},
        'log': 'L-0163'
    },
    'E-0051': {
        'description': 'Las configuraciones provistas no tienen la estructura correcta',
        'source': {'class': 'WordProcessorController', 'method': 'update_conjugator_configs'},
        'log': 'L-0164'
    },
    'E-0052': {
        'description': 'El tema a actualizar no existe o es el tema por defecto',
        'source': {'class': 'WordProcessorController', 'method': 'update_fuzzy_gen_config'},
        'log': 'L-0172'
    },
    'E-0053': {
        'description': 'La configuración provista no tiene la estructura correcta',
        'source': {'class': 'WordProcessorController', 'method': 'update_fuzzy_gen_config'},
        'log': 'L-0173'
    },
    'E-0054': {
        'description': 'No se ha podido actualizar la configuración en la base de datos',
        'source': {'class': 'WordProcessorController', 'method': 'update_fuzzy_gen_config'},
        'log': None
    },
    'E-0055': {
        'description': 'El tema a actualizar no existe o es el tema por defecto',
        'source': {'class': 'WordProcessorController', 'method': 'update_noun_conversor_config'},
        'log': 'L-0181'
    },
    'E-0056': {
        'description': 'La configuración provista no tiene la estructura correcta',
        'source': {'class': 'WordProcessorController', 'method': 'update_noun_conversor_config'},
        'log': 'L-0182'
    },
    'E-0057': {
        'description': 'No se ha podido actualizar la configuración en la base de datos',
        'source': {'class': 'WordProcessorController', 'method': 'update_noun_conversor_config'},
        'log': None
    },
    'E-0058': {
        'description': 'Hay una tarea de creación de modelos en curso',
        'source': {'class': 'SystemController', 'method': 'add_theme_conjugator_exceptions'},
        'log': None
    },
    'E-0059': {
        'description': 'El tema seleccionado no existe o es el tema por defecto',
        'source': {'class': 'WordProcessorController', 'method': 'add_conjugator_exceptions'},
        'log': 'L-0118'
    },
    'E-0060': {
        'description': 'La configuración de la excepción no tiene la estructura correcta',
        'source': {'class': 'WordProcessorController', 'method': 'add_conjugator_exceptions'},
        'log': 'L-0121'
    },
    'E-0061': {
        'description': 'Ya existe una excepción con la clave seleccionada',
        'source': {'class': 'WordProcessorController', 'method': 'add_conjugator_exceptions'},
        'log': 'L-0122'
    },
    'E-0062': {
        'description': 'Hay una tarea de creación de modelos en curso',
        'source': {'class': 'SystemController', 'method': 'add_word_processor_config_theme'},
        'log': None
    },
    'E-0063': {
        'description': 'El modulo del procesador de palabras especificado no existe',
        'source': {'class': 'AdminModuleController', 'method': 'add_word_processor_config_theme'},
        'log': None
    },
    'E-0064': {
        'description': 'El tema solicitado ya existe',
        'source': {'class': 'WordProcessorController', 'method': 'add_conjugator_config'},
        'log': None
    },
    'E-0065': {
        'description': 'Alguna de las configuraciones no posee la estructura correcta',
        'source': {'class': 'WordProcessorController', 'method': 'add_conjugator_config'},
        'log': 'L-0112'
    },
    'E-0066': {
        'description': 'El tema solicitado ya existe',
        'source': {'class': 'WordProcessorController', 'method': 'add_fuzzy_gen_config'},
        'log': None
    },
    'E-0067': {
        'description': 'Alguna de las configuraciones no posee la estructura correcta',
        'source': {'class': 'WordProcessorController', 'method': 'add_fuzzy_gen_config'},
        'log': 'L-0130'
    },
    'E-0068': {
        'description': 'El tema solicitado ya existe',
        'source': {'class': 'WordProcessorController', 'method': 'add_noun_conversor_config'},
        'log': None
    },
    'E-0069': {
        'description': 'Alguna de las configuraciones no posee la estructura correcta',
        'source': {'class': 'WordProcessorController', 'method': 'add_noun_conversor_config'},
        'log': 'L-0136'
    }
}
