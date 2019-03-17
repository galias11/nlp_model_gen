class TrainExample:
    def __init__(self, example_id, sentence, tags, example_type, status):
        self.__example_id = example_id
        self.__sentence = sentence
        self.__tags = tags
        self.__example_type = example_type
        self.__status = status

    def get_example_id(self):
        self.__example_id

    def get_sentece(self):
        self.__sentence

    def get_tags(self):
        self.__tags

    def get_example_type(self):
        self.__example_type

    def get_status(self):
        self.__status

    def apply(self):
        """
        Cambia el estado del ejemplo a aplicado.
        """
        pass

    def approve(self):
        """
        Cambia el estado del ejemplo a aprobado.
        """
        pass

    def reject(self):
        """
        Cambia el estado del ejemplo a rechazado.
        """
        pass

    def to_dict(self):
        """
        Obtiene un diccionario a partir de los datos del ejemplo de entrenamiento.

        :return: [Dict] - Diccionario con la información del ejemplo de entrenamiento.
        """
        return {
            'id': self.get_example_id(),
            'sentence': self.get_sentece(),
            'tags': self.get_sentece(),
            'type': self.get_example_type(),
            'status': self.get_status()
        }
