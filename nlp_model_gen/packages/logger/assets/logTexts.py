TYPE_INFO = 'info'
TYPE_ERR = 'err'
TYPE_WRN = 'warn'
TYPE_SUCCESS = 'success'
LOG_DATA = {
    'L-0001': {
        'class_name': 'AdminModuleController',
        'method_name': 'generate_model',
        'main_text': 'Iniciando creación de modelo',
        'type': TYPE_INFO
    },
    'L-0002': {
        'class_name': 'AdminModuleController',
        'method_name': 'generate_model',
        'main_text': 'Creación abortada, modelo existente',
        'type': TYPE_ERR
    },
    'L-0003': {
        'class_name': 'TokenizerRulesGenerator',
        'method_name': 'generate_model_data',
        'main_text': 'Generando datos temporales del modelo',
        'type': TYPE_INFO
    },
    'L-0004': {
        'class_name': 'TokenizerRulesGenerator',
        'method_name': 'generate_model_data',
        'main_text': 'Archivos temporales generados',
        'type': TYPE_SUCCESS
    },
    'L-0005': {
        'class_name': 'TokenizerRulesGenerator',
        'method_name': 'generate_model_data',
        'main_text': 'Excepción al generar temporales de modelo: %s',
        'type': TYPE_INFO
    },
    'L-0006': {
        'class_name': 'TokenizerRulesGenerator',
        'method_name': 'generate_verb_rules',
        'main_text': 'Generando archivos temporales de modelo para categoria %s...',
        'type': TYPE_INFO
    },
    'L-0007': {
        'class_name': 'TokenizerRulesGenerator',
        'method_name': 'generate_verb_rules',
        'main_text': 'Archivos temporales de modelo generados para la categoria',
        'type': TYPE_SUCCESS
    },
    'L-0008': {
        'class_name': 'TokenizerRulesGenerator',
        'method_name': 'generate_verb_rules',
        'main_text': 'Generando diccionario para el término %s...',
        'type': TYPE_INFO
    },
    'L-0009': {
        'class_name': 'TokenizerRulesGenerator',
        'method_name': 'generate_noun_rules',
        'main_text': 'Generando archivos temporales de modelo para categoria %s...',
        'type': TYPE_INFO
    },
    'L-0010': {
        'class_name': 'TokenizerRulesGenerator',
        'method_name': 'generate_noun_rules',
        'main_text': 'Archivos temporales de modelo generados para la categoria',
        'type': TYPE_SUCCESS
    },
    'L-0011': {
        'class_name': 'TokenizerRulesGenerator',
        'method_name': 'generate_noun_rules',
        'main_text': 'Generando diccionario para el término %s...',
        'type': TYPE_INFO
    },
    'L-0012': {
        'class_name': 'TokenizerRulesGenerator',
        'method_name': 'generate_noun_rules',
        'main_text': 'Guardando semilla del modelo...',
        'type': TYPE_INFO
    },
    'L-0013': {
        'class_name': 'TokenizerRulesGenerator',
        'method_name': 'generate_noun_rules',
        'main_text': 'Semilla del modelo guardada',
        'type': TYPE_SUCCESS
    },
    'L-0014': {
        'class_name': 'TokenGenerator',
        'method_name': 'generate_verb_rules_set',
        'main_text': 'Procesando término %s...',
        'type': TYPE_INFO
    },
    'L-0015': {
        'class_name': 'TokenGenerator',
        'method_name': 'generate_noun_rules_set',
        'main_text': 'Procesando término %s...',
        'type': TYPE_INFO
    },
    'L-0016': {
        'class_name': 'AnalyzerRulesGenerator',
        'method_name': 'create_analyzer_rule_set',
        'main_text': 'Creando set de reglas de análisis para %s...',
        'type': TYPE_INFO
    },
    'L-0017': {
        'class_name': 'AnalyzerRulesGenerator',
        'method_name': 'create_analyzer_rule_set',
        'main_text': 'Set de reglas creado.',
        'type': TYPE_SUCCESS
    },
    'L-0018': {
        'class_name': 'AnalyzerRulesGenerator',
        'method_name': 'create_analyzer_rule_set',
        'main_text': 'Excepción al generar temporales de modelo: %s',
        'type': TYPE_INFO
    },
    'L-0019': {
        'class_name': 'ModelManager',
        'method_name': 'create_model',
        'main_text': 'Aborto: Modelo ya existe',
        'type': TYPE_ERR
    },
    'L-0020': {
        'class_name': 'ModelManager',
        'method_name': 'create_model',
        'main_text': 'Excepción al generar y guardar modelo de spacy: %s',
        'type': TYPE_INFO
    },
    'L-0021': {
        'class_name': 'ModelManager',
        'method_name': 'create_model',
        'main_text': 'Cargando nuevo modelo de Spacy',
        'type': TYPE_INFO
    },
    'L-0022': {
        'class_name': 'ModelManager',
        'method_name': 'create_model',
        'main_text': 'Modelo cargado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0023': {
        'class_name': 'ModelManager',
        'method_name': 'apply_tokenizer_exceptions',
        'main_text': 'Aplicando excepciones al tokenizer del modelo',
        'type': TYPE_INFO
    },
    'L-0024': {
        'class_name': 'ModelManager',
        'method_name': 'apply_tokenizer_exceptions',
        'main_text': 'Excepciones al tokenizer aplicadas',
        'type': TYPE_SUCCESS
    },
    'L-0025': {
        'class_name': 'ModelManager',
        'method_name': 'apply_tokenizer_exceptions',
        'main_text': 'Modelo generado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0026': {
        'class_name': 'ModelDataManager',
        'method_name': 'save_model_data',
        'main_text': 'Guardando datos del modelo en la base de datos...',
        'type': TYPE_INFO
    },
    'L-0027': {
        'class_name': 'ModelDataManager',
        'method_name': 'save_model_data',
        'main_text': 'Aborto: Modelo ya existe en base de datos',
        'type': TYPE_ERR
    },
    'L-0028': {
        'class_name': 'ModelDataManager',
        'method_name': 'save_model_data',
        'main_text': 'Excepción al guardar modelo en base de datos: %s',
        'type': TYPE_INFO
    },
    'L-0029': {
        'class_name': 'ModelDataManager',
        'method_name': 'save_model_data',
        'main_text': 'Modelo guardado en la base de datos exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0030': {
        'class_name': 'ModelLoader',
        'method_name': 'save_model',
        'main_text': 'Guardando archivos de modelo...',
        'type': TYPE_INFO
    },
    'L-0031': {
        'class_name': 'ModelLoader',
        'method_name': 'save_model',
        'main_text': 'Error al crear el directorio del modelo',
        'type': TYPE_ERR
    },
    'L-0032': {
        'class_name': 'ModelLoader',
        'method_name': 'save_model',
        'main_text': 'Archivos de modelo guardados correctamente',
        'type': TYPE_SUCCESS
    },
    'L-0033': {
        'class_name': 'ModelLoader',
        'method_name': 'save_model',
        'main_text': 'Excepción al guardar archivos de modelo: %s',
        'type': TYPE_INFO
    },
    'L-0034': {
        'class_name': 'AdminModuleController',
        'method_name': 'generate_model',
        'main_text': 'Removiendo archivos temporales de modelo',
        'type': TYPE_INFO
    },
    'L-0035': {
        'class_name': 'AdminModuleController',
        'method_name': 'generate_model',
        'main_text': 'Archivos temporales de modelo removidos',
        'type': TYPE_SUCCESS
    },
    'L-0036': {
        'class_name': 'AdminModuleController',
        'method_name': '__initialize',
        'main_text': 'Inicializando modulo de administración...',
        'type': TYPE_INFO
    },
    'L-0037': {
        'class_name': 'AdminModuleController',
        'method_name': '__initialize',
        'main_text': 'Inicialización exitosa',
        'type': TYPE_SUCCESS
    },
    'L-0038': {
        'class_name': 'WordProcessorController',
        'method_name': '__init__',
        'main_text': 'Inicializando modulo de procesamiento de palabras...',
        'type': TYPE_INFO
    },
    'L-0039': {
        'class_name': 'WordProcessorController',
        'method_name': '__initializate_cfg',
        'main_text': 'Inicialización exitosa del modulo de procesamiento de palabras',
        'type': TYPE_SUCCESS
    },
    'L-0040': {
        'class_name': 'WordProcessorController',
        'method_name': '__initializate_cfg',
        'main_text': 'Ocurrio una excepción al inicializar el modulo: %s',
        'type': TYPE_INFO
    },
    'L-0041': {
        'class_name': 'WordProcessorController',
        'method_name': '__initialize_controller',
        'main_text': 'Inicialilizando controlador...',
        'type': TYPE_INFO
    },
    'L-0042': {
        'class_name': 'WordProcessorController',
        'method_name': '__initialize_controller',
        'main_text': 'Controlador inicializado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0043': {
        'class_name': 'WordProcessorController',
        'method_name': '__initialize_conjugator',
        'main_text': 'Inicializando conjugador...',
        'type': TYPE_INFO
    },
    'L-0044': {
        'class_name': 'WordProcessorController',
        'method_name': '__initialize_conjugator',
        'main_text': 'Conjugador inicializado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0045': {
        'class_name': 'WordProcessorController',
        'method_name': '__initialize_fuzzy_generator',
        'main_text': 'Inicializando generador de terminos fuzzy...',
        'type': TYPE_INFO
    },
    'L-0046': {
        'class_name': 'WordProcessorController',
        'method_name': '__initialize_fuzzy_generator',
        'main_text': 'Generador de terminos fuzzy inicializado exitosamente...',
        'type': TYPE_SUCCESS
    },
    'L-0047': {
        'class_name': 'WordProcessorController',
        'method_name': '__initialize_noun_conversor',
        'main_text': 'Inicializando conversor de sustantivos...',
        'type': TYPE_INFO
    },
    'L-0048': {
        'class_name': 'WordProcessorController',
        'method_name': '__initialize_noun_conversor',
        'main_text': 'Conversor de sustantivos inicializado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0049': {
        'class_name': 'TokenizerRulesGenerator',
        'method_name': '__init__',
        'main_text': 'Inicializando generador de reglas para el tokenizer...',
        'type': TYPE_INFO
    },
    'L-0050': {
        'class_name': 'TokenizerRulesGenerator',
        'method_name': '__init__',
        'main_text': 'Generador de reglas del tokenizer inicializado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0051': {
        'class_name': 'ModelManagerController',
        'method_name': '__initialize',
        'main_text': 'Inicializando administrador de modelos...',
        'type': TYPE_INFO
    },
    'L-0052': {
        'class_name': 'ModelManagerController',
        'method_name': '__initialize',
        'main_text': 'Administrador de modelos inicializado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0053': {
        'class_name': 'ModelManagerController',
        'method_name': '__initialize',
        'main_text': 'Excepción al inicializar administrador de modelos: %s',
        'type': TYPE_INFO
    },
    'L-0054': {
        'class_name': 'ModelManagerController',
        'method_name': 'analyze_text',
        'main_text': 'Analizando texto...',
        'type': TYPE_INFO
    },
    'L-0055': {
        'class_name': 'ModelManagerController',
        'method_name': 'analyze_text',
        'main_text': 'El modelo no existe o no se ha provisto de un texto',
        'type': TYPE_ERR
    },
    'L-0056': {
        'class_name': 'Model',
        'method_name': 'load',
        'main_text': 'Cargando modelo de spaCy...',
        'type': TYPE_INFO
    },
    'L-0057': {
        'class_name': 'Model',
        'method_name': 'load',
        'main_text': 'Modelo de spaCy cargado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0058': {
        'class_name': 'ModelManagerController',
        'method_name': 'analyze_text',
        'main_text': 'Error al cargar el modelo de spaCy',
        'type': TYPE_ERR
    },
    'L-0059': {
        'class_name': 'Model',
        'method_name': 'analyze_text',
        'main_text': 'Analizando el texto con modelo de spaCy...',
        'type': TYPE_INFO
    },
    'L-0060': {
        'class_name': 'Model',
        'method_name': 'analyze_text',
        'main_text': 'Error al intentar utilizar el modelo de spaCy',
        'type': TYPE_ERR
    },
    'L-0061': {
        'class_name': 'Model',
        'method_name': 'analyze_text',
        'main_text': 'Procesando resultados...',
        'type': TYPE_INFO
    },
    'L-0062': {
        'class_name': 'Model',
        'method_name': 'analyze_text',
        'main_text': 'Resultados procesados exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0063': {
        'class_name': 'Model',
        'method_name': 'analyze_text',
        'main_text': 'Texto analizado exitosamente con modelo de spaCy',
        'type': TYPE_SUCCESS
    },
    'L-0064': {
        'class_name': 'ModelManagerController',
        'method_name': 'remove_model',
        'main_text': 'Eliminando modelo...',
        'type': TYPE_INFO
    },
    'L-0065': {
        'class_name': 'ModelManagerController',
        'method_name': 'remove_model',
        'main_text': 'Modelo inexistente',
        'type': TYPE_ERR
    },
    'L-0066': {
        'class_name': 'ModelDataManager',
        'method_name': 'remove_model_data',
        'main_text': 'Eliminando modelo de la base de datos...',
        'type': TYPE_INFO
    },
    'L-0067': {
        'class_name': 'ModelDataManager',
        'method_name': 'remove_model_data',
        'main_text': 'Excepción al intentar elimnar modelo de la base de datos: %s',
        'type': TYPE_INFO
    },
    'L-0068': {
        'class_name': 'ModelManagerController',
        'method_name': 'remove_model',
        'main_text': 'Error al eliminar modelo de la base de datos',
        'type': TYPE_ERR
    },
    'L-0069': {
        'class_name': 'ModelManagerController',
        'method_name': 'remove_model',
        'main_text': 'Modelo eliminado de la base de datos',
        'type': TYPE_SUCCESS
    },
    'L-0070': {
        'class_name': 'ModelLoader',
        'method_name': 'delete_model_files',
        'main_text': 'Eliminando archivos del modelo...',
        'type': TYPE_INFO
    },
    'L-0071': {
        'class_name': 'ModelManagerController',
        'method_name': 'remove_model',
        'main_text': 'Error al eliminar los archivos del modelo',
        'type': TYPE_ERR
    },
    'L-0072': {
        'class_name': 'ModelManagerController',
        'method_name': 'remove_model',
        'main_text': 'Archivos del modelo eliminados exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0073': {
        'class_name': 'ModelManagerController',
        'method_name': 'remove_model',
        'main_text': 'Modelo eliminado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0074': {
        'class_name': 'AdminModuleController',
        'method_name': 'edit_model_data',
        'main_text': 'Modificando datos del modelo...',
        'type': TYPE_INFO
    },
    'L-0075': {
        'class_name': 'AdminModuleController',
        'method_name': 'edit_model_data',
        'main_text': 'Error: Modelo inexistente',
        'type': TYPE_ERR
    },
    'L-0076': {
        'class_name': 'AdminModuleController',
        'method_name': 'edit_model_data',
        'main_text': 'Error: Ningún dato que modificar',
        'type': TYPE_ERR
    },
    'L-0077': {
        'class_name': 'ModelManagerController',
        'method_name': 'edit_model',
        'main_text': 'Error: Modelo inexistente',
        'type': TYPE_ERR
    },
    'L-0078': {
        'class_name': 'ModelManagerController',
        'method_name': 'edit_model',
        'main_text': 'Error al modificar los datos en la base de datos',
        'type': TYPE_ERR
    },
    'L-0079': {
        'class_name': 'ModelDataManager',
        'method_name': 'modify_model_data',
        'main_text': 'Excepción al modificar datos en la base de datos: %s',
        'type': TYPE_INFO
    },
    'L-0080': {
        'class_name': 'ModelDataManager',
        'method_name': 'modify_model_data',
        'main_text': 'Modificando datos del modelo en la base de datos...',
        'type': TYPE_INFO
    },
    'L-0081': {
        'class_name': 'ModelDataManager',
        'method_name': 'modify_model_data',
        'main_text': 'Ya existe un modelo con el nuevo nombre',
        'type': TYPE_ERR
    },
    'L-0082': {
        'class_name': 'ModelDataManager',
        'method_name': 'modify_model_data',
        'main_text': 'Datos del modelo modificados exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0083': {
        'class_name': '',
        'method_name': 'remove_dir',
        'main_text': 'Excepción al eliminar el directorio: %s',
        'type': TYPE_INFO
    },
    'L-0084': {
        'class_name': '',
        'method_name': 'create_dir_if_not_exist',
        'main_text': 'Excepción al crear el directorio: %s',
        'type': TYPE_INFO
    },
    'L-0085': {
        'class_name': '',
        'method_name': 'db_check_collection',
        'main_text': 'Excepción al validar colección en BD: %s',
        'type': TYPE_INFO
    },
    'L-0086': {
        'class_name': '',
        'method_name': 'db_get_item',
        'main_text': 'Excepción al realizar consulta en BD: %s',
        'type': TYPE_INFO
    },
    'L-0087': {
        'class_name': '',
        'method_name': 'db_get_items',
        'main_text': 'Excepción al realizar consulta en BD: %s',
        'type': TYPE_INFO
    },
    'L-0088': {
        'class_name': '',
        'method_name': 'db_insert_item',
        'main_text': 'Excepción al guardar datos en BD: %s',
        'type': TYPE_INFO
    },
    'L-0089': {
        'class_name': '',
        'method_name': 'db_insert_items',
        'main_text': 'Excepción al guardar datos en BD: %s',
        'type': TYPE_INFO
    },
    'L-0090': {
        'class_name': '',
        'method_name': 'db_delete_item',
        'main_text': 'Excepción al eliminar datos en BD: %s',
        'type': TYPE_INFO
    },
    'L-0091': {
        'class_name': '',
        'method_name': 'db_delete_items',
        'main_text': 'Excepción al eliminar datos en BD: %s',
        'type': TYPE_INFO
    },
    'L-0092': {
        'class_name': '',
        'method_name': 'db_drop_collection',
        'main_text': 'Excepción al eliminar colección en BD: %s',
        'type': TYPE_INFO
    },
    'L-0093': {
        'class_name': '',
        'method_name': 'db_batch_operation',
        'main_text': 'Excepción al realizar operación en batch sobre la BD: %s',
        'type': TYPE_INFO
    },
    'L-0094': {
        'class_name': 'AdminModuleController',
        'method_name': 'generate_model',
        'main_text': 'El módulo no se ha inicializado correctamente.',
        'type': TYPE_ERR
    },
    'L-0095': {
        'class_name': 'AdminModuleController',
        'method_name': 'get_available_models',
        'main_text': 'El módulo no se ha inicializado correctamente.',
        'type': TYPE_ERR
    },
    'L-0096': {
        'class_name': 'AdminModuleController',
        'method_name': 'load_model',
        'main_text': 'El módulo no se ha inicializado correctamente.',
        'type': TYPE_ERR
    },
    'L-0097': {
        'class_name': 'AdminModuleController',
        'method_name': 'edit_model_data',
        'main_text': 'El módulo no se ha inicializado correctamente.',
        'type': TYPE_ERR
    },
    'L-0098': {
        'class_name': 'AdminModuleController',
        'method_name': 'delete_model_data',
        'main_text': 'El módulo no se ha inicializado correctamente.',
        'type': TYPE_ERR
    },
    'L-0099': {
        'class_name': 'AdminModuleController',
        'method_name': 'analyse_text',
        'main_text': 'El módulo no se ha inicializado correctamente.',
        'type': TYPE_ERR
    },
    'L-0100': {
        'class_name': 'WordProcessorController',
        'method_name': 'get_available_conjugator_configs',
        'main_text': 'Obteniendo configuración de la base de datos...',
        'type': TYPE_INFO
    },
    'L-0101': {
        'class_name': 'WordProcessorController',
        'method_name': 'get_available_conjugator_configs',
        'main_text': 'Los datos de configuración se han obtenido exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0102': {
        'class_name': 'WordProcessorController',
        'method_name': 'get_available_conjugator_configs',
        'main_text': 'Orgnizando datos de configuración...',
        'type': TYPE_INFO
    },
    'L-0103': {
        'class_name': 'WordProcessorController',
        'method_name': 'get_available_conjugator_configs',
        'main_text': 'Datos organizados exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0104': {
        'class_name': 'WordProcessorController',
        'method_name': 'get_available_conjugator_configs',
        'main_text': 'Excepción al obtener los datos de configuración: %s',
        'type': TYPE_INFO
    },
    'L-0105': {
        'class_name': 'WordProcessorController',
        'method_name': 'get_available_fuzzy_gen_configs',
        'main_text': 'Obteniendo configuraciones de la base de datos...',
        'type': TYPE_INFO
    },
    'L-0106': {
        'class_name': 'WordProcessorController',
        'method_name': 'get_available_fuzzy_gen_configs',
        'main_text': 'Configuraciones obtenidas exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0107': {
        'class_name': 'WordProcessorController',
        'method_name': 'get_available_fuzzy_gen_configs',
        'main_text': 'Excepción al obtener los datos de configuración: %s',
        'type': TYPE_INFO
    },
    'L-0108': {
        'class_name': 'WordProcessorController',
        'method_name': 'get_available_conversor_configs',
        'main_text': 'Obteniendo configuraciones de la base de datos...',
        'type': TYPE_INFO
    },
    'L-0109': {
        'class_name': 'WordProcessorController',
        'method_name': 'get_available_conversor_configs',
        'main_text': 'Configuraciones obtenidas exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0110': {
        'class_name': 'WordProcessorController',
        'method_name': 'get_available_conversor_configs',
        'main_text': 'Excepción al obtener los datos de configuración: %s',
        'type': TYPE_INFO
    },
    'L-0111': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_conjugator_config',
        'main_text': 'Validando tema de configuración...',
        'type': TYPE_INFO
    },
    'L-0112': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_conjugator_config',
        'main_text': 'Tema existente o configuraciones provistas no válidas',
        'type': TYPE_ERR
    },
    'L-0113': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_conjugator_config',
        'main_text': 'Nuevo tema validado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0114': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_conjugator_config',
        'main_text': 'Guardando nuevo tema...',
        'type': TYPE_INFO
    },
    'L-0115': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_conjugator_config',
        'main_text': 'Nuevo tema guardado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0116': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_conjugator_config',
        'main_text': 'Excepción al guardar el nuevo tema: %s',
        'type': TYPE_INFO
    },
    'L-0117': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_conjugator_exceptions',
        'main_text': 'Validando tema...',
        'type': TYPE_INFO
    },
    'L-0118': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_conjugator_exceptions',
        'main_text': 'Tema inexistente o se intenta modificar el tema por default.',
        'type': TYPE_ERR
    },
    'L-0119': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_conjugator_exceptions',
        'main_text': 'Datos del tema validados exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0120': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_conjugator_exceptions',
        'main_text': 'Construyendo datos de las nuevas excepciones...',
        'type': TYPE_INFO
    },
    'L-0121': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_conjugator_exceptions',
        'main_text': 'Una de las nuevas excepciones no cumple con el formato requerido',
        'type': TYPE_ERR
    },
    'L-0122': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_conjugator_exceptions',
        'main_text': 'Una de las nuevas excepciones ya se encuentra registrada',
        'type': TYPE_ERR
    },
    'L-0123': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_conjugator_exceptions',
        'main_text': 'Datos de las excepciones construidos exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0124': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_conjugator_exceptions',
        'main_text': 'Guardando datos...',
        'type': TYPE_INFO
    },
    'L-0125': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_conjugator_exceptions',
        'main_text': 'Datos guardados exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0126': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_conjugator_exceptions',
        'main_text': 'Modificando excepciones del tema activo...',
        'type': TYPE_INFO
    },
    'L-0127': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_conjugator_exceptions',
        'main_text': 'Excepciones del tema actvo modificadas exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0128': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_conjugator_exceptions',
        'main_text': 'Excepción al guardar nuevas configuraciones: %s',
        'type': TYPE_INFO
    },
    'L-0129': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_fuzzy_gen_config',
        'main_text': 'Validando tema...',
        'type': TYPE_INFO
    },
    'L-0130': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_fuzzy_gen_config',
        'main_text': 'Tema existente o configuraciones provistas no válidas',
        'type': TYPE_ERR
    },
    'L-0131': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_fuzzy_gen_config',
        'main_text': 'Tema validado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0132': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_fuzzy_gen_config',
        'main_text': 'Guardando datos...',
        'type': TYPE_INFO
    },
    'L-0133': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_fuzzy_gen_config',
        'main_text': 'Datos guardados exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0134': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_fuzzy_gen_config',
        'main_text': 'Excepción al guardar nuevas configuraciones: %s',
        'type': TYPE_INFO
    },
    'L-0135': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_noun_conversor_theme',
        'main_text': 'Validando tema...',
        'type': TYPE_INFO
    },
    'L-0136': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_noun_conversor_theme',
        'main_text': 'Tema existente o configuraciones provistas no válidas',
        'type': TYPE_ERR
    },
    'L-0137': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_noun_conversor_theme',
        'main_text': 'Tema validado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0138': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_noun_conversor_theme',
        'main_text': 'Guardando datos...',
        'type': TYPE_INFO
    },
    'L-0139': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_noun_conversor_theme',
        'main_text': 'Datos guardados exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0140': {
        'class_name': 'WordProcessorController',
        'method_name': 'add_noun_conversor_theme',
        'main_text': 'Excepción al guardar nuevas configuraciones: %s',
        'type': TYPE_INFO
    },
    'L-0141': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_conjugator_active_theme',
        'main_text': 'Validando tema...',
        'type': TYPE_INFO
    },
    'L-0142': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_conjugator_active_theme',
        'main_text': 'El tema solicitado ya es el tema activo',
        'type': TYPE_ERR
    },
    'L-0143': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_conjugator_active_theme',
        'main_text': 'El tema solicitado no existe',
        'type': TYPE_ERR
    },
    'L-0144': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_conjugator_active_theme',
        'main_text': 'Tema validado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0145': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_conjugator_active_theme',
        'main_text': 'Realizando cambio de tema...',
        'type': TYPE_INFO
    },
    'L-0146': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_conjugator_active_theme',
        'main_text': 'Tema cambiado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0147': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_conjugator_active_theme',
        'main_text': 'Excepción al intentar cambiar el tema: %s',
        'type': TYPE_INFO
    },
    'L-0148': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_fuzzy_generator_active_theme',
        'main_text': 'Validando tema...',
        'type': TYPE_INFO
    },
    'L-0149': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_fuzzy_generator_active_theme',
        'main_text': 'El tema solicitado ya es el tema activo',
        'type': TYPE_ERR
    },
    'L-0150': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_fuzzy_generator_active_theme',
        'main_text': 'El tema solicitado no existe',
        'type': TYPE_ERR
    },
    'L-0151': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_fuzzy_generator_active_theme',
        'main_text': 'Tema validado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0152': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_fuzzy_generator_active_theme',
        'main_text': 'Realizando cambio de tema...',
        'type': TYPE_INFO
    },
    'L-0153': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_fuzzy_generator_active_theme',
        'main_text': 'Tema cambiado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0154': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_fuzzy_generator_active_theme',
        'main_text': 'Excepción al intentar cambiar el tema: %s',
        'type': TYPE_INFO
    },
    'L-0155': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_noun_conversor_active_theme',
        'main_text': 'Validando tema...',
        'type': TYPE_INFO
    },
    'L-0156': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_noun_conversor_active_theme',
        'main_text': 'El tema solicitado ya es el tema activo',
        'type': TYPE_ERR
    },
    'L-0157': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_noun_conversor_active_theme',
        'main_text': 'El tema solicitado no existe',
        'type': TYPE_ERR
    },
    'L-0158': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_noun_conversor_active_theme',
        'main_text': 'Tema validado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0159': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_noun_conversor_active_theme',
        'main_text': 'Realizando cambio de tema...',
        'type': TYPE_INFO
    },
    'L-0160': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_noun_conversor_active_theme',
        'main_text': 'Tema cambiado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0161': {
        'class_name': 'WordProcessorController',
        'method_name': 'set_noun_conversor_active_theme',
        'main_text': 'Excepción al intentar cambiar el tema: %s',
        'type': TYPE_INFO
    },
    'L-0162': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_conjugator_configs',
        'main_text': 'Validando y construyendo datos actualizados...',
        'type': TYPE_INFO
    },
    'L-0163': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_conjugator_configs',
        'main_text': 'Intentando editar tema por defecto o tema con datos inconsistentes',
        'type': TYPE_ERR
    },
    'L-0164': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_conjugator_configs',
        'main_text': 'Los nuevos datos no tienen una estructura válida',
        'type': TYPE_ERR
    },
    'L-0165': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_conjugator_configs',
        'main_text': 'Datos validados y construidos correctamente',
        'type': TYPE_SUCCESS
    },
    'L-0166': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_conjugator_configs',
        'main_text': 'Actualizando datos...',
        'type': TYPE_INFO
    },
    'L-0167': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_conjugator_configs',
        'main_text': 'Datos actualizados correctamente',
        'type': TYPE_SUCCESS
    },
    'L-0168': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_conjugator_configs',
        'main_text': 'Actualizando datos del modelo en uso...',
        'type': TYPE_INFO
    },
    'L-0169': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_conjugator_configs',
        'main_text': 'Datos del modelo en uso actualizados correctamente',
        'type': TYPE_SUCCESS
    },
    'L-0170': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_conjugator_configs',
        'main_text': 'Excepción al actualizar el tema de configuración: %s',
        'type': TYPE_INFO
    },
    'L-0171': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_fuzzy_gen_config',
        'main_text': 'Validando y construyendo datos actualizados...',
        'type': TYPE_INFO
    },
    'L-0172': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_fuzzy_gen_config',
        'main_text': 'Intentando editar tema por defecto o tema con datos inconsistentes',
        'type': TYPE_ERR
    },
    'L-0173': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_fuzzy_gen_config',
        'main_text': 'Los nuevos datos no tienen una estructura válida',
        'type': TYPE_ERR
    },
    'L-0174': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_fuzzy_gen_config',
        'main_text': 'Datos validados y construidos correctamente',
        'type': TYPE_SUCCESS
    },
    'L-0175': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_fuzzy_gen_config',
        'main_text': 'Actualizando datos...',
        'type': TYPE_INFO
    },
    'L-0176': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_fuzzy_gen_config',
        'main_text': 'Datos actualizados correctamente',
        'type': TYPE_SUCCESS
    },
    'L-0177': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_fuzzy_gen_config',
        'main_text': 'Actualizando datos del modelo en uso...',
        'type': TYPE_INFO
    },
    'L-0178': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_fuzzy_gen_config',
        'main_text': 'Datos del modelo en uso actualizados correctamente',
        'type': TYPE_SUCCESS
    },
    'L-0179': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_fuzzy_gen_config',
        'main_text': 'Excepción al actualizar el tema de configuración: %s',
        'type': TYPE_INFO
    },
    'L-0180': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_noun_conversor_config',
        'main_text': 'Validando y construyendo datos actualizados...',
        'type': TYPE_INFO
    },
    'L-0181': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_noun_conversor_config',
        'main_text': 'Intentando editar tema por defecto o tema con datos inconsistentes',
        'type': TYPE_ERR
    },
    'L-0182': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_noun_conversor_config',
        'main_text': 'Los nuevos datos no tienen una estructura válida',
        'type': TYPE_ERR
    },
    'L-0183': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_noun_conversor_config',
        'main_text': 'Datos validados y construidos correctamente',
        'type': TYPE_SUCCESS
    },
    'L-0184': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_noun_conversor_config',
        'main_text': 'Actualizando datos...',
        'type': TYPE_INFO
    },
    'L-0185': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_noun_conversor_config',
        'main_text': 'Datos actualizados correctamente',
        'type': TYPE_SUCCESS
    },
    'L-0186': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_noun_conversor_config',
        'main_text': 'Actualizando datos del modelo en uso...',
        'type': TYPE_INFO
    },
    'L-0187': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_noun_conversor_config',
        'main_text': 'Datos del modelo en uso actualizados correctamente',
        'type': TYPE_SUCCESS
    },
    'L-0188': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_noun_conversor_config',
        'main_text': 'Excepción al actualizar el tema de configuración: %s',
        'type': TYPE_INFO
    },
    'L-0189': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_conjugator_exception',
        'main_text': 'Validando y construyendo datos actualizados...',
        'type': TYPE_INFO
    },
    'L-0190': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_conjugator_exception',
        'main_text': 'Intentando editar tema por defecto o tema con datos inconsistentes',
        'type': TYPE_ERR
    },
    'L-0191': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_conjugator_exception',
        'main_text': 'Los nuevos datos no tienen una estructura válida',
        'type': TYPE_ERR
    },
    'L-0192': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_conjugator_exception',
        'main_text': 'Datos validados y construidos correctamente',
        'type': TYPE_SUCCESS
    },
    'L-0193': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_conjugator_exception',
        'main_text': 'Actualizando datos...',
        'type': TYPE_INFO
    },
    'L-0194': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_conjugator_exception',
        'main_text': 'Datos actualizados correctamente',
        'type': TYPE_SUCCESS
    },
    'L-0195': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_conjugator_exception',
        'main_text': 'Actualizando datos del modelo en uso...',
        'type': TYPE_INFO
    },
    'L-0196': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_conjugator_exception',
        'main_text': 'Datos del modelo en uso actualizados correctamente',
        'type': TYPE_SUCCESS
    },
    'L-0197': {
        'class_name': 'WordProcessorController',
        'method_name': 'update_conjugator_exception',
        'main_text': 'Excepción al actualizar el tema de configuración: %s',
        'type': TYPE_INFO
    },
    'L-0198': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_conjugator_theme',
        'main_text': 'Validando datos del tema...',
        'type': TYPE_INFO
    },
    'L-0199': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_conjugator_theme',
        'main_text': 'El tema solicitado no existe o es el tema por defecto.',
        'type': TYPE_ERR
    },
    'L-0200': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_conjugator_theme',
        'main_text': 'Datos del tema validados exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0201': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_conjugator_theme',
        'main_text': 'Seleccionando tema por default como tema activo...',
        'type': TYPE_INFO
    },
    'L-0202': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_conjugator_theme',
        'main_text': 'Cambio de tema realizado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0203': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_conjugator_theme',
        'main_text': 'Error al cambiar el tema activo',
        'type': TYPE_ERR
    },
    'L-0204': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_conjugator_theme',
        'main_text': 'Eliminando datos...',
        'type': TYPE_INFO
    },
    'L-0205': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_conjugator_theme',
        'main_text': 'Exito al eliminar los datos',
        'type': TYPE_SUCCESS
    },
    'L-0206': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_conjugator_theme',
        'main_text': 'Excepción al borrar el tema de configuración: %s',
        'type': TYPE_INFO
    },
    'L-0207': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_fuzzy_gen_theme',
        'main_text': 'Validando datos del tema...',
        'type': TYPE_INFO
    },
    'L-0208': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_fuzzy_gen_theme',
        'main_text': 'El tema solicitado no existe o es el tema por defecto.',
        'type': TYPE_ERR
    },
    'L-0209': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_fuzzy_gen_theme',
        'main_text': 'Datos del tema validados exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0210': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_fuzzy_gen_theme',
        'main_text': 'Seleccionando tema por default como tema activo...',
        'type': TYPE_INFO
    },
    'L-0211': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_fuzzy_gen_theme',
        'main_text': 'Cambio de tema realizado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0212': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_fuzzy_gen_theme',
        'main_text': 'Error al cambiar el tema activo',
        'type': TYPE_ERR
    },
    'L-0213': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_fuzzy_gen_theme',
        'main_text': 'Eliminando datos...',
        'type': TYPE_INFO
    },
    'L-0214': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_fuzzy_gen_theme',
        'main_text': 'Exito al eliminar los datos',
        'type': TYPE_SUCCESS
    },
    'L-0215': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_fuzzy_gen_theme',
        'main_text': 'Excepción al borrar el tema de configuración: %s',
        'type': TYPE_INFO
    },
    'L-0216': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_noun_conversor_theme',
        'main_text': 'Validando datos del tema...',
        'type': TYPE_INFO
    },
    'L-0217': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_noun_conversor_theme',
        'main_text': 'El tema solicitado no existe o es el tema por defecto.',
        'type': TYPE_ERR
    },
    'L-0218': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_noun_conversor_theme',
        'main_text': 'Datos del tema validados exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0219': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_noun_conversor_theme',
        'main_text': 'Seleccionando tema por default como tema activo...',
        'type': TYPE_INFO
    },
    'L-0220': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_noun_conversor_theme',
        'main_text': 'Cambio de tema realizado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0221': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_noun_conversor_theme',
        'main_text': 'Error al cambiar el tema activo',
        'type': TYPE_ERR
    },
    'L-0222': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_noun_conversor_theme',
        'main_text': 'Eliminando datos...',
        'type': TYPE_INFO
    },
    'L-0223': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_noun_conversor_theme',
        'main_text': 'Exito al eliminar los datos',
        'type': TYPE_SUCCESS
    },
    'L-0224': {
        'class_name': 'WordProcessorController',
        'method_name': 'remove_noun_conversor_theme',
        'main_text': 'Excepción al borrar el tema de configuración: %s',
        'type': TYPE_INFO
    },
    'L-0225': {
        'class_name': 'TaskManager',
        'method_name': 'create_model_creation_task',
        'main_text': 'Generando tarea de creación de modelo...',
        'type': TYPE_INFO
    },
    'L-0226': {
        'class_name': 'TaskManager',
        'method_name': 'create_model_creation_task',
        'main_text': 'Tarea creada exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0227': {
        'class_name': 'TaskManager',
        'method_name': 'create_task',
        'main_text': 'Agregando tarea al administrador de tareas...',
        'type': TYPE_INFO
    },
    'L-0228': {
        'class_name': 'TaskManager',
        'method_name': 'create_task',
        'main_text': 'Tarea agregada exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0229': {
        'class_name': 'Task',
        'method_name': 'run',
        'main_text': 'Ejecutando tarea %s...',
        'type': TYPE_INFO
    },
    'L-0230': {
        'class_name': 'Task',
        'method_name': 'run',
        'main_text': 'Tarea ejecutada con exito',
        'type': TYPE_SUCCESS
    },
    'L-0231': {
        'class_name': 'TaskManager',
        'method_name': 'create_model_training_task',
        'main_text': 'Generando tarea de entrenamiento de modelo...',
        'type': TYPE_INFO
    },
    'L-0232': {
        'class_name': 'TaskManager',
        'method_name': 'create_model_training_task',
        'main_text': 'Tarea creada exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0233': {
        'class_name': 'TaskManager',
        'method_name': 'create_text_analysis_task',
        'main_text': 'Generando tarea de análisis de texto...',
        'type': TYPE_INFO
    },
    'L-0234': {
        'class_name': 'TaskManager',
        'method_name': 'create_text_analysis_task',
        'main_text': 'Tarea creada exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0235': {
        'class_name': 'TaskManager',
        'method_name': 'update',
        'main_text': 'Actualizando estado de administrador de tareas...',
        'type': TYPE_INFO
    },
    'L-0236': {
        'class_name': 'TaskManager',
        'method_name': 'update',
        'main_text': 'No hay ninguna tarea en cola',
        'type': TYPE_WRN
    },
    'L-0237': {
        'class_name': 'TaskManager',
        'method_name': 'update',
        'main_text': 'Evaluando inicialización de tarea %s...',
        'type': TYPE_INFO
    },
    'L-0238': {
        'class_name': 'TaskManager',
        'method_name': 'update',
        'main_text': 'Estado del administrador de tareas actualizado exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0239': {
        'class_name': 'TaskManager',
        'method_name': 'abort_task',
        'main_text': 'Intentando abortar tarea %s...',
        'type': TYPE_INFO
    },
    'L-0240': {
        'class_name': 'TaskManager',
        'method_name': 'abort_task',
        'main_text': 'La tarea no se encuentra entre las tareas activas',
        'type': TYPE_ERR
    },
    'L-0241': {
        'class_name': 'TaskManager',
        'method_name': 'abort_task',
        'main_text': 'Tarea abortada exitosamente',
        'type': TYPE_SUCCESS
    },
    'L-0242': {
        'class_name': 'TaskManager',
        'method_name': 'abort_task',
        'main_text': 'La tarea ya se encuentra en ejecución',
        'type': TYPE_WRN
    },
}
