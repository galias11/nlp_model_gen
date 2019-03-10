# @Vendors
from abc import ABC, abstractmethod

class Task(ABC):
    def __init__(self):
        pass

    __id = -1
    __status = ''
    __error = { 'active': False, 'code': '', 'description': '' }
    __init_time = -1
    __end_time = -1

    def __init__(self, id):
        self.__id = id

    def get_id(self):
        return self.__id

    def get_status(self):
        return self.__status

    def get_error(self):
        return self.__error

    def get_init_time(self):
        return self.__init_time

    def get_end_time(self):
        return self.__end_time

    def init(self):
        """
        Inicia la tarea.
        """
        pass

    def abort(self):
        """
        Aborta la tarea. Su ejecución no debe haber iniciado para realizar esta operación.
        """
        pass

    def get_task_status_data(self):
        """
        Retorna un resumen de la información de la tarea.

        :return: [Dict] - Diccionario con la inofrmación acerca del estdo de la tarea.
        """
        return {
            'id': self.get_id(),
            'status': self.get_status(),
            'init_time': self.get_init_time(),
            'end_time': self.get_end_time(),
            'error': self.get_error()
        }

    @abstractmethod
    def task_init_hook(self):
        """
        Método que se ejecutará en el template del init de la task de la clase padre.
        """

    @abstractmethod
    def get_task_data(self):
        """
        Retorna los datos de la tarea, debe ser sobreescrito por las subclases
        """
