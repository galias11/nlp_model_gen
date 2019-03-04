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
        'method_name': '__init__',
        'main_text': 'Inicializando modulo de administración...',
        'type': TYPE_INFO
    },
    'L-0037': {
        'class_name': 'AdminModuleController',
        'method_name': '__init__',
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
    }
}
