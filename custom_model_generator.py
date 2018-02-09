# TODO:
# - Crear una clase que englobe la generación de las reglas para el tokenizer.
# Esto implica:
# --> La clase debe aceptar listas de terminos etiquetados por una categoria
# (que se diferencia dentro del ambito del modelo a generar) --> OK
# --> Los términos antes mencionados deberían poder diferenciarse en verbos y
# sustantivos, de modo de que el tratamiento sea distinto para ellos. --> OK
# --> Para los verbos se debe obtener la conjugación a diferenctes tiempos
# verbales (utilizar esp_verb_conjugator de este mismo proyecto) --> OK
# --> Tanto para los verbos (ya conjugados) como para los sustantivos
# se debe generar deformaciones que tengan como máximo una distancia de
# demerau-levenshtein de 2 --> OK
# --> Para dichas deformaciones generar archivos que enlisten las nuevas reglas
# en un formato compatible con el tokenizer de spacy --> OK
# --> Se debe poder anexar estas reglas al tokenizer de un modelo dado, y generar
# un nuevo modelo que se guarde a disco.--> OK

import spacy
from spacy.symbols import ORTH, LEMMA, POS, TAG, SHAPE
from spacy.tokens import Doc, Span, Token
import ast
import os
from os import scandir, getcwd
from os.path import abspath
from collections import Counter
import fnmatch
from .esp_conjugator import Conjugator
from .esp_conjugator import Noun_modifier
from termcolor import colored, cprint
import importlib.util
import sys


DIC_PATH = "/home/infolab/Documentos/SAVE/Dictionaries/dictionary-es_A/"

# Implementación de la función de demerau_levenshtein. Calcula dicha distancia
# entre dos cadenas.
# <s1> Cadena 1 (sin restricciones)
# <s2> Cadena 2 (sin restricciones)
# <return> valor numérico entero que representa la distancia entre estas dos
# cadenas.
def damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1,lenstr1+1):
        d[(i,-1)] = i+1
    for j in range(-1,lenstr2+1):
        d[(-1,j)] = j+1

    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i,j)] = min(
                           d[(i-1,j)] + 1, # deletion
                           d[(i,j-1)] + 1, # insertion
                           d[(i-1,j-1)] + cost, # substitution
                          )
            if i and j and s1[i]==s2[j-1] and s1[i-1] == s2[j]:
                d[(i,j)] = min (d[(i,j)], d[i-2,j-2] + cost) # transposition

    return d[lenstr1-1,lenstr2-1]


