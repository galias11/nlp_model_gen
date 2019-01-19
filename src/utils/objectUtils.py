# Utilidades para trabajar con diccionarios.

def fillDict(dict, keys):
    """
    Busca las keys especificadas en un diccionario y devuelve las keys que matcheen
    o None en su defecto

    :dict: diccionario sobre el que iterar

    :keys: claves requeridas

    :return: lista con todas las claves que cumplen la condición
    """
    return [dict[k] if k in dict.keys() else None for k in keys]

def destructure(dict, keys):
    """
    Simula el comportamiento de una asignación por destructuración de js.

    :dict: diccionrio sobre el cual se buscaran las claves

    :keys: claves requeridas

    :return: Diccionario con totas las claves que se encuentran
    """
    for key in keys:
        if key.__name__ in dict.keys():
            key = dict[key.__name__]

def get_elements_from_dict(dict, exceptions):
    """
    Devuelve todos los elementos de un diccionario con excepción de las claves
    especificadas como excepción.

    :dict: diccionario sobre el cual obtener las claves

    :keys: claves requeridas

    :return: lista con todas las claves que cumplen la condición
    """
    keys = dict.keys()
    return [dict[key] if key in keys else None and key not in exceptions for key in keys]

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]