# @Clases
from ..modelLoader.ModelLoader import ModelLoader
from ..token.Token import Token
from ..entity.Entity import Entity

class Model:
    __model_name = ''
    __description = ''
    __author = ''
    __path = ''
    __reference = None
    __loaded = False

    def __init__(self, model_name, description, author, path):
        self.__model_name = model_name
        self.__description = description
        self.__author = author
        self.__path = path
        self.__reference = None
        self.__loaded = False

    def get_model_name(self):
        return self.__model_name

    def get_description(self):
        return self.__description

    def get_author(self):
        return self.__author

    def get_path(self):
        return self.__path

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
        model_reference = ModelLoader.load_model(self.__path)
        if model_reference is not None:
            self.__loaded = True
        self.__reference = model_reference

    def __process_tokenizer_results(self, doc):
        """
        Procesa los resultados del analisis de un texto almacenados en un doc de spacy en función de los
        resultados del tokenizer.

        :doc: [SpacyDoc] - Documento con los resultado del analisis de spacy.

        :return: [List(Dict)] - Lista con los resultados del analisis del tokenizer   
        """
        results = list([])
        if doc is None:
            return results
        for token in doc:
            results.append(Token(token.lemma_, token.is_oov, token.pos_, token.sent, token.sentiment, token.tag_, token.text))
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

    def analyse_text(self, text):
        """
        Analiza el texto deseado.

        :text: String - Texto a analizar

        :return: [Dict()] - Resultados del análisis.
        """
        if not self.is_loaded():
            return None
        doc = self.__reference(text)
        results = {
            'tokenizer_results': self.__process_tokenizer_results(doc),
            'ner_results': self.__process_ner_results(doc)
        }
        return results

    def train_model(self, training_data):
        """
        Aplica los ejemplos de entrenamiento al entrenamiento del modelo.

        :training_data: [List(Dict)] - Lista de ejemplos de entrenamiento.

        :return: [boolean] - True si el entrenamiento fue exitoso, False en caso contrario.
        """
        pass

    def to_dict(self):
        """
        Retorna un diccionario con la información del modelo.

        :return: [Dict] - Diccionario con los datos del modelo.
        """
        return dict({
            "model_name": self.__model_name,
            "descripcion": self.__description,
            "author": self.__author,
            "path": self.__path
        })

    def __eq__(self, other):
        """
        Sobreescribe metodo equals de la clase.
        """
        if other is None or not isinstance(other, Model):
            return False
        return self.__model_name == other.get_model_name()
