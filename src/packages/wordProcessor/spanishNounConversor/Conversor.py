# @Vendors
import fnmatch

# @Utils
from src.utils.fileUtils import loadDictFromJSONFile

# @Assets
nounGroups = loadDictFromJSONFile('wordProcessor-nounGroups')
pluralExceptions = loadDictFromJSONFile('wordProcessor-nounPluralExceptions')

# [WIP] Esta clase cumple la función de recibir un sustantivo y devolver su plurar
class Conversor:
    def __init__(self):
        pass

    def a_plural(self, noun):
        words = noun.split()
        line = ''
        first_flag = True
        for word in words:
            if first_flag:
                first_flag = False
            else:
                line += ' '
            if not word in pluralExceptions:
                if any(fnmatch.fnmatch(word, suffix) for suffix in nounGroups['grupo_01']):
                    line += word + 's'
                elif any(fnmatch.fnmatch(word, suffix) for suffix in nounGroups['grupo_02']):
                    line += word + 'es'
                elif any(fnmatch.fnmatch(word, suffix) for suffix in nounGroups['grupo_03']):
                    line += word + 'es'
                elif any(fnmatch.fnmatch(word, suffix) for suffix in nounGroups['grupo_04']):
                    line += word
                elif any(fnmatch.fnmatch(word, suffix) for suffix in nounGroups['grupo_05']):
                    line += word[:len(word)-1] + 'ces'
                else:
                    line += word
            else:
                line += word
        if line == noun:
            return ''
        return line
