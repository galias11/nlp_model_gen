# @Vendors
import spacy
import random
from spacy.util import minibatch, compounding

# @Logger
from nlp_model_gen.packages.logger.Logger import Logger
from nlp_model_gen.packages.logger.assets.logColors import ERROR_COLOR, HIGHLIGHT_COLOR, SUCCESS_COLOR

# @Utils
from nlp_model_gen.utils.fileUtils import (
    build_path, 
    check_dir_existence,
    copy_file,
    create_dir_if_not_exist,
    dictionary_to_disk,
    get_absoulute_path,
    load_json_file,
    remove_dir
)

# @Constants
from nlp_model_gen.constants.constants import (
    COMPOUNDING_COMPOUND_DEFAULT,
    COMPOUNDING_START_DEFAULT,
    COMPOUNDING_STOP_DEFAULT,
    DIR_PATH_SEPARATOR,
    MODEL_MANAGER_CUSTOM_FILES_DIR,
    MODEL_MANAGER_DEFAULT_BASE_MODEL,
    MODEL_MANAGER_ROOT_DIR,
    MODEL_NER,
    MODEL_TRAINING_DROP_RATE,
    MODEL_TRAINING_ITER_AMOUNT,
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
    def get_model_ner(model_ref):
        """
        Obtiene el NER de un determinado modelo. Si el mismo no existe, crea uno nuevo y lo agrega
        al pipeline del modelo.

        :model_reference: [SpacyModelRef] - Referencia al modelo de spacy
        """
        Logger.log('L-0343')
        ner = None
        if MODEL_NER in model_ref.pipe_names:
            ner = model_ref.get_pipe(MODEL_NER)
        else:
            ner = model_ref.create_pipe(MODEL_NER)
            model_ref.add_pipe(ner, last=True)
        Logger.log('L-0344')
        return ner

    @staticmethod
    def add_ner_labels(ner, training_data):
        """
        Agrega las nuevas etiquetas al ner.

        :ner: [SpacyNER] - NER al cual aplicar las nuevas etiquetas

        :training_data: [List(Dict)] - Set de datos de entrenamiento.
        """
        Logger.log('L-0345')
        for _, annotations in training_data:
            for ent in annotations.get('entities'):
                ner.add_label(ent[2])
        Logger.log('L-0346')

    @staticmethod
    def apply_training_loop(model_ref, training_data):
        """
        Aplica el bucle de entrenamiento al NER de un determinado modelo.

        :model_ref: [SpacyModelRef] - Referencia del modelo de spacy

        :training_data: [List] - Set de datos de entrenamiento
        """
        for iter_number in range(1, MODEL_TRAINING_ITER_AMOUNT):
            Logger.log('L-0350', [{'text': iter_number, 'color': SUCCESS_COLOR}, {'text': MODEL_TRAINING_ITER_AMOUNT, 'color': HIGHLIGHT_COLOR}])
            random.shuffle(training_data)
            losses = {}
            batches = minibatch(training_data, size=compounding(COMPOUNDING_START_DEFAULT, COMPOUNDING_STOP_DEFAULT, COMPOUNDING_COMPOUND_DEFAULT))
            for batch in batches:
                texts, annotations = zip(*batch)
                model_ref.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=MODEL_TRAINING_DROP_RATE,  # dropout - make it harder to memorise data
                    losses=losses,
                )
            Logger.log('L-0351', [{'text': iter_number, 'color': SUCCESS_COLOR}, {'text': losses['ner'], 'color': HIGHLIGHT_COLOR}])
    
    @staticmethod
    def update_model_info(model_ref, model_path):
        """
        Actualiza la información en dico para el modelo que se encuentra en el path
        especificado.

        :model_ref: [SpacyModelRef] - Referencia del modelo de spacy

        :model_path: [String] - Directorio base del modelo (nombre del mismo).
        """
        Logger.log('L-0352')
        relative_base_path = build_path(MODEL_MANAGER_ROOT_DIR, model_path)
        relative_seed_path = build_path(MODEL_MANAGER_ROOT_DIR, model_path +  DIR_PATH_SEPARATOR + MODEL_MANAGER_CUSTOM_FILES_DIR)
        base_path = build_path(MODEL_MANAGER_ROOT_DIR, model_path, add_absolute_root=True)
        seed_dir_path = build_path(MODEL_MANAGER_ROOT_DIR, model_path +  DIR_PATH_SEPARATOR + MODEL_MANAGER_CUSTOM_FILES_DIR, add_absolute_root=True)
        model_seed = load_json_file(build_path(seed_dir_path, TOKEN_RULES_GEN_MODEL_SEED_FILENAME))
        remove_dir(relative_base_path)
        create_dir_if_not_exist(relative_base_path)
        create_dir_if_not_exist(relative_seed_path)
        model_ref.to_disk(base_path)
        dictionary_to_disk(relative_seed_path + DIR_PATH_SEPARATOR + TOKEN_RULES_GEN_MODEL_SEED_FILENAME, model_seed)
        Logger.log('L-0353')

    @staticmethod
    def apply_training_data(model, training_data):
        """
        Ejecuta la rutina de entrenamiento de un modelo particular.

        :model: [Model] - Modelo sobre el cual aplicar el entrenamiento.

        :training_data: [List(Dict)] - Conjunto de datos de entrenamiento.

        :return: [boolean] - True si se ha realizado el entrenamiento correctamente, 
        False en caso contrario.
        """
        model_ref = model.get_reference()
        model_path = model.get_path()
        ner = ModelLoader.get_model_ner(model_ref)
        ModelLoader.add_ner_labels(ner, training_data)
        other_pipes = [pipe for pipe in model_ref.pipe_names if pipe != MODEL_NER]
        Logger.log('L-0347')
        try:
            with model_ref.disable_pipes(*other_pipes):
                ModelLoader.apply_training_loop(model_ref, training_data)
            ModelLoader.update_model_info(model_ref, model_path)
            Logger.log('L-0348')
            return True
        except Exception as e:
            Logger.log('L-0349', [{'text': e, 'color': ERROR_COLOR}])
            return False
