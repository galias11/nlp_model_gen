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
}
