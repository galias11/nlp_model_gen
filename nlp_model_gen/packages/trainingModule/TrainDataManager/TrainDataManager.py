# @Classes
from ..CustomEntityTagManager.CustomEntityTagManager import CustomEntityTagManager
from ..ModelTrainData.ModelTrainData import ModelTrainData

class TrainDataManager:
    def __init__(self):
        self.__custom_entity_manager = CustomEntityTagManager()
        self.__models = list([])
        self.__init_success = False
        self.__init()


    def __init(self):
        """
        Inicializa el modulo.
        """
        pass

    def __validate_example(self, example):
        """
        Valida un ejemplo de entrenamiento.

        :example: [Dict] - Ejemplo de entrenamiento a validar.

        :return: [boolean] - True si el ejemplo es válido. False en caso contrario.
        """
        pass
    
    def retry_init(self):
        """
        Reintenta la inicialización del módulo.
        """
        self.__init()

    def add_training_example(self, example):
        """
        Agrega un nuevo ejemplo de entrenamiento. El ejemplo debe ser válido.

        :example: [Dict] - Datos del ejemplo de entrenamiento.

        :return: [boolean] - True si el ejemplo es válido, False en caso contrario.
        """
        pass

    def approve_example(self, example_id):
        """
        Aprueba el ejemplo de entrenamiento identificado on el id solicitado. El 
        ejemplo debe existir y no estar ya aprobado o aplicado.

        :example_id: [int] - Id del ejemplo de entrenamiento.

        :return: [boolean] - True si el ejemplo fue aprobado, False en caso contrario.
        """
        pass

    def discard_example(self, example_id):
        """
        Rechaza el ejemplo de entrenamiento. El ejemplo solicitado debe existir y no 
        estar ya rechazado o aplicado.

        :example_id: [int] - Id del ejemplo de entrenamiento.

        :return: [boolean] - True si el ejemplo fue rechazado, False en caso contrario.
        """
        pass

    def get_pending_examples(self):
        """
        Retorna un listado con todos los ejemplos que tienen su aprobación / rechazo aún
        pendiente.

        :return: [List] - Lista de los ejemplos pendientes de una decisión.
        """
        pass

    def get_approved_examples(self):
        """
        Retorna un listado con todos los ejemplos aprobados.

        :return: [List] - Lista de los ejemplos aprobados.
        """
        pass

    def add_custom_entity(self, name, description):
        """
        Agrega una nueva entidad personalizada para el NER. No debe existir previamente una
        entidad ya registrada con el nombre deseado.

        :name: [String] - Nombre de la entidad.

        :description: [String] - Descripcion de la entidad.

        :return: [boolean] - True si la entidad ha sido agregada exitosamente, False en caso
        contrario.
        """
        pass

    def edit_custom_entity(self, name, description):
        """
        Edita la descripcioón de una entidad personalizada para el NER. La entidad debe existir
        previamente.

        :name: [String] - Nombre de la entidad.

        :description: [String] - Nueva descripción de la entidad.

        :return: [boolean] - True si la entidad ha sido editada correctamente, False en caso
        contrario.
        """
        pass

    def get_available_entities(self):
        """
        Devuelve un listado con todas las entidades personalizadas disponibles.

        :return: [List] - Listado de todas las entidades personalizadas disponibles.
        """
        pass
