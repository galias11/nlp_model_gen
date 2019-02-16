# @Vendors
import spacy

# @Utils
from src.utils.fileUtils import check_dir_existence

# @Constants
from src.constants.constants import (
    MODEL_MANAGER_DEFAULT_BASE_MODEL,
    MODEL_MANAGER_ROOT_DIR
)

class ModelLoader:
    def __init__(self):
        pass

    @staticmethod
    def load_model(path):
        """
        Carga el modelo a partir del path.

        :path: [String] - Ruta para acceder al modelo.

        :return: [SpacyModelRef] - Referencia al modelo de spacy, None si no se pdo cargar el modelo.
        """
        try:
            nlp_model = spacy.load(path)
            return nlp_model
        except:
            return None

    @staticmethod
    def initiate_default_model():
        """
        Inicializa un instancia del modelo por defecto.
    
        :return: [SpacyModelRef] - Referencia al modelo de spacy
        """
        default_nlp_model = ModelLoader.load_model(MODEL_MANAGER_DEFAULT_BASE_MODEL)
        return default_nlp_model

    @staticmethod
    def save_model(model, path):
        """
        Guarda el modelo en el path solicitado.

        :model: [SpacyModelRef] - Referencia a un modelo de spacy.

        :path: [String] - Ruta en la cual guardar el modelo.

        :return: [boolean] - True si el modelo fue cargado correctamente, False en caso contrario.
        """
        try:
            full_path = MODEL_MANAGER_ROOT_DIR + path
            if check_dir_existence(full_path):
                return False
            model.to_disk(full_path)
            return True
        except:
            return False

    @staticmethod
    def delete_model_files(path):
        """
        Elimina los archivos de un modelo del disco.

        :path: [String] - Ruta a eliminar.

        :return: [Boolean] - Ture si el modelo fue borrado correctamente, False en caso contrario.
        """
        pass

    @staticmethod
    def apply_training_data(path, training_data):
        """
        Ejecuta la rutina de entrenamiento de un modelo particular.

        :path: [String] - Ruta donde se encuentra el modelo.

        :training_data: [List(Dict)] - Conjunto de datos de entrenamiento.

        :return: [boolean] - True si se ha realizado el entrenamiento correctamente, False en caso contrario.
        """
        pass
