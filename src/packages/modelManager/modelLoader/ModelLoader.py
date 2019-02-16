# @Vendors
import spacy

class ModelLoader:
    __connected: False

    def __init__(self):
        self.__initialize()

    def __initialize(self):
        """
        Inicializa el modulo conectando con spacy.
        """
        pass

    def load_model(self, path):
        """
        Carga el modelo a partir del path.

        :path: [String] - Ruta para acceder al modelo.

        :return: [SpacyModelRef] - Referencia al modelo de spacy
        """
        try:
            nlp_model = spacy.load(path)
            return nlp_model
        except:
            return None

    def save_model(self, path):
        """
        Guarda el modelo en el path solicitado.

        :path: [String] - Ruta en la cual guardar el modelo.

        :return: [boolean] - True si el modelo fue cargado correctamente, False en caso contrario.
        """
        pass

    def delete_model_files(self, path):
        """
        Elimina los archivos de un modelo del disco.

        :path: [String] - Ruta a eliminar.

        :return: [Boolean] - Ture si el modelo fue borrado correctamente, False en caso contrario.
        """
        pass

    def apply_training_data(self, path, training_data):
        """
        Ejecuta la rutina de entrenamiento de un modelo particular.

        :path: [String] - Ruta donde se encuentra el modelo.

        :training_data: [List(Dict)] - Conjunto de datos de entrenamiento.

        :return: [boolean] - True si se ha realizado el entrenamiento correctamente, False en caso contrario.
        """
        pass