# @Vendors
import fnmatch

# @Utils
from src.utils.fileUtils import load_dict_from_json

# @Constants
from src.constants.constants import (WORD_PROCESOR_DEFAULT_THEME, WORD_PROCESOR_RESERVED_THEME)

# @Assets
noun_groups = load_dict_from_json('wordProcessor-nounGroups')
plural_exceptions = load_dict_from_json('wordProcessor-nounPluralExceptions')

# [WIP] Esta clase cumple la función de recibir un sustantivo y devolver su plurar
class Conversor:
    def __init__(self, config_theme=WORD_PROCESOR_DEFAULT_THEME):
        self.config_theme = config_theme if config_theme in noun_groups.keys() and config_theme is not WORD_PROCESOR_RESERVED_THEME else WORD_PROCESOR_DEFAULT_THEME
        self.configs = {
            'noun_groups': noun_groups[self.config_theme],
            'plural_exceptions': plural_exceptions[self.config_theme]
        }

    def set_config_theme(self, config_theme):
        if config_theme in noun_groups.keys() and config_theme is not WORD_PROCESOR_RESERVED_THEME:
            self.config_theme = config_theme
            self.configs = {
                'noun_groups': noun_groups[self.config_theme],
                'plural_exceptions': plural_exceptions[self.config_theme]
            }

    def a_plural(self, noun):
        words = noun.split()
        line = ''
        first_flag = True
        for word in words:
            if first_flag:
                first_flag = False
            else:
                line += ' '
            if not word in self.configs['plural_exceptions']:
                if any(fnmatch.fnmatch(word, suffix) for suffix in self.configs['noun_groups']['grupo_01']):
                    line += word + 's'
                elif any(fnmatch.fnmatch(word, suffix) for suffix in self.configs['noun_groups']['grupo_02']):
                    line += word + 'es'
                elif any(fnmatch.fnmatch(word, suffix) for suffix in self.configs['noun_groups']['grupo_03']):
                    line += word + 'es'
                elif any(fnmatch.fnmatch(word, suffix) for suffix in self.configs['noun_groups']['grupo_04']):
                    line += word
                elif any(fnmatch.fnmatch(word, suffix) for suffix in self.configs['noun_groups']['grupo_05']):
                    line += word[:len(word)-1] + 'ces'
                else:
                    line += word
            else:
                line += word
        if line == noun:
            return ''
        return line
