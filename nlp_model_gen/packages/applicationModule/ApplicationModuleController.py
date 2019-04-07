# @Logger
from nlp_model_gen.packages.logger.Logger import Logger

# @Vendors
from nlp_model_gen.packages.modelManager.ModelManagerController import ModelManagerController
from nlp_model_gen.packages.trainingModule.ModelTrainingController import ModelTrainingController

class ApplicationModuleController:
    def __init__(self):
        self.__model_manager = ModelManagerController()
        self.__model_trainer = ModelTrainingController()

    def analyse_text(self, model_id, text, only_positives=False):
        """
        Analiza un texto aplicandole el modelo solicitado. El modelo debe existir.

        :model_id: [String] - Id del modelo a utilizar.

        :text: [String] - Texto a analizar.

        :only_positives: [boolean] - Si esta activado, devuelve solo los resultados positivos.

        :return: [List(Dict)] - Resultados del analisis, None si ha ocurrido un error.
        """
        if not self.__model_manager.is_ready():
            Logger.log('L-0356')
            return None
        return self.__model_manager.analyze_text(model_id, text, only_positives)

    def submit_training_example(self, model_id, example):
        """
        Provee de un ejemplo de entrenamiento. El mismo será agregado al sistema si cumple con 
        las validaciones de schema.

        :model_id: [String] - Id del modelo para el cual se provee el ejemplo.

        :example: [Dict] - Ejemplo de enetranamiento, se trata de un diccionario con dos partes:
        una oración y un arreglo que contiene entidades y su posición en la oración.

        :return: [boolean] - True si el ejemplo fue agregado exitosamente, False en caso 
        contrario.
        """
        pass

    def get_available_tagging_entities(self):
        """
        Devuelve el listado de la entidades disponibles para etiquetar entidades en los ejemplos
        de entrenamiento.

        :return: [List(Dict)] - Lista con todas las entidades posibles.
        """
        pass