class Tokenizer_rules_generator:
    windows_mode = False

    cat_types = ['verb', 'noun']

    categories = {}

    generated_model = None

    def __init__(self, default_tmp_path, demerau_levenshtein_max_dist=0, windows_mode=False):
        self.windows_mode = windows_mode
        self.default_path = default_tmp_path
        self.demerau_levenshtein_max_dist = demerau_levenshtein_max_dist

        try:
            os.stat(default_tmp_path)
        except:
            os.mkdir(default_tmp_path)


    def add_category(self, cat_name, cat_type, detection_msg='', word_dict=[], search_dist=0):
        if cat_type + '_' + cat_name in self.categories.keys():
            print('ERROR: La categoría ya existe')
            return

        if not cat_type in self.cat_types:
            print('ERROR: Tipo inexistente. Disponibles: verb, noun/adj')
            returncust

        new_category = {
            'name' : cat_name,
            'type' : cat_type,
            'default_dir' : cat_type + '__' + cat_name,
            'dictionary' : word_dict,
            'search_dist' : search_dist,
            'detection_msg' : detection_msg
        }

        self.categories[cat_type + '_' + cat_name] = new_category

    def create_spacy_model(self, base_model):
        self.generate_verb_rules()

        self.generate_noun_rules()

        print('Cargando tokenizer del modelo base...', end=' ')
        nlp = spacy.load(base_model)

        tokenizer = nlp.tokenizer
        print('OK')

        print('Agregando nuevas reglas...', end=' ')
        self.add_changed_word_model(tokenizer, self.default_path)
        print('OK')

        generated_model = nlp

        print('Generando archivo de personalización de filtros...', end='')
        self.generate_search_functions_file()
        print('OK')

        print('Guardando nuevo modelo...', end=' ')
        nlp.to_disk(self.default_path + self.path_separator() + 'spacy_model')
        print('OK')

    def load_custom_model(self, path):
        print('Cargando modelo...', end='')
        nlp = spacy.load(path + self.path_separator() + 'spacy_model')
        print('OK')

        print('Cargando funciones de busqueda...', end='')

        sys.path.append(path)

        import search_function_load_file

        exec('search_function_load_file.load_search_functions()')

        print('OK')


        return nlp

    def generate_search_functions_file(self):

        search_targets = []
        for cat in self.categories:
            category = self.categories[cat]
            if category['type'] == 'noun':
                for topic in category['dictionary']:
                    search_targets.append({category['name'] + '_' + topic[0]:[topic[1], category['detection_msg'] + ' - ' + topic[0]]})
            else:
                search_targets.append({category['name'] + '_acto':[category['dictionary'], category['detection_msg']]})

        arch = open(self.default_path + self.path_separator() + '__init__.py', 'w')
        arch.write('from .search_function_load_file import *')
        arch.close()

        arch = open(self.default_path + self.path_separator() + 'search_function_load_file.py', 'w')

        arch.write('from spacy.tokens import Doc, Span, Token\n\n')
        arch.write('def load_search_functions():\n')

        for target in search_targets:
            target_key = next(iter(target))
            is_key = 'is_' + target_key
            has_key = 'has_' + target_key
            is_key_quoted = '\'is_' + target_key + '\''
            has_key_quoted = '\'has_' + target_key + '\''
            is_getter_key = 'is_' + target_key + '_getter'
            has_getter_key = 'has_' + target_key + '_getter'
            search_list = target_key + '_dict'
            exec_string = '\t' + search_list + ' = ' + str(target[target_key][0]) + '\n'
            exec_string += '\t' + is_getter_key + ' = lambda token: token.lemma_ in ' + search_list + '\n'
            exec_string += '\t' + 'Token.set_extension(' + is_key_quoted + ', getter=' + is_getter_key + ') \n'
            exec_string += '\t' + has_getter_key + '= lambda obj: any([t._.' + is_key + ' for t in obj]) \n'
            exec_string += '\t' + 'Doc.set_extension(' + has_key_quoted + ', getter=' + has_getter_key + ') \n'
            exec_string += '\t' + 'Span.set_extension(' + has_key_quoted + ', getter=' + has_getter_key + ') \n'
            arch.write(exec_string)
            arch.write('')

        arch.close()



    # Genera las conjugaciones para cada categoria del tipo verbo almacenada
    # junto con un diccionario de la misma.
    def generate_verb_rules(self):

        for key in self.categories.keys():
            if self.categories[key]['type'] == 'verb':

                print('Generando archivos temporales de modelo para categoria ' + colored(self.categories[key]['name'], 'green') + '...')

                category_path = self.default_path + self.path_separator() + self.categories[key]['default_dir']
                self.create_dir_if_not_exist(category_path)

                print('Generando archivos temporales...')

                for verb in self.categories[key]['dictionary']:

                    verb_path = category_path + self.path_separator() + verb
                    self.create_dir_if_not_exist(verb_path)

                    self.gen_lote_reglas_verbos_completo(verb, self.demerau_levenshtein_max_dist, verb_path)

                print('Temporales generados')

                print('Generando diccionario para categoria ' + colored(self.categories[key]['name'], 'green') + '...', end='')
                self.dictionary_to_disk(category_path + self.path_separator() + 'dictionary.dict', self.categories[key]['dictionary'])
                print('OK')

                print('---> Archivos temporales de modelo generados.')


    def generate_noun_rules(self):

        for key in self.categories.keys():
            if self.categories[key]['type'] == 'noun':

                print('Generando archivos temporales de modelo para categoria ' + colored(self.categories[key]['name'], 'green') + '...')

                category_path = self.default_path + self.path_separator() + self.categories[key]['default_dir']
                self.create_dir_if_not_exist(category_path)

                print('Generando archivos temporales...')

                for noun_cat in self.categories[key]['dictionary']:
                    noun_group = noun_cat[0]
                    noun_path = category_path + self.path_separator() + noun_group

                    self.create_dir_if_not_exist(noun_path)


                    for noun in noun_cat[1]:
                        self.gen_lote_reglas_sustantivos_completo(noun, self.demerau_levenshtein_max_dist, noun_path)

                    print('Generando diccionario para subcategoria ' + colored(noun_group, 'green') + '...', end='')

                    self.dictionary_to_disk(category_path + self.path_separator() + 'dictionary_' + noun_group + '.dict', noun_cat[1])

                    print('OK')

                print('Temporales generados')

                print('---> Archivos temporales de modelo generados.')

    def dictionary_to_disk(self, path, dictionary):
        arch = open(path, 'w')
        arch.write(str(dictionary))
        arch.close()

    def create_dir_if_not_exist(self, path):
        try:
            os.stat(path)
        except:
            os.mkdir(path)

    def path_separator(self):
        if self.windows_mode:
            path_split_token = '\\'
        else:
            path_split_token = '/'
        return path_split_token

    # Extrae un diccionario de un archivo y genera a partir de cada elemento del mismo
    # un archivo que contiene las deformaciones para dicho termino.
    def dictionary_token_selector(self, dict_file, pos, tag, output_path, max_dist):
        dictionary = self.extract_dict_from_file(dict_file)
        for token in dictionary:
            self.token_selector(token, token, pos, tag, output_path + token + ".rl", max_dist)


    def extract_dict_from_file(self, file_path):
        arch = open(file_path, "r").read().replace("\'", "\"")
        return ast.literal_eval(arch)


    # add_rules_to_tokenizer()
    # ***************************************************************************************
    # Agrega a un determinado tokenizer las reglas adicionales para determinados tokens
    # especificadas en un archivo.
    # -> input:
    #   <tokenizer>: Se trata de un tokenizer correspondiente a un nlp de spaCy. La sintaxis
    #   estándar para obtener el tokenizer es:
    #   cargar modelo de spaCy --> <spaCy model>.tokenizer
    #   <file_name>: Nombre de archivo de un archivo de reglas para reconocimiento de token.
    #   Es recomendable que solo se usen los archivos generados como output de la función
    #   token_selector.
    # -> output:
    #   El tokenizer pasado como parametro se actualizar con las reglas especificadas
    #   en el archivo.
    def add_rules_to_tokenizer(self, tokenizer, file_name):
        print('Agregando archivo ' + colored(file_name, 'green') + '...', end=' ')
        for token in ast.literal_eval(open(file_name, "r").read()):
            for key in token:
                tokenizer.add_special_case(key, token[key])
        print('OK')


    def add_changed_word_model(self, tokenizer, path):
        for arch in scandir(path):
            if arch.is_dir():
                self.add_changed_word_model(tokenizer, abspath(arch.path))
            elif fnmatch.fnmatch(arch.name, '*.rl'):
                self.add_rules_to_tokenizer(tokenizer, abspath(arch.path))


    def gen_lote_reglas_sustantivos_completo(self, singular, max_dist, output_dir):
        if not fnmatch.fnmatch(output_dir, '*/') and not self.windows_mode:
            output_dir += '/'
        elif self.windows_mode:
            output_dir += '\\'

        modifier = Noun_modifier()
        plural = modifier.a_plural(singular)

        print('Generando entradas para el sustantivo ', colored(singular, 'green'), end=' ')
        self.gen_lote_reglas_sustantivo(singular, plural, singular, output_dir, max_dist)
        print('OK')



    def gen_lote_reglas_sustantivo(self, singular, plural, lemma, path, max_dist):
        singular_conj = "self.token_selector(\"" + singular + "\",\"" + lemma + "\",\"NOUN\",\"NOUN_BASE_SING\",\"" + path + singular + ".rl\", " + str(max_dist) + ")"
        eval(singular_conj)
        if not (plural == '' or plural == singular):
            plural_conj = "self.token_selector(\"" + plural + "\",\"" + lemma + "\",\"NOUN\",\"NOUN_BASE_PLUR\",\"" + path + plural + ".rl\", " + str(max_dist) + ")"
            eval(plural_conj)



    # gen_lote_reglas_verbo_completo()
    # ******************************************************************************
    # Recibe un verbo en infinitivo, una distancia de demerau-levenshtein máxima y
    # un directorio de output. A partir del verbo recibido genera las conjugaciones
    # posibles utilizando esp_verb_conjugator y llama a token_selector para que lo
    # deforme y lo guarde a disco en el directorio de output seleccionado.
    #  -> input:
    #   <Infinitivo> Verbo en infinitivo que debe ser conjugado. Debe ser una
    #   cadena de caracteres terminada en uno de {'*ar', '*er', '*ir', '*ár',
    #   '*ér', '*ír'}
    #   <max_dist> Distancia de demerau_levenshtein máxima que se admite en las
    #   deformaciones.
    #   <output_dir> Directorio donde se guardarán los archivos de reglas. Debe
    #   ser una cadena de caracteres que contenga una ruta válida a un directorio.
    #   <mode> Valor entero, determina el modo del conjugador, con el parametro
    #   en 0, se activa el modo 'vos' para la segunda persona singular. En otro,
    #   caso esta desactivado.
    #  -> output:
    #   ... : Un archivo por cada conjugación conteniendo las variantes en la
    #  escritura para cada uno.
    def gen_lote_reglas_verbos_completo(self, infinitive, max_dist, output_dir):
        conj = Conjugator(0)

        if not any(fnmatch.fnmatch(infinitive, suffix) for suffix in ['*ar', '*er', '*ir', '*ár', '*ér', '*ír']):
            print("Error: verbo infinitivo no válido.")
            return

        print("Generando lote de reglas para verbo " + colored(infinitive, 'green') + "...")

        print("Generando conjugaciones...", end='')

        if not fnmatch.fnmatch(output_dir, '*/') and not self.windows_mode:
            output_dir += '/'
        elif self.windows_mode:
            output_dir += '\\'

        conj_dict = conj.generar_diccionario_conjugacion(infinitive)

        print("OK")

        self.token_selector(conj_dict['inf'][0], conj_dict['inf'][0], 'VERB', 'VERB_INF', output_dir + conj_dict['inf'][0] + ".rl", max_dist)

        self.token_selector(conj_dict['ger'][0], conj_dict['inf'][0], 'VERB', 'VERB_GER', output_dir + conj_dict['ger'][0] + ".rl", max_dist)

        self.token_selector(conj_dict['part'][0], conj_dict['inf'][0], 'VERB', 'VERB_PART_MASC', output_dir + conj_dict['part'][0] + ".rl", max_dist)
        self.token_selector(conj_dict['part'][1], conj_dict['inf'][0], 'VERB', 'VERB_PART_FEM', output_dir + conj_dict['part'][1] + ".rl", max_dist)
        self.token_selector(conj_dict['part'][2], conj_dict['inf'][0], 'VERB', 'VERB_PART_MASC', output_dir + conj_dict['part'][2] + ".rl", max_dist)

        self.gen_lote_reglas(conj_dict['pres'][0], conj_dict['pres'][1], conj_dict['pres'][2], conj_dict['pres'][3], conj_dict['pres'][4], conj_dict['pres'][5], infinitive, 'PRES', output_dir, max_dist)

        self.gen_lote_reglas(conj_dict['pret_perf'][0], conj_dict['pret_perf'][1], conj_dict['pret_perf'][2], conj_dict['pret_perf'][3], conj_dict['pret_perf'][4], conj_dict['pret_perf'][5], infinitive, 'PAST', output_dir, max_dist)

        self.gen_lote_reglas(conj_dict['pret_imperf'][0], conj_dict['pret_imperf'][1], conj_dict['pret_imperf'][2], conj_dict['pret_imperf'][3], conj_dict['pret_imperf'][4], conj_dict['pret_imperf'][5], infinitive, 'PAST', output_dir, max_dist)

        self.gen_lote_reglas(conj_dict['fut'][0], conj_dict['fut'][1], conj_dict['fut'][2], conj_dict['fut'][3], conj_dict['fut'][4], conj_dict['fut'][5], infinitive, 'FUT', output_dir, max_dist)

        self.gen_lote_reglas(conj_dict['impA'][0], conj_dict['impA'][1], conj_dict['impA'][2], conj_dict['impA'][3], conj_dict['impA'][4], conj_dict['impA'][5], infinitive, 'IMP', output_dir, max_dist)

        self.gen_lote_reglas(conj_dict['impB'][0], conj_dict['impB'][1], conj_dict['impB'][2], conj_dict['impB'][3], conj_dict['impB'][4], conj_dict['impB'][5], infinitive, 'IMP', output_dir, max_dist)

        self.gen_lote_reglas(conj_dict['impC'][0], conj_dict['impC'][1], conj_dict['impC'][2], conj_dict['impC'][3], conj_dict['impC'][4], conj_dict['impC'][5], infinitive, 'IMP', output_dir, max_dist)

        self.gen_lote_reglas(conj_dict['condA'][0], conj_dict['condA'][1], conj_dict['condA'][2], conj_dict['condA'][3], conj_dict['condA'][4], conj_dict['condA'][5], infinitive, 'COND', output_dir, max_dist)

        self.gen_lote_reglas(conj_dict['condB'][0], conj_dict['condB'][1], conj_dict['condB'][2], conj_dict['condB'][3], conj_dict['condB'][4], conj_dict['condB'][5], infinitive, 'SIMP', output_dir, max_dist)

        print("Lote de reglas generado.")


    # gen_lote_reglas()
    # ***************************************************************************************
    # Genera un lote completo de archivos de reglas para excepciones. Cada archivos
    # contiene variantes de la conjugación para cada persona de un verbo en un
    # determinado tiempo.
    #  -> input:
    #   <yo> Verbo conjugado para primera persona singular, escrito correctamente.
    #   <tu> Verbo conjugado para segunda persona singular, escrito correctamente.
    #   <el> Verbo conjugado para tercera persona singular, escrito correctamente.
    #   <nos> Verbo conjugado para primera persona plural, escrito correctamento.
    #   <vos> Verbo conjugado para segunda persona plural, escrito correctamento.
    #   <ellos> Verbo conjugado para tercera persona plural, escrito correctamente.
    #   <lemma> Verbo en infinitivo.
    #   <tiempo> Tiempo verbal. Uno de: {PRES, PAST, FUT}
    #   <path> Ruta de acceso al directorio del archivo a crear. Ej:
    #   "/home/user/.../"
    #   <max_dist> distancia de levenshtein máxima para que una variación de una palabra
    #   sea tomada como tal.
    #  -> output:
    #   ... : Un archivo por cada conjugación conteniendo las variantes en la
    #  escritura para cada uno.
    def gen_lote_reglas(self, yo, tu, el, nos, vos, ellos, lemma, tiempo, path, max_dist):
        if tiempo == 'IMP':
            yo_conj = "self.token_selector(\"" + yo + "\",\"" + lemma + "\",\"VERB\",\"VERB_PRES_1STPER_PLUR\",\"" + path + yo + ".rl\", " + str(max_dist) + ")"
        else:
            yo_conj = "self.token_selector(\"" + yo + "\",\"" + lemma + "\",\"VERB\",\"VERB_" + tiempo + "_1STPER_SING\",\"" + path + yo + ".rl\", " + str(max_dist) + ")"
        tu_conj = "self.token_selector(\"" + tu + "\",\"" + lemma + "\",\"VERB\",\"VERB_" + tiempo + "_2NDPER_SING\",\"" + path + tu + ".rl\", " + str(max_dist) + ")"
        el_conj = "self.token_selector(\"" + el + "\",\"" + lemma + "\",\"VERB\",\"VERB_" + tiempo + "_3RDPER_SING\",\"" + path + el + ".rl\", " + str(max_dist) + ")"
        nos_conj = "self.token_selector(\"" + nos + "\",\"" + lemma + "\",\"VERB\",\"VERB_" + tiempo + "_1STPER_PLUR\",\"" + path + nos + ".rl\", " + str(max_dist) + ")"
        vos_conj = "self.token_selector(\"" + vos + "\",\"" + lemma + "\",\"VERB\",\"VERB_" + tiempo + "_2NDPER_PLUR\",\"" + path + nos + ".rl\", " + str(max_dist) + ")"
        ellos_conj = "self.token_selector(\"" + ellos + "\",\"" + lemma + "\",\"VERB\",\"VERB_" + tiempo + "_3RDPER_SING\",\"" + path + ellos + ".rl\", " + str(max_dist) + ")"
        eval(yo_conj)
        eval(tu_conj)
        eval(el_conj)
        eval(nos_conj)
        eval(vos_conj)
        eval(ellos_conj)

    # token_selector()
    # ************************************************************************************
    # Genera una serie de entradas al tokenizer del procesador de lenguaje natural.
    # A partir de un token bien escrito genera diferentes variaciones de dicho token
    # y los muestra al usuario para que defina si dicha variaciòn puede ser tomada
    # como una forma válida.
    # -> Input:
    #   <token_text>: Forma "bien escrita" de la palabra a deformar.
    #   <lemma>: Forma base de la palabra (Ej. vende --> vender)
    #   <pos>: (Part of speech) Define la funciòn que tendra la palabra en el texto.
    #   (Ej. vender --> verbo)
    #   <tag>: Es el <pos> profundizado. Por el momento se dispone de tags limitados.
    #   Básicamente, extiende la descripción de la función del token en el documento.
    #   <max_dist> distancia de levenshtein máxima para que una variación de una palabra
    #   sea tomada como tal.
    # -> Output:
    #   Archivo (de texto plano) con una lista de la forma [<token_rule>]
    #   <token_rule> = {<token_text>, [{<variation_text>, <lemma>, <pos>, <tag>, <shape>}]}
    def token_selector(self, token, lemma, pos, tag, output_file, max_dist):
        generator = custom_token_generator(token, lemma, pos, custom_token_generator.TAG_KEY[tag], max_dist)
        arch = open(output_file, 'w')
        if max_dist == 0:
            arch.write(str(generator.no_variation_tokenizer_rule()))
        else:
            arch.write(str(generator.gen_tokenizer_rules()))
        arch.close()


