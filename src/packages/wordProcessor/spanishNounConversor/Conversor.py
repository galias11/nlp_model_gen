# @Vendors
import fnmatch

# [WIP] Esta clase cumple la función de recibir un sustantivo y devolver su plurar
class Conversor:
    def __init__(self, general_configs):
        self.configs = {
            'noun_groups': general_configs['groups'],
            'exceptions': general_configs['exceptions']
        }

    def set_config_theme(self, general_configs):
        self.configs = {
            'noun_groups': general_configs['groups'],
            'exceptions': general_configs['exceptions']
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
            if not word in self.configs['exceptions']:
                founded = False
                for group in self.configs['noun_groups']:
                    if any(fnmatch.fnmatch(word, suffix) for suffix in group['suffixes']):
                        line += word + group['replacement']
                        founded = True
                if not founded:
                    line += word
            else:
                line += word
        if line == noun:
            return ''
        return line
