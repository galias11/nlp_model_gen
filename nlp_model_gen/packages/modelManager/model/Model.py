# @Utils
from nlp_model_gen.utils.objectUtils import transform_dict_key_data_to_int

# @Logger
from nlp_model_gen.packages.logger.Logger import Logger

# @Clases
from ..modelLoader.ModelLoader import ModelLoader
from ..token.Token import Token
from ..entity.Entity import Entity
from ..analyzer.Analyzer import Analyzer

class Model:
    __model_id = ''
    __model_name = ''
    __description = ''
    __author = ''
    __path = ''
    __analyzer_rules_set = []
    __reference = None
    __loaded = False

    def __init__(self, model_id, model_name, description, author, path, __analyzer_rules_set):
        self.__model_id = model_id
        self.__model_name = model_name
        self.__description = description
        self.__author = author
        self.__path = path
        self.__analyzer_rules_set = __analyzer_rules_set
        self.__reference = None
        self.__loaded = False

    def get_model_id(self):
        return self.__model_id

    def get_model_name(self):
        return self.__model_name

    def get_description(self):
        return self.__description

    def get_author(self):
        return self.__author

    def get_path(self):
        return self.__path

    def get_analyser_rules_set(self):
        return self.__analyzer_rules_set

    def get_reference(self):
        return self.__reference

    def set_model_name(self, model_name):
        self.__model_name = model_name

    def set_description(self, description):
        self.__description = description

    def set_reference(self, reference):
        self.__reference = reference

    def is_loaded(self):
        return self.__loaded

    def load(self):
        """
        Setea al modelo como cargado.
        """
        Logger.log('L-0056')
        model_reference = ModelLoader.load_model(self.__path)
        if model_reference is not None:
            Logger.log('L-0057')
            self.__loaded = True
        self.__reference = model_reference

    def __get_model_ner(self):
        """
        Devuelve el NER del modelo si existe o un NER en blanco en caso que no exista.

        :return: [SpacyNER] - NER del modelo. Si el modelo no estuviese cargado devuelve
        None.
        """
        if not self.is_loaded():
            return None
        return ModelLoader.get_model_ner(self.__reference)

    def __process_tokenizer_results(self, doc, only_positives=False):
        """
        Procesa los resultados del analisis de un texto almacenados en un doc de spacy en función de los
        resultados del tokenizer.

        :doc: [SpacyDoc] - Documento con los resultado del analisis de spacy.

        :only_positives: [boolean] - Si esta activado, solo se devulven los resultados positivos.

        :return: [List(Dict)] - Lista con los resultados del analisis del tokenizer.
        """
        results = list([])
        if doc is None:
            return results
        token_analyzer = Analyzer(self.__analyzer_rules_set)
        for sent in doc.sents:
            for token in sent:
                generated_token = Token(token.lemma_, token.is_oov, token.pos_, token.sent, token.sentiment, token.tag_, sent.text)
                token_analyzer.analyze_token(generated_token)
                if not only_positives or generated_token.is_positive():
                    results.append(generated_token)
        return results

    def __process_ner_results(self, doc):
        """
        Procesa los resultados del analisis de un texto almacenados en un doc de spacy en función de los
        resultados del NER.

        :doc: [SpacyDoc] - Documento con los resultado del analisis de spacy.

        :return: [List(Dict)] - Lista con los resultados del analisis del NER  
        """
        results = list([])
        if doc is None:
            return results
        for ent in doc.ents:
            results.append(Entity(ent.text, ent.start_char, ent.end_char, ent.label_))
        return results

    def analyse_text(self, text, only_positives=False):
        """
        Analiza el texto deseado.

        :text: [String] - Texto a analizar

        :only_positives: [Boolean] - Si esta activado solo se devulven los resultados positivos

        :return: [Dict()] - Resultados del análisis.
        """
        Logger.log('L-0059')
        if not self.is_loaded():
            Logger.log('L-0060')
            return None
        doc = self.__reference(text)
        Logger.log('L-0061')
        results = {
            'tokenizer_results': self.__process_tokenizer_results(doc, only_positives),
            'ner_results': self.__process_ner_results(doc)
        }
        Logger.log('L-0062')
        Logger.log('L-0063')
        return results

    def add_tokenizer_rule_set(self, rule_set):
        """
        Agrega una regla al modelo. El modelo debe estar inicializado.

        :rule_set: [Dict] - Regla agregar al tokenizer del modelo.
        """
        tokenizer = self.__reference.tokenizer
        for rule in rule_set:
            token_key = next(iter(rule))
            exception_data = rule[token_key][0]
            exception_dict = transform_dict_key_data_to_int(exception_data)
            tokenizer.add_special_case(token_key, [exception_dict])

    def train_model(self, training_data):
        """
        Aplica los ejemplos de entrenamiento al entrenamiento del modelo.

        :training_data: [List(Dict)] - Lista de ejemplos de entrenamiento.

        :return: [boolean] - True si el entrenamiento fue exitoso, False en caso contrario.
        """
        if training_data is None:
            return False
        if not self.is_loaded():
            Logger.log('L-0340')
            self.load()
            if not self.is_loaded():
                Logger.log('L-0341')
                return False
            Logger.log('L-0342')
        return ModelLoader.apply_training_data(self, training_data)

    def to_dict(self):
        """
        Retorna un diccionario con la información del modelo.

        :return: [Dict] - Diccionario con los datos del modelo.
        """
        return dict({
            'model_id': self.__model_id,
            'model_name': self.__model_name,
            'descripcion': self.__description,
            'author': self.__author,
            'path': self.__path
        })

    def __eq__(self, other):
        """
        Sobreescribe metodo equals de la clase.
        """
        if other is None or not isinstance(other, Model):
            return False
        return self.__model_id == other.get_model_id()
