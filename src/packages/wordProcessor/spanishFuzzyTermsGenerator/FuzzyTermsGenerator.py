# @Vendors
import itertools

# @Utils
from src.utils.fileUtils import loadDictFromJSONFile

# @Constants
from src.constants.constants import (WORD_PROCESOR_DEFAULT_THEME, WORD_PROCESOR_RESERVED_THEME)

# @Helpers
from .helpers.demerauDistanceHelper import damerau_levenshtein_distance
from .helpers.fuzzyHelper import (
    rnd_char_change,
    rnd_char_del,
    rnd_confuse_char,
    rnd_duplicate_char
)

# @Assets
config = loadDictFromJSONFile('wordProcessor-fuzzyTermsConfig')

class FuzzyTermsGenerator:
    """
    Esta clase sirve como generador de variaciones para un token. A partir de un
    token permite generar diferentes variaciones en su escritura.
    """

    def __init__(self, config_theme=WORD_PROCESOR_DEFAULT_THEME):
        self.transformations = [rnd_confuse_char, rnd_char_del, rnd_char_change, rnd_duplicate_char]
        self.config_theme = config_theme if config_theme in config.keys() and config_theme is not WORD_PROCESOR_RESERVED_THEME else WORD_PROCESOR_DEFAULT_THEME
        self.configs = {
            'confuse_chars': config[self.config_theme]['char_confusions'],
            'confuse_chars_max_length': config[self.config_theme]['char_confusions_max_length']
        }
        
    def set_config_theme(self, config_theme):
        if config_theme in config.keys() and config_theme is not WORD_PROCESOR_RESERVED_THEME:
            self.config_theme = config_theme
            self.configs = {
                'confuse_chars': config[self.config_theme]['char_confusions'],
                'confuse_chars_max_length': config[self.config_theme]['char_confusions_max_length']
            }

    def get_fuzzy_tokens(self, token, max_distance=0):
        """
        Genera todas las posibles variaciones de la palabra con la que esta
        instanciada la clase (eliminación, trasposición, sustitución y
        duplicación) soportadas. De todas ellas filtra únicamente aquellas
        cuya distancia de demerau_levenshtein sea menor a la distancia máxima
        establecida para la clase y retorna un arreglo con aquellas que cumplan
        dicha condición.

        :token: Termino a deformar

        :max_distance: Distancia de demerau_levenstein maxima permitida

        :return: Arreglo con todas las variaciones que puede generar la clase
        para la palabra con la que fue instanciada, cuya distancia de
        demerau_levenshtein es igual o menor a la establecida.
        """
        transformation_permutations = self.get_transform_permutations()
        transformation_list = []
        for transformation_sequence in transformation_permutations:
            transformation_list += self.apply_transformation_sequence(token, transformation_sequence)
        filtered_list = self.filter_variations_list(token, transformation_list, max_distance)
        return filtered_list

    def apply_transformation_sequence(self, token, transformation_sequence):
        """
        Aplica una secuencia de transformaciones determinada en el orden recibido.

        :token: Termino a deformar.

        :transformation_sequence: Secuencia ordenada de funciones de tranforamación

        :return: lista de tokens transformados
        """
        variations_list = [token]
        for transformation in transformation_sequence:
            self.apply_transformation(variations_list, transformation)
        return variations_list

    def filter_variations_list(self, token, transformation_list, max_distance):
        """
        Filtra una lista de variaciones, eliminando aquellas entradas que esten 
        repetidas o que no cumplan con la distancia minima requerida al token.

        :token: Termino original.

        :transformation_list: Lista de transformaciones para el termino original

        :max_distance: Distancia de demerau_levenshtein maxima con el termino 
        original.

        :return: 
        """
        filtered_list = list(set(transformation_list))
        filtered_list = filter(lambda transformed_token: damerau_levenshtein_distance(token, transformed_token, True) <= max_distance, filtered_list)
        return list(filtered_list)

    def apply_transformation(self, token_list, transformation):
        """
        Aplica una transformación determinada a cada uno de los tokens contenidos
        en una lista de tokens

        :token_list: lista de tokens

        :transformation: Función de transformación a aplicar a cada uno de los 
        tokens

        :return: Lista de tokens transformados resultante de aplicar la 
        transformación dada a cada token
        """
        aux_list = []
        for token in token_list:
            aux_list += transformation(token, self.configs)
        token_list += aux_list

    def get_transform_permutations(self):
        """
        Obtiene todas las posibles permutaciones para la lista de permutaciones 
        posibles

        :return: lista de arreglos cada uno conteniendo las transformaciones
        en un orden diferente.
        """
        return itertools.permutations(self.transformations)
