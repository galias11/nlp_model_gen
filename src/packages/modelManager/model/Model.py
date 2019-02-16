class Model:
    __model_name = ''
    __description = ''
    __author = ''
    __path = ''
    __loaded = False

    def __init__(self):
        pass

    def load(self):
        """
        Setea al modelo como cargado.

        :return: [SpacyModelRef] - Referencia al modelo cargado.
        """

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
