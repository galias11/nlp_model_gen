# @Constatns
from src.constants.constants import ( MODEL_MANAGER_DB, MODEL_MANAGER_MODELS_COLLECTION )

# @Helpers
from src.utils.dbUtils import ( 
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
    def check_existing_model(model_name):
        """
        Devuelve un listado de los identificadores de cada modelo disponible.

        :return: [List(String)] - Listado con los identificadores de cada modelo guardado.
        """
        available_model_names = list(map(
            lambda model: model['model_name'], 
            db_get_items(MODEL_MANAGER_DB, MODEL_MANAGER_MODELS_COLLECTION, None, {'model_name': 1})
        ))
        return model_name in available_model_names

    @staticmethod
    def save_model_data(model_name, description, author, path):
        """
        Guarda información de un modelo.

        :model_name: [String] - Nombre del modelo (actua como id).

        :description: [String] - Descripción del modelo.

        :author: [String] - Nombre del creador del modelo.

        :path: [String] - Ruta relativa para encontrar el modelo.

        :return: [boolean] - True si se han guardado los datos con exito, False en caso contrario.
        """
        try:
            if ModelDataManager.check_existing_model(model_name): 
                return False
            data_dict = {
                'model_name': model_name,
                'description': description,
                'author': author,
                'path': path
            }
            db_insert_item(MODEL_MANAGER_DB, MODEL_MANAGER_MODELS_COLLECTION, data_dict)
            return True
        except:
            return False

    @staticmethod
    def modify_model_data(previous_model_name, model_name, description):
        """
        Modifica el nombre o la descripción de un modelo, el nuevo nombre no debe existir y si debe hacerlo el previo.

        :model_name: [String] - Nuevo nombre del modelo (actua como id).

        :description: [String] - Nueva descripción del modelo.

        :return: [boolean] - True si se ha guardado la modificación con exito, False en caso contrario.
        """
        try:
            if ModelDataManager.check_existing_model(model_name):
                return False
            updated_data = {
                'model_name': model_name,
                'description': description
            }
            update_count = db_update_item(MODEL_MANAGER_DB, MODEL_MANAGER_MODELS_COLLECTION, {'model_name': previous_model_name}, updated_data).modified_count
            return True if update_count > 0 else False
        except:
            return False

    @staticmethod
    def remove_model_data(model_name):
        """
        Elimina la entrada para un modelo.

        :model_name: [String] - Nombre del modelo a eliminar.

        :return: [boolean] - True si se ha eliminado con exito, False en caso contrario.
        """
        try:
            delete_count = db_delete_item(MODEL_MANAGER_DB, MODEL_MANAGER_MODELS_COLLECTION, {'model_name': model_name}).deleted_count
            return True if delete_count > 0 else False
        except:
            return False