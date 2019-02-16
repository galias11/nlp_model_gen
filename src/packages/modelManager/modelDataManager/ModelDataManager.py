# @Constatns
from src.constants.constants import ( MODEL_MANAGER_DB, MODEL_MANAGER_MODELS_COLLECTION )

class ModelDataManager:
    def __init__(self):
        pass

    def get_models(self):
        """
        Devuelve un listado de los modelos disponibles y sus caracteristicas.

        :return: [List(Dict)] - Listado de todos los modelos y sus datos.
        """
        pass

    def save_model_data(self, model_name, description, author, path):
        """
        Guarda información de un modelo.

        :model_name: [String] - Nombre del modelo (actua como id).

        :description: [String] - Descripción del modelo.

        :author: [String] - Nombre del creador del modelo.

        :path: [String] - Ruta relativa para encontrar el modelo.

        :return: [boolean] - True si se han guardado los datos con exito, False en caso contrario.
        """
        pass

    def modify_model_data(self, model_name, description):
        """
        Modifica el nombre o la descripción de un modelo, el nuevo nombre no debe existir.

        :model_name: [String] - Nuevo nombre del modelo (actua como id).

        :description: [String] - Nueva descripción del modelo.

        :return: [boolean] - True si se ha guardado la modificación con exito, False en caso contrario.
        """
        pass

    def remove_model_data(self, model_name):
        """
        Elimina la entrada para un modelo.

        :model_name: [String] - Nombre del modelo a eliminar.

        :return: [boolean] - True si se ha eliminado con exito, False en caso contrario.
        """
        pass
