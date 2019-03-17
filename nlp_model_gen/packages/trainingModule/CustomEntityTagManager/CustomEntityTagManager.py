# @Classes
from ..CustomEntity.CustomEntity import CustomEntity

class CustomEntityTagManager:
    def __init__(self):
        self.__custom_entities = list([])
        self.__init_suscces = False
        self.__init()
    

    def __init(self):
        """
        Inicializa el administrador de tags personalizados.
        """
        pass
    
    def retry_init(self):
        """
        Reintenta la inicialización del administrados
        """
        self.__init()

    def add_custom_entity(self, name, description):
        """
        Agrega un nuevo tag personalizado. El tag no debe existir previamente.

        :name: [String] - Nombre del nuevo tag (actúa como identificador).

        :description: [String] - Descripción del nuevo tag.

        :return: [boolean] - True si el nuevo tag se ha agregado con exito, False en 
        contario.
        """
        pass
    
    def edit_custom_tag_entity(self, name, description):
        """
        Edita un tag personalizado. El tag debe existir, solamente se puede modificar 
        la descripción.

        :name: [String] - Nombre del tag a actualizar.

        :description: [String] - Descripción actualizada del tag.

        :return: [boolean] - True si la edición se realizó con exito, False en caso 
        contrario.
        """
        pass
    
    def validate_tag(self, name):
        """
        Valida si existe un tag válido con el nombre indicado.

        :name: [String] - Nombre del tag a buscar.

        :return: [boolean] - True si existe un tag válido con el nombre indicado, False
        en caso contrario
        """
        pass

    def get_available_entities(self):
        """
        Retorna un listado con todas las entidades personalizadas existentes.

        :return: [List(CustomEntity)] - Listado con las entidades personalizadas existentes.
        """
        pass
