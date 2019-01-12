# Recibe un verbo y devuelve su conjugación en imperativo (variante argentina I).
# <verb> verbo a conjugar debe ser una cadena de caracteres terminada en
# uno de {ar, er, ir, ár, ér, ír}. De no ser asi devuelve un vector vacio.
# <force_conj>: valor booleano. Si es verdadero fuerza a que el verbo
# sea conjugado por la función sin recurrir al diccionario de irregulares
# (aún si el mismo se encontrase allí)

# @Vendors
import fnmatch

# @Utils
from src.utils.fileUtils import loadDictFromJSONFile

# @Config
irregularVerbData = loadDictFromJSONFile('wordProcessor-verbIrregularGroups')
config = loadDictFromJSONFile('wordProcessor-verbConfig')

def imperativo_B_conj(verb, force_conj, mode, irregular_verbs):
    if not any(fnmatch.fnmatch(verb, suffix) for suffix in ['*ar', '*er', '*ir', '*ár', '*ér', '*ír']):
        return ['','','','','','']
    verb_conj = []
    suffix_conj = []
    base_verb = verb[0:len(verb)-2]
    if not verb in irregular_verbs.keys() or force_conj:
        if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
            suffix_conj = ['ame', 'ate', 'ale', 'anos', 'aleis', 'ales']
        if fnmatch.fnmatch(verb, '*er') or fnmatch.fnmatch(verb, '*ér'):
            suffix_conj = ['eme', 'ete', 'ele', 'enos', 'eleis', 'eles']
        if fnmatch.fnmatch(verb, '*ir') or fnmatch.fnmatch(verb, '*ír'):
            suffix_conj = ['ime', 'ite', 'ile', 'inos', 'ileis', 'iles']
    else:
        return irregular_verbs[verb]['impB']
    for suffix in suffix_conj:
        verb_conj.append(base_verb + suffix)
    return verb_conj
