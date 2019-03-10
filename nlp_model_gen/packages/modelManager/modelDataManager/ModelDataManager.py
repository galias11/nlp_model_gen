# @Logger
from nlp_model_gen.packages.logger.Logger import Logger

# @Constatns
from nlp_model_gen.constants.constants import ( MODEL_MANAGER_DB, MODEL_MANAGER_MODELS_COLLECTION )

# @Log colors
from nlp_model_gen.packages.logger.assets.logColors import ERROR_COLOR

# @Helpers
from nlp_model_gen.utils.dbUtils import ( 
    db_delete_item,
    db_get_items, 
    db_insert_item,
    db_update_item
)

class ModelDataManager:
    def __init__(self):
        pass

    @staticmethod
    def get_models():
        """
        Devuelve un listado de los modelos disponibles y sus caracteristicas.

        :return: [List(Dict)] - Listado de todos los modelos y sus datos.
        """
        try:
            available_models = db_get_items(MODEL_MANAGER_DB, MODEL_MANAGER_MODELS_COLLECTION, None, {'_id': 0})
            return available_models
        except:
            return None

    @staticmethod
    def check_existing_model(model_id):
        """
        Devuelve un listado de los identificadores de cada modelo disponible.

        :model_id: [String] - id del modelo buscado. 

        :return: [List(String)] - Listado con los identificadores de cada modelo guardado.
        """
        available_model_names = list(map(
            lambda model: model['model_id'], 
            db_get_items(MODEL_MANAGER_DB, MODEL_MANAGER_MODELS_COLLECTION, None, {'model_id': 1})
        ))
        return model_id in available_model_names

    @staticmethod
    def save_model_data(model_id, model_name, description, author, path, analyser_rules_set):
        """
        Guarda información de un modelo.

        :model_id: [String] - Id del modelo.

        :model_name: [String] - Nombre del modelo (actua como id).

        :description: [String] - Descripción del modelo.

        :author: [String] - Nombre del creador del modelo.

        :path: [String] - Ruta relativa para encontrar el modelo.

        :analyser_rules_set: [List(Dict)] - Lista de reglas para el analizador

        :return: [boolean] - True si se han guardado los datos con exito, False en caso contrario.
        """
        try:
            Logger.log('L-0026')
            if ModelDataManager.check_existing_model(model_id):
                Logger.log('L-0027')
                return False
            data_dict = {
                'model_id': model_id,
                'model_name': model_name,
                'description': description,
                'author': author,
                'path': path,
                'analyzer_rules_set': analyser_rules_set
            }
            db_insert_item(MODEL_MANAGER_DB, MODEL_MANAGER_MODELS_COLLECTION, data_dict)
            Logger.log('L-0029')
            return True
        except Exception as e:
            Logger.log('L-0028', [{'text': e, 'color': ERROR_COLOR}])
            return False

    @staticmethod
    def modify_model_data(model_id, model_name, description):
        """
        Modifica el nombre o la descripción de un modelo, el nuevo nombre no debe existir y si debe hacerlo el previo.

        :model_id: [String] - Id del modelo.

        :model_name: [String] - Nuevo nombre del modelo.

        :description: [String] - Nueva descripción del modelo.

        :return: [boolean] - True si se ha guardado la modificación con exito, False en caso contrario.
        """
        try:
            Logger.log('L-0080')
            updated_data = {
                'model_name': model_name,
                'description': description
            }
            update_count = db_update_item(MODEL_MANAGER_DB, MODEL_MANAGER_MODELS_COLLECTION, {'model_id': model_id}, updated_data).modified_count
            return True if update_count > 0 else False
        except Exception as e:
            Logger.log('L-0079', [{'text': e, 'color': ERROR_COLOR}])
            return False

    @staticmethod
    def remove_model_data(model_id):
        """
        Elimina la entrada para un modelo.

        :model_id: [String] - Id del modelo a eliminar.

        :return: [boolean] - True si se ha eliminado con exito, False en caso contrario.
        """
        try:
            Logger.log('L-0066')
            delete_count = db_delete_item(MODEL_MANAGER_DB, MODEL_MANAGER_MODELS_COLLECTION, {'model_id': model_id}).deleted_count
            return True if delete_count > 0 else False
        except Exception as e:
            Logger.log('L-0067', [{'text': e, 'color': ERROR_COLOR}])
            return False
