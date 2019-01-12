# @Utils
from src.utils.fileUtils import loadDictFromJSONFile
from src.utils.objectUtils import fillDict

# @Helpers
from .presenteIndicativoHelper import presente_conj
from .preteritoPerfSimpleHelper import preterito_perf_simple_conj
from .preteritoImperfHelper import preterito_imperf_conj
from .futuroSimpleHelper import futuro_simple_conj
from .condicionalSimpleAHelper import condicional_simple_A_conj
from .condicionalSimpleBHelper import condicional_simple_B_conj
from .imperativoAHelper import imperativo_A_conj
from .imperativoBHelper import imperativo_B_conj
from .imperativoCHelper import imperativo_C_conj
from .participioHelper import participio
from .gerundioHelper import gerundio

# @Assets
irregularVerbExceptions = loadDictFromJSONFile('wordProcessor-verbIrregularExceptions')

# Recibe un verbo y las excepciones en sus conjugaciones. En los casos en los que 
# no existe una excepción se utilizaran los helpers para cada tiempo de conjugación.
def get_irregular_verb_template(verb, irregularDict, mode, verb_options):
    ger, part, pres, pret_perf, pret_imperf, fut, impA, impB, impC, condA, condB, alternatives = fillDict(verb_options, ['ger', 'part', 'pres', 'pret_perf', 'pret_imperf', 'fut', 'impA', 'impB', 'impC', 'condA', 'condB', 'alternatives'])
    template = {
        'inf': [verb],
        'ger' : ger if ger is not None else gerundio(verb, True, mode, irregularDict),
        'part': part if part is not None else participio(verb, True, mode, irregularDict),
        'pres': pres if pres is not None else presente_conj(verb, True, mode, irregularDict),
        'pret_perf': pret_perf if pret_perf is not None else preterito_perf_simple_conj(verb, True, mode, irregularDict),
        'pret_imperf': pret_imperf if pret_imperf is not None else preterito_imperf_conj(verb, True, mode, irregularDict),
        'fut': fut if fut is not None else futuro_simple_conj(verb, True, mode, irregularDict),
        'impA': impA if impA is not None else imperativo_A_conj(verb, True, mode, irregularDict),
        'impB': impB if impB is not None else imperativo_B_conj(verb, True, mode, irregularDict),
        'impC': impC if impC is not None else imperativo_C_conj(verb, True, mode, irregularDict),
        'condA': condA if condA is not None else condicional_simple_A_conj(verb, True, mode, irregularDict),
        'condB': condB if condB is not None else condicional_simple_B_conj(verb, True, mode, irregularDict),
    }
    if mode == 0 and alternatives is not None:
        for alternative in alternatives:
            template[alternative['key']][alternative['person']] = alternative['value']
    irregularDict[verb] = template

# Este modulo se utiliza para generar los casos excepcionales de verbos irregulares.
def get_irregular_verbs(irregularDict, mode):
    for verbException in irregularVerbExceptions:
        get_irregular_verb_template(verbException['key'], irregularDict, mode, verbException['exceptions'])
