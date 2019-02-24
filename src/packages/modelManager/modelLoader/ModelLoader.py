# @Vendors
import spacy

# @Utils
from src.utils.fileUtils import (
    build_path, 
    check_dir_existence, 
    copy_file,
    create_dir_if_not_exist, 
    remove_dir
)

# @Constants
from src.constants.constants import (
    MODEL_MANAGER_CUSTOM_FILES_DIR,
    MODEL_MANAGER_DEFAULT_BASE_MODEL,
    MODEL_MANAGER_ROOT_DIR,
    TOKEN_RULES_GEN_MODEL_SEED_FILENAME
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
            full_path = build_path(MODEL_MANAGER_ROOT_DIR, path)
            nlp_model = spacy.load(full_path)
            return nlp_model
        except:
            return None

    @staticmethod
    def initiate_default_model():
        """
        Inicializa un instancia del modelo por defecto.
    
        :return: [SpacyModelRef] - Referencia al modelo de spacy
        """
        default_nlp_model = spacy.load(MODEL_MANAGER_DEFAULT_BASE_MODEL)
        return default_nlp_model

    @staticmethod
    def save_model(model, path, tmp_files_path):
        """
        Guarda el modelo en el path solicitado.

        :model: [SpacyModelRef] - Referencia a un modelo de spacy.

        :path: [String] - Ruta en la cual guardar el modelo.

        :tmp_files_path: [String] - Ruta donde se encuentran los archivos temporales del modelo.

        :return: [boolean] - True si el modelo fue cargado correctamente, False en caso contrario.
        """
        try:
            full_path = build_path(MODEL_MANAGER_ROOT_DIR, path)
            if check_dir_existence(full_path):
                return False
            model.to_disk(full_path)
            custom_model_files_path = build_path(full_path, MODEL_MANAGER_CUSTOM_FILES_DIR)
            create_dir_if_not_exist(custom_model_files_path)
            model_seed_path = build_path(tmp_files_path, TOKEN_RULES_GEN_MODEL_SEED_FILENAME)
            model_seed_copy_path = build_path(custom_model_files_path, TOKEN_RULES_GEN_MODEL_SEED_FILENAME)
            copy_file(model_seed_path, model_seed_copy_path)
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
        full_path = build_path(MODEL_MANAGER_ROOT_DIR, path)
        return remove_dir(full_path)

    @staticmethod
    def apply_training_data(path, training_data):
        """
        Ejecuta la rutina de entrenamiento de un modelo particular.

        :path: [String] - Ruta donde se encuentra el modelo.

        :training_data: [List(Dict)] - Conjunto de datos de entrenamiento.

        :return: [boolean] - True si se ha realizado el entrenamiento correctamente, False en caso contrario.
        """
        pass
