# @Classes
from ..TrainExample.TrainExample import TrainExample

class ModelTrainData:
    def __init__(self, model_id, model_name, training_examples_data):
        self.__model_id = model_id
        self.__model_name = model_name
        self.__training_examples = list([])
        for example_data in training_examples_data:
            example = TrainExample(example_data['id'], example_data['sentence'], example_data['tags'], example_data['type'], example_data['status'])
            self.__training_examples.append(example)
    
    def get_approved_examples(self):
        """
        Devuelve un listado con los ejemplos de entrenamiento aprobados para el modelo.

        :return: [List(TrainExample)] - Listado de los ejemplos de entrenamiento aprobados.
        """
        pass

    def get_rejected_examples(self):
        """
        Devuelve un listado de los ejemplos rechazados para el modelo.

        :return: [List(TrainExample)] - Listado de los ejemplos de entrenamiento rechazados.
        """
        pass

    def get_pending_examples(self):
        """
        Devuelve un listado de los ejemplos pendientes de decisión para el modelo.

        :return: [List(TrainExample)] - Listado de los ejemplos de entrenamiento pendientes
        de definir su aprobación.
        """
        pass

    def get_examples_history(self):
        """
        Devuelve un listado completo de todos los ejemplos aplicados al modelo.

        :return: [List(TrainExample)] - Listado de todos los ejemplos aplicados al modelo.
        """
        pass
