# Recibe un verbo y devuelve su conjugación en condicional indicativo.
# <verb> verbo a conjugar debe ser una cadena de caracteres terminada en
# uno de {ar, er, ir, ár, ér, ír}. De no ser asi devuelve un vector vacio.
# <force_conj>: valor booleano. Si es verdadero fuerza a que el verbo
# sea conjugado por la función sin recurrir al diccionario de irregulares
# (aún si el mismo se encontrase allí)

# @Vendors
import fnmatch

# @Utils
from src.utils.fileUtils import loadDictFromJSONFile

# @Helpers
from .irregularVerbCastHelper import irregular_cast_group_13_b

# @Config
irregularVerbData = loadDictFromJSONFile('wordProcessor-verbIrregularGroups')
config = loadDictFromJSONFile('wordProcessor-verbConfig')

def condicional_simple_A_conj(verb, force_conj, mode, irregular_verbs):
    if not any(fnmatch.fnmatch(verb, suffix) for suffix in ['*ar', '*er', '*ir', '*ár', '*ér', '*ír']):
        return ['','','','','','']
    verb_conj = []
    suffix_conj = []
    if fnmatch.fnmatch(verb, '*hacer'):
        verb = verb.replace('hacer', 'hacar')
    base_verb = verb[0:len(verb)-2]
    if not verb in irregular_verbs.keys() or force_conj:
        if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
            suffix_conj = ['aría', 'arías', 'aría', 'aríamos', 'aríais', 'arían']
        if fnmatch.fnmatch(verb, '*er') or fnmatch.fnmatch(verb, '*ér'):
            suffix_conj = ['ería', 'erías', 'ería', 'eríamos', 'eríais', 'erían']
        if fnmatch.fnmatch(verb, '*ir') or fnmatch.fnmatch(verb, '*ír'):
            suffix_conj = ['iría', 'irías', 'iría', 'iríamos', 'iríais', 'irían']
    else:
        return irregular_verbs[verb]['condA']
    for suffix in suffix_conj:
        if  fnmatch.fnmatch(verb, '*decir'):
            base_form = base_verb.replace('dec', 'd')
        elif fnmatch.fnmatch(verb, '*hacar'):
            base_form = base_verb.replace('hac', 'h')
        else:
            base_form = base_verb

        # Mofifica el verbo base para los verbos en el grupo 13
        # base_verb + d
        base_form = irregular_cast_group_13_b(verb, base_form)

        # Elimina la i que resulta en un sobrante para los verbos del
        # grupo 13
        if verb in irregularVerbData['irregular_verbs_grupo_13_alir'] or verb in irregularVerbData['irregular_verbs_grupo_13_aler']:
            suffix = suffix[1:]

        verb_conj.append(base_form + suffix)
    return verb_conj
