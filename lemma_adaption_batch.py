from spacy.symbols import ORTH, LEMMA, POS, TAG, SHAPE
import json
import ast
from collections import Counter
import enchant
import hunspell
from os import scandir, getcwd
from os.path import abspath
import fnmatch


DIC_PATH = "/home/infolab/Documentos/SAVE/Dictionaries/dictionary-es_A/"


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
def token_selector(token, lemma, pos, tag, output_file, max_dist):
    generator = custom_token_generator(token, lemma, pos, custom_token_generator.TAG_KEY[tag], max_dist)
    arch = open(output_file, 'w')
    if max_dist == 0:
        arch.write(str(generator.no_variation_tokenizer_rule()))
    else:
        arch.write(str(generator.gen_tokenizer_rules()))
    arch.close()

def dictionary_token_selector(dict_file, pos, tag, output_path, max_dist):
    dictionary = extract_dict_from_file(dict_file)
    for token in dictionary:
        token_selector(token, token, pos, tag, output_path + token + ".rl", max_dist)


def extract_dict_from_file(file_path):
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
def add_rules_to_tokenizer(tokenizer, file_name):
    for token in ast.literal_eval(open(file_name, "r").read()):
        for key in token:
            tokenizer.add_special_case(key, token[key])


# add_dir()
# ***************************************************************************************
# Agrega al tokenizer el contenido de un directorio completo de archivos
# de reglas para excepciones.
def add_dir(tokenizer, path):
    for arch in scandir(path):
        if arch.is_file():
            add_rules_to_tokenizer(tokenizer, abspath(arch.path))

def add_changed_word_model(tokenizer, path):
    for arch in scandir(path):
        if arch.is_dir():
            add_changed_word_model(tokenizer, abspath(arch.path))
        elif fnmatch.fnmatch(arch.name, '*.rl'):
            add_rules_to_tokenizer(tokenizer, abspath(arch.path))


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
def gen_lote_reglas(yo, tu, el, nos, ellos, lemma, tiempo, path, max_dist):
    if tiempo == 'IMP':
        yo_conj = "token_selector(\"" + yo + "\",\"" + lemma + "\",\"VERB\",\"VERB_PRES_1STPER_PLUR\",\"" + path + yo + ".rl\", " + str(max_dist) + ")"
    else:
        yo_conj = "token_selector(\"" + yo + "\",\"" + lemma + "\",\"VERB\",\"VERB_" + tiempo + "_1STPER_SING\",\"" + path + yo + ".rl\", " + str(max_dist) + ")"
    tu_conj = "token_selector(\"" + tu + "\",\"" + lemma + "\",\"VERB\",\"VERB_" + tiempo + "_2NDPER_SING\",\"" + path + tu + ".rl\", " + str(max_dist) + ")"
    el_conj = "token_selector(\"" + el + "\",\"" + lemma + "\",\"VERB\",\"VERB_" + tiempo + "_3RDPER_SING\",\"" + path + el + ".rl\", " + str(max_dist) + ")"
    nos_conj = "token_selector(\"" + nos + "\",\"" + lemma + "\",\"VERB\",\"VERB_" + tiempo + "_1STPER_PLUR\",\"" + path + nos + ".rl\", " + str(max_dist) + ")"
    ellos_conj = "token_selector(\"" + ellos + "\",\"" + lemma + "\",\"VERB\",\"VERB_" + tiempo + "_3RDPER_SING\",\"" + path + ellos + ".rl\", " + str(max_dist) + ")"
    eval(yo_conj)
    eval(tu_conj)
    eval(el_conj)
    eval(nos_conj)
    eval(ellos_conj)

def gen_lote_reglas_completo(infinitive, max_dist, conj_dict, output_dir):
    for conj in conj_dict['inf']:
        token_selector(conj, conj, 'VERB', 'VERB_INF', output_dir + conj + ".rl", max_dist)
    for conj in conj_dict['ger']:
        token_selector(conj, conj, 'VERB', 'VERB_INF', output_dir + conj + ".rl", max_dist)
    for conj in conj_dict['pres']:
        gen_lote_reglas(conj[0], conj[1], conj[2], conj[3], conj[4], infinitive, 'PRES', output_dir, max_dist)
    for conj in conj_dict['past']:
        gen_lote_reglas(conj[0], conj[1], conj[2], conj[3], conj[4], infinitive, 'PAST', output_dir, max_dist)
    for conj in conj_dict['fut']:
        gen_lote_reglas(conj[0], conj[1], conj[2], conj[3], conj[4], infinitive, 'FUT', output_dir, max_dist)
    for conj in conj_dict['imp']:
        gen_lote_reglas(conj[0], conj[1], conj[2], conj[3], conj[4], infinitive, 'IMP', output_dir, max_dist)
    for conj in conj_dict['cond']:
        gen_lote_reglas(conj[0], conj[1], conj[2], conj[3], conj[4], infinitive, 'COND', output_dir, max_dist)

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
    'VERB_COND_1STPER_PLUR' : "VERB__Mood=Cnd|Number=Plur|Person=1|VerbForm=Fin",
    'VERB_COND_3RDPER_PLUR' : "VERB__Mood=Cnd|Number=Plur|Person=3|VerbForm=Fin",
    'VERB_COND_1STPER_SING' : "VERB__Mood=Cnd|Number=Sing|Person=1|VerbForm=Fin",
    'VERB_COND_2NDPER_SING' : "VERB__Mood=Cnd|Number=Sing|Person=2|VerbForm=Fin",
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
    'VERB_FUT_3RDPER_PLUR' : "VERB__Mood=Ind|Number=Plur|Person=3|Tense=Fut|VerbForm=Fin",
    'VERB_IMP_3RDPER_PLUR' : "VERB__Mood=Ind|Number=Plur|Person=3|Tense=Imp|VerbForm=Fin",
    'VERB_PAST_3RDPER_PLUR' : "VERB__Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin",
    'VERB_PRES_3RDPER_PLUR' : "VERB__Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin",
    'VERB_FUT_1STPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=1|Tense=Fut|VerbForm=Fin",
    'VERB_IMP_1STPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=1|Tense=Imp|VerbForm=Fin",
    'VERB_PAST_1STPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin",
    'VERB_PRES_1STPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin",
    'VERB_FUT_2NDPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=2|Tense=Fut|VerbForm=Fin",
    'VERB_IMP_2NDPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=2|Tense=Imp|VerbForm=Fin",
    'VERB_PAST_2NDPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=2|Tense=Past|VerbForm=Fin",
    'VERB_PRES_2NDPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=2|Tense=Pres|VerbForm=Fin",
    'VERB_FUT_3RDPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=3|Tense=Fut|VerbForm=Fin",
    'VERB_IMP_3RDPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=3|Tense=Imp|VerbForm=Fin",
    'VERB_PAST_3RDPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin",
    'VERB_PRES_3RDPER_SING' : "VERB__Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
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
        self.confuse_chars = {'v':['b'],'b':['v'],'n':['m'],'m':['n'],'c':['s','z'],
        's':['c','z'],'z':['s','c'],'q':['k'],'k':['q'],'qu':['k'],'k':['qu'],
        'll':['y'],'y':['ll','i'],'i':['y'],'á':['a'],'é':['e'],
        'í':['i'],'ó':['o'],'ú':['u']}
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
