# Utilidades para trabajar con diccionarios.

# Busca las keys especificadas en un diccionario y devuelve las keys que matcheen
# o None en su defecto
def fillDict(dict, keys):
    return [dict[k] if k in dict.keys() else None for k in keys]
            