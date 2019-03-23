# @Constants
from nlp_model_gen.constants.constants import (
    TRAIN_EXAMPLE_STATUS_APPLIED,
    TRAIN_EXAMPLE_STATUS_APPROVED,
    TRAIN_EXAMPLE_STATUS_REJECTED,
    TRAIN_EXAMPLE_STATUS_SUBMITTED
)

class TrainExample:
    def __init__(self, example_id, sentence, tags, example_type, status=TRAIN_EXAMPLE_STATUS_SUBMITTED):
        self.__example_id = example_id
        self.__sentence = sentence
        self.__tags = tags
        self.__example_type = example_type
        self.__status = status

    def get_example_id(self):
        return self.__example_id

    def get_sentece(self):
        return self.__sentence

    def get_tags(self):
        return self.__tags

    def get_example_type(self):
        return self.__example_type

    def get_status(self):
        return self.__status

    def apply(self):
        """
        Cambia el estado del ejemplo a aplicado.
        """
        self.__status = TRAIN_EXAMPLE_STATUS_APPLIED

    def approve(self):
        """
        Cambia el estado del ejemplo a aprobado.
        """
        self.__status = TRAIN_EXAMPLE_STATUS_APPROVED

    def reject(self):
        """
        Cambia el estado del ejemplo a rechazado.
        """
        self.__status = TRAIN_EXAMPLE_STATUS_REJECTED

    def to_dict(self):
        """
        Obtiene un diccionario a partir de los datos del ejemplo de entrenamiento.

        :return: [Dict] - Diccionario con la información del ejemplo de entrenamiento.
        """
        return {
            'id': self.get_example_id(),
            'sentence': self.get_sentece(),
            'tags': self.get_tags(),
            'type': self.get_example_type(),
            'status': self.get_status()
        }
