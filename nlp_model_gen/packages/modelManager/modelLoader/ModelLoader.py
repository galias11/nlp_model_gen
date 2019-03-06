# @Vendors
import spacy

# @Logger
from nlp_model_gen.packages.logger.Logger import Logger
from nlp_model_gen.packages.logger.assets.logColors import ERROR_COLOR

# @Utils
from nlp_model_gen.utils.fileUtils import (
    build_path, 
    check_dir_existence, 
    copy_file,
    create_dir_if_not_exist, 
    get_absoulute_path,
    remove_dir
)

# @Constants
from nlp_model_gen.constants.constants import (
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
            full_path = build_path(MODEL_MANAGER_ROOT_DIR, path, add_absolute_root=True)
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
            Logger.log('L-0030')
            base_path = build_path(MODEL_MANAGER_ROOT_DIR, path)
            if check_dir_existence(base_path):
                Logger.log('L-0031')
                return False
            model_storage_path = get_absoulute_path(base_path)
            model.to_disk(model_storage_path)
            custom_model_files_path = build_path(base_path, MODEL_MANAGER_CUSTOM_FILES_DIR)
            create_dir_if_not_exist(custom_model_files_path)
            model_seed_path = build_path(tmp_files_path, TOKEN_RULES_GEN_MODEL_SEED_FILENAME)
            model_seed_copy_path = build_path(custom_model_files_path, TOKEN_RULES_GEN_MODEL_SEED_FILENAME, add_absolute_root=True)
            copy_file(model_seed_path, model_seed_copy_path, is_absolute_path=True)
            Logger.log('L-0032')
            return True
        except Exception as e:
            Logger.log('L-0033', [{'text': e, 'color': ERROR_COLOR}])
            return False

    @staticmethod
    def delete_model_files(path):
        """
        Elimina los archivos de un modelo del disco.

        :path: [String] - Ruta a eliminar.

        :return: [Boolean] - Ture si el modelo fue borrado correctamente, False en caso contrario.
        """
        Logger.log('L-0070')
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
