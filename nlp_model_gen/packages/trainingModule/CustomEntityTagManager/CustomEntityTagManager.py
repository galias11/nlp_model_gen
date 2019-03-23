# @Constants
from nlp_model_gen.constants.constants import CUSTOM_ENTITY_MANAGER_COLLECTION, TRAIN_MANAGER_DB

# @Utils
from nlp_model_gen.utils.dbUtils import db_get_items, db_insert_item, db_update_item

# @Classes
from ..CustomEntity.CustomEntity import CustomEntity

class CustomEntityTagManager:
    def __init__(self):
        self.__custom_entities = list([])
        self.__init_susccess = False
        self.__init()

    def is_ready(self):
        return self.__init_susccess

    def __init(self):
        """
        Inicializa el administrador de tags personalizados.
        """
        try:
            stored_entities = db_get_items(TRAIN_MANAGER_DB, CUSTOM_ENTITY_MANAGER_COLLECTION)
            for stored_entity in stored_entities:
                entity = CustomEntity(stored_entity['name'], stored_entity['description'])
                self.__custom_entities.append(entity)
            self.__init_susccess = True
        except:
            self.__init_susccess = False

    def __check_entity_existence(self, name):
        """
        Valida si ya existe una entidad con el nombre solicitado en el listado
        de entidades disponibles.

        :name: [String] - Nombre de la entidad a buscar

        :return: [boolean] - True si la entidad existe, False en caso contrario
        """
        try:
            next(entity for entity in self.__custom_entities if entity.get_name() == name)
            return True
        except:
            return False
    
    def __get_entity(self, name):
        """
        Obtiene una entidad del listado de entidades personalizades que cumpla con el
        nombre especificada. Devuelve None si la entidad no existe.

        :name: [String] - Nombre de la entidad (identificador)

        :return: [CustomEntity] - Entidad buscada
        """
        try:
            founded_entity = next(entity for entity in self.__custom_entities if entity.get_name() == name)
            return founded_entity
        except:
            return None

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
        if self.__check_entity_existence(name):
            return False
        try:
            db_insert_item(TRAIN_MANAGER_DB, CUSTOM_ENTITY_MANAGER_COLLECTION, {'name': name, 'description': description})
            new_entity = CustomEntity(name, description)
            self.__custom_entities.append(new_entity)
            return True
        except:
            return False
    
    def edit_custom_tag_entity(self, name, description):
        """
        Edita un tag personalizado. El tag debe existir, solamente se puede modificar 
        la descripción.

        :name: [String] - Nombre del tag a actualizar.

        :description: [String] - Descripción actualizada del tag.

        :return: [boolean] - True si la edición se realizó con exito, False en caso 
        contrario.
        """
        entity = self.__get_entity(name)
        if entity is None:
            return False
        if entity.get_description() == description:
            return False
        try:
            updated_entries = db_update_item(TRAIN_MANAGER_DB, CUSTOM_ENTITY_MANAGER_COLLECTION, {'name': name}, {'description': description})
            if updated_entries == 0:
                return False
            entity.set_description(description)
            return True
        except:
            return False
    
    def validate_tag(self, name):
        """
        Valida si existe un tag válido con el nombre indicado.

        :name: [String] - Nombre del tag a buscar.

        :return: [boolean] - True si existe un tag válido con el nombre indicado, False
        en caso contrario
        """
        return self.__check_entity_existence(name)

    def get_available_entities(self):
        """
        Retorna un listado con todas las entidades personalizadas existentes.

        :return: [List(CustomEntity)] - Listado con las entidades personalizadas existentes.
        """
        return self.__custom_entities
