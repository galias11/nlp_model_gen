# @Clases
from ..modelLoader.ModelLoader import ModelLoader

class Model:
    __model_name = ''
    __description = ''
    __author = ''
    __path = ''
    __reference = False
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

    def analyse_text(self, text):
        """
        Analiza el texto deseado.

        :text: String - Texto a analizar

        :return: [List(Dict)] - Resultados del análisis.
        """
        pass

    def train_model(self, training_data):
        """
        Aplica los ejemplos de entrenamiento al entrenamiento del modelo.

        :training_data: [List(Dict)] - Lista de ejemplos de entrenamiento.

        :return: [boolean] - True si el entrenamiento fue exitoso, False en caso contrario.
        """
        pass
