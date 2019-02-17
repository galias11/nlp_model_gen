# @Classes
from .modelDataManager.ModelDataManager import ModelDataManager
from .modelLoader.ModelLoader import ModelLoader
from .model.Model import Model

class ModelManagerController:
    __models = list([])
    __init_success = False

    def __init__(self):
        self.__initialize()

    def __initialize(self):
        """
        Inicializa el modulo.
        """
        try:
            stored_models_data = ModelDataManager.get_models()
            for model in stored_models_data:
                model_object = Model(model['model_name'], model['description'], model['author'], model['path'])
                self.__models.append(model_object)
            self.__init_success = True
        except Exception as e:
            print(e)
            self.__init_success = False

    def __get_model(self, model_name):
        """
        Obtiene un modelo de la lista de modelos disponibles.

        :model_name: [String] - Nombre del modelo.

        :return: [Model] - Modelo encontrado, None si el modelo no existe
        """
        for model in self.__models:
            if model.get_model_name() == model_name:
                return model
        return None

    def __initialize_custom_model(self):
        """
        Inicializa un nuevo modelo de spacy, cargando lo en memoria.

        :return: [SpacyModelRef] - Referencia al nuevo modelo de spacy creado.
        """
        return ModelLoader.initiate_default_model()

    def load_model(self, model_name):
        """
        Carga el modelo requerido en memoria.

        :model_name: [String] - Nombre del modelo.

        :return: [boolean] - True si fue exitoso, false en caso contrario.
        """
        selected_model = self.__get_model(model_name)
        if selected_model is None:
            return False
        selected_model.load()
        return selected_model.is_loaded()

    def get_available_models(self):
        """
        Devuelve una lista de los modelos disponibles y sus caracteristicas.

        :return: [List(Model)] - Lista de los modelos disponibles y sus caracteristicas.
        """
        return self.__models

    def get_available_models_dict(self):
        """
        Devuelve la lista de modelos disponibles y sus caracteristicas convertidos a formato dict.
        
        :return: [List(Dict)] - Lista de los modelos disponibles y sus caracteristicas.
        """
        models_list = list([])
        for model in self.__models:
            models_list.append(model.to_dict())
        return models_list

    def analyze_text(self, model_name, text):
        """
        Analiza un texto con el modelo solicitado.

        :model_name: [String] - Nombre del modelo a utilizar.

        :text: [String] - Texto a analizar.

        :return: [SpacyDoc] - Resultados del análisis.
        """
        pass

    def train_model(self, model_name, training_data):
        """
        Aplica un set de datos de entrenamiento al modelo solicitado.

        :model_name: [String] - Nombre del modelo a entrenar.

        :training_data: [List(Dict)] - Set de datos de entrenamiento.

        :return: [boolean] - True si el proceso ha sido exitoso, False en caso contrario.
        """
        pass

    def create_model(self, model_name, description, author, path, tokenizer_exceptions):
        """
        Crea un nuevo modelo. Crea los datos necesarios y lo guarda tanto en disco como su
        referencia en la base de datos.

        :model_name: [String] - Nombre del modelo.

        :description: [String] - Descripción.

        :author: [String] - Referencia del autor del modelo.

        :path: [String] - Path relativo donde guardar el modelo.

        :tokenizer_exceptions: [List(Dict)] - Lista de excepciones del modulo tokenizer del modelo.

        :return: [boolean] - True si el proceso ha sido exitoso, False en caso contrario.
        """
        if self.__get_model(model_name) is not None:
            return False
        try:
            custom_model = self.__initialize_custom_model()
            # TODO: Add tokenizer_exceptions logic here.
            ModelDataManager.save_model_data(model_name, description, author, path)
            ModelLoader.save_model(custom_model, path)
            new_model = Model(model_name, description, author, path)
            new_model.set_reference(custom_model)
            self.__models.append(new_model)
            return True
        except:
            return False

    def edit_model(self, previous_model_name, model_name, description):
        """
        Permite editar la descripción de un modelo. El modelo debe existir.

        :model_name: [String] - Nombre del modelo.

        :description: [String] - Nueva descripción.

        :return: [boolean] - True si la modificación se ha realizado correctamente, False en caso contrario.
        """
        selected_model = self.__get_model(previous_model_name)
        if selected_model is None:
            return False
        target_model = self.__get_model(model_name)
        if target_model is not None:
            return False
        if not ModelDataManager.modify_model_data(previous_model_name, model_name, description):
            return False
        selected_model.set_model_name(model_name)
        selected_model.set_description(description)
        return True

    def remove_model(self, model_name):
        """
        Elimina un modelo del sistema. Borra los datos del mismo de la base de datos y elimina los archivos
        del mismo del disco.

        :model_name: [String] - Nombre del modelo.

        :return: [boolean] - True si el modelo fue exitosamente borrado, False en caso contrario.
        """
        selected_model = self.__get_model(model_name)
        if selected_model is None:
            return False
        if not ModelDataManager.remove_model_data(selected_model.get_model_name()):
            return False
        if not ModelLoader.delete_model_files(selected_model.get_path()):
            return False
        self.__models.remove(selected_model)
        return True