# Class: custom_token_generator()
# ****************************************************************************************
# Esta clase sirve como generador de variaciones para un token. Recibe un token, su
# lemma, su pos (part of speech) y su tag. A partir de esto permite generar diferentes
# variaciones en su escritura.
class custom_token_generator:
    #TAGs de modos verbales (no incluye condicionales por ahora):
    TAG_KEY = {
    'VERB_INF' : "VERB__VerbForm=Inf",
    'VERB_GER' : "VERB__VerbForm=Ger",

    'VERB_PART_FEM' : "VERB__Gender=Fem|Number=Plur|Tense=Past|VerbForm=Part",
    'VERB_PART_MASC' : "VERB__Gender=Fem|Number=Sing|Tense=Past|VerbForm=Part",

    'VERB_COND_1STPER_PLUR' : "VERB__Mood=Cnd|Number=Plur|Person=1|VerbForm=Fin",
    'VERB_COND_3RDPER_PLUR' : "VERB__Mood=Cnd|Number=Plur|Person=3|VerbForm=Fin",
    'VERB_COND_1STPER_SING' : "VERB__Mood=Cnd|Number=Sing|Person=1|VerbForm=Fin",
    'VERB_COND_2NDPER_SING' : "VERB__Mood=Cnd|Number=Sing|Person=2|VerbForm=Fin",
    # Adicionado
    'VERB_COND_2NDPER_PLUR' : "VERB__Mood=Cnd|Number=Sing|Person=2|VerbForm=Fin",
    'VERB_COND_3RDPER_SING' : "VERB__Mood=Cnd|Number=Sing|Person=3|VerbForm=Fin",

    'VERB_IMP_1STPER_PLUR' : "VERB__Mood=Imp|Number=Plur|Person=1|VerbForm=Fin",
    'VERB_IMP_2NDPER_PLUR' : "VERB__Mood=Imp|Number=Plur|Person=2|VerbForm=Fin",
    'VERB_IMP_3RDPER_PLUR' : "VERB__Mood=Imp|Number=Plur|Person=3|VerbForm=Fin",
    'VERB_IMP_2NDPER_SING' : "VERB__Mood=Imp|Number=Sing|Person=2|VerbForm=Fin",
    'VERB_IMP_3RDPER_SING' : "VERB__Mood=Imp|Number=Sing|Person=3|VerbForm=Fin",
    'VERB_FUT_1STPER_PLUR' : "VERB__Mood=Ind|Number=Plur|Person=1|Tense=Fut|VerbForm=Fin",
    'VERB_PAST_1STPER_PLUR' : "VERB__Mood=Ind|Number=Plur|Person=1|Tense=Past|VerbForm=Fin",
    'VERB_PRES_1STPER_PLUR' : "VERB__Mood=Ind|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin",
    'VERB_PRES_2NDPER_PLUR' : "VERB__Mood=Ind|Number=Plur|Person=2|Tense=Pres|VerbForm=Fin",
    'VERB_PAST_2NDPER_PLUR' : "VERB__Mood=Ind|Number=Sing|Person=2|Tense=Past|VerbForm=Fin",
    'VERB_FUT_2NDPER_PLUR' : "VERB__Mood=Ind|Number=Sing|Person=2|Tense=Fut|VerbForm=Fin",
    'VERB_FUT_3RDPER_PLUR' : "VERB__Mood=Ind|Number=Plur|Person=3|Tense=Fut|VerbForm=Fin",
    'VERB_PAST_3RDPER_PLUR' : "VERB__Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin",
    'VERB_PRES_3RDPER_PLUR' : "VERB__Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin",
    'VERB_FUT_1STPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=1|Tense=Fut|VerbForm=Fin",
    'VERB_PAST_1STPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin",
    'VERB_PRES_1STPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin",
    'VERB_FUT_2NDPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=2|Tense=Fut|VerbForm=Fin",
    'VERB_PAST_2NDPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=2|Tense=Past|VerbForm=Fin",
    'VERB_PRES_2NDPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin",
    'VERB_FUT_3RDPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=3|Tense=Fut|VerbForm=Fin",
    'VERB_PAST_3RDPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin",
    'VERB_PRES_3RDPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",

    'VERB_SIMP_1STPER_PLUR' : "VERB__Mood=Sub|Number=Plur|Person=1|Tense=Imp|VerbForm=Fin",
    'VERB_SPRE_1STPER_PLUR' : "VERB__Mood=Sub|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin",
    # Adicionado
    'VERB_SIMP_2NDPER_PLUR' : "VERB__Mood=Sub|Number=Plur|Person=2|Tense=Pres|VerbForm=Fin",
    'VERB_SPRE_2NDPER_PLUR' : "VERB__Mood=Sub|Number=Plur|Person=2|Tense=Pres|VerbForm=Fin",
    'VERB_SIMP_3RDPER_PLUR' : "VERB__Mood=Sub|Number=Plur|Person=3|Tense=Imp|VerbForm=Fin",
    'VERB_SPRE_1STPER_PLUR' : "VERB__Mood=Sub|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin",
    'VERB_SIMP_1STPER_SING' : "VERB__Mood=Sub|Number=Sing|Person=1|Tense=Imp|VerbForm=Fin",
    'VERB_SPRE_1STPER_SING' : "VERB__Mood=Sub|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin",
    # Adicionado
    'VERB_SIMP_2NDPER_SING' : "VERB__Mood=Sub|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin",
    'VERB_SPRE_2NDPER_SING' : "VERB__Mood=Sub|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin",
    'VERB_SIMP_3RDPER_SING' : "VERB__Mood=Sub|Number=Sing|Person=3|Tense=Imp|VerbForm=Fin",
    'VERB_SPRE_3RDPER_SING' : "VERB__Mood=Sub|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",

    'NOUN_BASE' : "NOUN___",
    'NOUN_ADV_MORPH' : "NOUN__AdvType=Tim",
    'NOUN_ADV_MASC_SING' : "NOUN__AdvType=Tim|Gender=Masc|Number=Sing",
    'NOUN_FEM_BASE' : "NOUN__Gender=Fem",
    'NOUN_FEM_PLUR' : "NOUN__Gender=Fem|Number=Plur",
    'NOUN_FEM_SING' : "NOUN__Gender=Fem|Number=Sing",
    'NOUN_MASC_BASE' : "NOUN__Gender=Masc",
    'NOUN_MASC_PLUR' : "NOUN__Gender=Masc|Number=Plur",
    'NOUN_MASC_SING' : "NOUN__Gender=Masc|Number=Sing",
    'NOUN_VERBPART_MASC_PLUR' : "NOUN__Gender=Masc|Number=Sing|VerbForm=Part",
    'NOUN_BASE_PLUR' : "NOUN__Number=Plur",
    'NOUN_BASE_SING' : "NOUN__Number=Sing"}

    def __init__(self,token_text, token_lemma, token_pos, token_tag, min_dist):
        self.confuse_chars = {'v':['b'],'b':['v'],'n':['m'],'m':['n'],'c':['s', 'k', 'z'],
        's':['c','z'],'z':['s','c'],'q':['k'],'k':['q'],'qu':['k'],'k':['qu', 'c'],
        'll':['y'],'y':['ll','i'],'i':['y'],'á':['a', 'ha'], 'a': ['ha'], 'é':['e'],
        'e': ['he'], 'í':['i'],'ó':['o'],'ú':['u'], 'ha':['a'], 'he':['e'], 'hi':['i'],
        'ho':['o'], 'hu':['u']}

        self.token_lemma = token_lemma
        self.token_pos = token_pos
        self.token_tag = token_tag
        self.token_text = token_text
        self.min_dist = min_dist

    def no_variation_tokenizer_rule(self):
        return [{self.token_text:
        [{ORTH:self.token_text, LEMMA:self.token_lemma,
        POS:self.token_pos, TAG:self.token_tag,
        SHAPE:self.shape(self.token_text)}]}]

    def gen_tokenizer_rules(self):
        rules = []
        for variation in self.string_variations():
            rules.append({variation:
            [{ORTH:variation, LEMMA:self.token_lemma,
            POS:self.token_pos, TAG:self.token_tag,
            SHAPE:self.shape(variation)}]})
        return rules

    def string_variations(self):
        variations_list = set([])
        char_del = self.random_char_del()
        char_duplicate = self.random_duplicate_char()
        char_order_change = self.random_char_change()
        char_confuse = self.random_confuse_char(self.token_text)
        for token in char_del:
            if not ('á' in token or 'é' in token or 'í' in token or 'ú' in token or 'ó' in token):
                variations_list.add(token)
        for token in char_duplicate:
            if not ('á' in token or 'é' in token or 'í' in token or 'ú' in token or 'ó' in token):
                variations_list.add(token)
        for token in char_order_change:
            if not ('á' in token or 'é' in token or 'í' in token or 'ú' in token or 'ó' in token):
                variations_list.add(token)
        for token in char_confuse:
            if not ('á' in token or 'é' in token or 'í' in token or 'ú' in token or 'ó' in token):
                variations_list.add(token)
        for token in char_confuse:
            if not ('á' in token or 'é' in token or 'í' in token or 'ú' in token or 'ó' in token):
                token_aux = self.token_text
                self.token_text = token
                char_del_f2 = self.random_char_del()
                char_duplicate_f2 = self.random_duplicate_char()
                char_order_change_f2 = self.random_char_change()
                self.token_text = token_aux
                for token_f2 in char_del_f2:
                    variations_list.add(token_f2)
                for token_f2 in char_duplicate_f2:
                    variations_list.add(token_f2)
                for token_f2 in char_order_change_f2:
                    variations_list.add(token_f2)
        selected_variations = []
        for token in variations_list:
            if damerau_levenshtein_distance(token, self.token_text) <= self.min_dist:
                selected_variations.append(token)
        selected_variations.append(self.token_text)
        return selected_variations

    def shape(self, string):
        shape_string = ''
        for char in string:
            if not str(char).isspace():
                shape_string += 'x'
            else:
                shape_string += ' '
        return shape_string

    def random_confuse_char(self, string):
        new_string_arr = []
        char_confuse = self.rnd_confuse_char(string)
        for token in char_confuse:
            new_string_arr.append(token)
        for string in char_confuse:
            char_confuse2 = self.rnd_confuse_char(string)
            for token in char_confuse:
                new_string_arr.append(token)
            for string2 in char_confuse2:
                char_confuse3 = self.rnd_confuse_char(string2)
                for token in char_confuse3:
                    new_string_arr.append(token)
                for string3 in char_confuse3:
                    char_confuse4 = self.rnd_confuse_char(string3)
                    for token in char_confuse4:
                        new_string_arr.append(token)
        string_arr_sr = []
        for string in new_string_arr:
            if not string in string_arr_sr:
                string_arr_sr.append(string)
        return string_arr_sr

    def rnd_confuse_char(self, string):
        new_string_arr = []
        counter = Counter()
        i = 0
        length = len(string)
        while i < length:
            string_as_list = list(string)
            if i < length - 1:
                if string[i:i+2] in self.confuse_chars:
                    for char in self.confuse_chars[string[i:i+2]]:
                        string_as_list[i] = char
                        del(string_as_list[i + 1])
                        new_string_arr.append("".join(string_as_list))
                        counter[string[i:i+2]] += 1
                elif string[i] in self.confuse_chars:
                    for char in self.confuse_chars[string[i]]:
                        string_as_list[i] = char
                        new_string_arr.append("".join(string_as_list))
                        counter[string[i]] += 1
            else:
                if string[i] in self.confuse_chars:
                    for char in self.confuse_chars[string[i]]:
                        string_as_list[i] = char
                        new_string_arr.append("".join(string_as_list))
                        counter[string[i]] += 1
            i += 1
        for char in counter:
            if counter[char] > 1:
                for replaced_char in self.confuse_chars[char]:
                    new_string_arr.append(string.replace(char, replaced_char))
        return new_string_arr

    def random_char_del(self):
        i = len(self.token_text)
        j = 0
        new_string_arr = []
        while j < i:
            if j == 0:
                new_string_arr.append(self.token_text[1:i])
            elif j == i - 1:
                new_string_arr.append(self.token_text[0:i-1])
            else:
                new_string_arr.append(self.token_text[0:j] + self.token_text[j+1:i])
            j += 1
        return new_string_arr

    def swap(self, arr, p0, p1):
        arr_list = list(arr)
        aux = arr_list[p0]
        arr_list[p0] = arr_list[p1]
        arr_list[p1] = aux
        return "".join(arr_list)

    def random_char_change(self):
        i = 0
        j = i + 1
        aux = ''
        new_string_arr = []
        string = self.token_text
        while j < len(string):
            string = self.swap(string, i, j)
            new_string_arr.append(string)
            string = self.swap(string, i, j)
            i = j
            j += 1
        return new_string_arr

    def random_duplicate_char(self):
        i = 0
        j = len(self.token_text)
        new_string_arr = []
        while i < j:
            if i == 0:
                new_string_arr.append(self.token_text[0:1] + self.token_text[0:1] + self.token_text[1:j])
            else:
                new_string_arr.append(self.token_text[0:i] + self.token_text[i:i+1] + self.token_text[i:j])
            i += 1
        return new_string_arr
