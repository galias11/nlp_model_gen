DB_CONNECTION_TIMEOUT = 3000
DB_OPERATION_DELETE = 'delete'
DB_OPERATION_INSERT = 'insert'
DB_OPERATION_INSERT_MANY = 'insert_many'
DB_OPERATION_UPDATE = 'update'
DB_SERVER_URL = 'mongodb://localhost:27017/'
PATH_SEPARATOR = '-'
WORD_PROCESSOR_CONFIG_DB = 'word_processor_config'
WORD_PROCESSOR_CONJ_CFG_COLLECTION = 'wp_conjugator_config'
WORD_PROCESSOR_FUZZY_GEN_CFG_COLLECTION = 'wp_fuzzy_gen_config'
WORD_PROCESSOR_GENERAL_SETTING_COLLECTION = 'wp_general_settings'
WORD_PROCESSOR_NOUN_CONV_CFG_COLLECTION = 'wp_noun_conv_config'
WORD_PROCESSOR_VERB_EXCEPTIONS_COLLECTION = 'wp_conjugator_verb_exceptions'
WORD_PROCESSOR_VERB_GROUPS_COLLECTION = 'wp_conjugator_verb_groups'
WORD_PROCESOR_DEFAULT_MODE = 0
WORD_PROCESSOR_DEFAULT_THEME = 'default'
WORD_PROCESOR_RESERVED_THEME = 'selected_theme'
WORD_PROCESSOR_SCHEMAS = {
    'CONJ_GENERAL_CFG': 'conjugator_general_config_schema',
    'CONJ_IRR_GROUPS': 'conjugator_verb_groups_schema ',
    'CONJ_EXCEPTIONS': 'conjugator_verb_exceptions_schema',
    'FUZZY_GENERAL_CFG': 'fuzzy_genetator_config_schema',
    'NOUN_CONV_GENERAL_CFG': 'noun_conversor_config_schema'
}
WORD_PROCESSOR_DEFAULT_CFG_OBJECT = {
    'conjugator_active_theme': 'default',
    'fuzzy_gen_active_theme': 'default',
    'noun_conversor_active_theme': 'default'
}
