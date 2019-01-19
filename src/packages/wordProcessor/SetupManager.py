# @Utils
from src.utils.fileUtils import loadDictFromJSONFile
from src.utils.objectUtils import get_elements_from_dict

# @Asseta
conjugator_config = loadDictFromJSONFile('wordProcessor-verbConfig')
conjugator_irregular_exceptions = loadDictFromJSONFile('wordProcessor-verbIrregularExceptions')
conjugator_irregular_groups = loadDictFromJSONFile('wordProcessor-verbIrregularGroups')
noun_conversor_groups = loadDictFromJSONFile('wordProcessor-nounGroups')
noun_conversor_plural_exceptions = loadDictFromJSONFile('wordProcessor-nounPluralExceptions')
fuzzy_generator_config = loadDictFromJSONFile('wordProcessor-fuzzyTermsConfig')

class WordProcessorSetupManager:
    def __init__(self):
        self.conjugator_cfg_theme = conjugator_config['selectedTheme']
        self.noun_conversor_cfg_theme = conjugator_config['selectedTheme']
        self.fuzzy_generator_cfg_theme = conjugator_config['selectedTheme']

    def get_conjugator_available_configs(self):
        return get_elements_from_dict(conjugator_config, ['selectedTheme'])

    def get_conjugator_available_exceptions(self):
        return get_elements_from_dict(conjugator_irregular_exceptions, ['selectedTheme'])

    def get_conjugator_available_irr_groups(self):
        return get_elements_from_dict(conjugator_irregular_groups, ['selectedTheme'])

    def get_noun_conversor_available_groups(self):
        return get_elements_from_dict(noun_conversor_groups, ['selectedTheme'])

    def get_noun_conversor_plural_available_exceptions(self):
        return get_elements_from_dict(noun_conversor_plural_exceptions, ['selectedTheme'])

    def get_fuzzy_gen_available_configs(self):
        return get_elements_from_dict(fuzzy_generator_config, ['selectedTheme'])
