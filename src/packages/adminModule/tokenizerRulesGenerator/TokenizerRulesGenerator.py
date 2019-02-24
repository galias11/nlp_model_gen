# @Utils
from src.utils.fileUtils import build_path, check_dir_existence, create_dir_if_not_exist, dictionary_to_disk

# @Constants
from src.constants.constants import (
    TOKEN_RULES_GEN_MODEL_SEED_FILENAME,
    TOKEN_RULES_GEN_TMP_ROOT_PATH,
    TOKEN_RULES_GEN_TYPE_NOUN,
    TOKEN_RULES_GEN_TYPE_VERB,
    TOKEN_RULES_GEN_RULES_EXT
)

# @Log
from src.packages.logger.assets.logColors import OK_COLOR
from src.packages.logger.assets.logTexts import (
    GENERAL_OK,
    TOKEN_RULES_GEN_CREATING_CATEG,
    TOKEN_RULES_GEN_CREATING_DICT,
    TOKEN_RULES_GEN_CREATING_TMP_FILES,
    TOKEN_RULES_GEN_MODEL_FILES_GENERATED,
    TOKEN_RULES_GEN_TMP_FILES_GENERATED
)

# @Classes
from src.packages.logger.Logger import Logger
from ..tokenGenerator.TokenGenerator import TokenGenerator

class TokenizerRulesGenerator:
    token_generator = None

    def __init__(self):
        self.__token_generator = TokenGenerator()

    def __generate_verb_rules(self, categories, max_dist, base_path):
        """
        Genera todas las reglas necesarias para generar un nuevo modelo con el
        tokenizer modificado a partir de las categorias indicadas. Para cada
        una de dichas categorias genera un directorio temporal del modelo (el
        mismo se será eliminado al finalizar el proceso de creación del modelo).

        Solo toma aquellas categorias que sean de tipo 'verb'

        :categories: [Dict] - Diccionario conteniendo las categorias y los token por cada una de ellas.

        :max_dist: [int] - Distancia de demerau levenshtein máxima

        :base_path: [String] - Ruta raíz del modelo.
        """
        for key in categories.keys():
            Logger.log(TOKEN_RULES_GEN_CREATING_CATEG, [{'text': categories[key]['name'], 'color': OK_COLOR}])
            category_path = build_path(base_path, categories[key]['default_dir'])
            create_dir_if_not_exist(category_path)
            Logger.log(TOKEN_RULES_GEN_CREATING_TMP_FILES)
            for verb in categories[key]['dictionary']:
                verb_path = build_path(category_path, verb)
                create_dir_if_not_exist(verb_path)
                exceptions = self.__token_generator.generate_verb_rules_set(verb, max_dist)
                dictionary_to_disk(build_path(verb_path, verb + TOKEN_RULES_GEN_RULES_EXT), exceptions)
            Logger.log(TOKEN_RULES_GEN_TMP_FILES_GENERATED)
            Logger.log(TOKEN_RULES_GEN_CREATING_DICT, [{'text': categories[key]['name'], 'color': OK_COLOR}])
            Logger.log(GENERAL_OK)
            Logger.log(TOKEN_RULES_GEN_MODEL_FILES_GENERATED)

    def __generate_noun_rules(self, categories, max_dist, base_path):
        """
        Genera todas las reglas necesarias para generar un nuevo modelo con el
        tokenizer modificado a partir de las categorias guardadas en el atributo
        categories de la clase. Para cada una de dichas categorias genera un
        directorio separado dentro del directorio maestro del nuevo modelo.

        Solo toma aquellas categorias que sean de tipo 'noun'

        :categories: [Dict] - Diccionario conteniendo las categorias y los tokens de cada una de ellas.

        :max_dist: [int] - Distancia de demerau levenshtein máxima

        :base_path: [String] - Ruta raíz del modelo.
        """

        for key in categories.keys():
            Logger.log(TOKEN_RULES_GEN_CREATING_CATEG, [{'text': categories[key]['name'], 'color': OK_COLOR}])
            category_path = build_path(base_path, categories[key]['default_dir'])
            create_dir_if_not_exist(category_path)
            Logger.log(TOKEN_RULES_GEN_CREATING_TMP_FILES)
            for noun in categories[key]['dictionary']:
                noun_path = build_path(category_path, noun)
                create_dir_if_not_exist(noun_path)
                exceptions = self.__token_generator.generate_noun_rules_set(noun, max_dist)
                dictionary_to_disk(build_path(noun_path, noun + TOKEN_RULES_GEN_RULES_EXT), exceptions)    
                Logger.log(TOKEN_RULES_GEN_CREATING_DICT, [{'text': categories[key]['name'], 'color': OK_COLOR}])
                Logger.log(GENERAL_OK)
            Logger.log(GENERAL_OK)
            Logger.log(TOKEN_RULES_GEN_MODEL_FILES_GENERATED)

    def __save_model_seed(self, model_seed, base_path):
        """
        Guarda la semilla del modelo en el disco.

        :model_seed: [Dict] - Semilla para la creación del modelo.

        :base_path: [String] - Directorio base del modelo.
        """
        path = build_path(base_path, TOKEN_RULES_GEN_MODEL_SEED_FILENAME)
        dictionary_to_disk(path, model_seed)

    def generate_model_data(self, model_seed, path, max_dist):
        """
        A partir de una model_seed, crea los archivos de configuración para modificar el tokenizer
        de un modelo de spacy. 

        :model_seed: [Dict] - Semilla para la creación del modelo.

        :base_path: [String] - Directorio base del modelo.

        :max_dist: [int] - Distancia de demerau levenshtein máxima para las deformaciones a los token.
        """
        base_path = build_path(TOKEN_RULES_GEN_TMP_ROOT_PATH, path)
        if check_dir_existence(base_path):
            return False
        try:
            create_dir_if_not_exist(base_path)
            self.__save_model_seed(model_seed, base_path)
            nouns_path = build_path(base_path, TOKEN_RULES_GEN_TYPE_NOUN)
            create_dir_if_not_exist(nouns_path)
            verbs_path = build_path(base_path, TOKEN_RULES_GEN_TYPE_VERB)
            create_dir_if_not_exist(verbs_path)
            self.__generate_noun_rules(model_seed['nouns'], max_dist, nouns_path)
            self.__generate_verb_rules(model_seed['verbs'], max_dist, verbs_path)
            return base_path
        except:
            return False