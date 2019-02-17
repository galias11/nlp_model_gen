# @Vendors
import os
import json
import shutil

# @Constants
from src.constants.constants import PATH_SEPARATOR

def load_json_file(path_from_root):
    """
    Lee el contenido de un archivo a partir de la ruta relativa a la raíz
    y devuelve su contenido como un diccionario.

    :path_from_root: cadena con la ruta relativa a la raíz.

    :return: diccionario conteniendo el contenido del archivo json
    """
    with open(path_from_root) as f:
        parsedDict = json.loads(f.read())
    f.close()
    return parsedDict

def overwrite_json_file(path_from_root, content):
    """
    Sobreescribe el archivo indicado con el contenido del diccionario recibido.

    :path_from_root: cadena con la ruta relativa a la raíz.

    :content: diccionario con el contenido a escribir en el archivo.
    """
    file = open(path_from_root, 'w')
    file.write(content)

# @Paths
paths = load_json_file('paths.json')

def get_path(element):
    """
    A partir de un elemento especificado en el archivo de rutas obtiene la
    ruta relativa desde la raíz al recurso.

    :element: elemento perteneciente a la lista de rutas.

    :return: cadena conteniendo la ruta relativa desde la raíz al recurso
    """
    path_components = element.split(PATH_SEPARATOR)
    if len(path_components) == 2 :
        path_from_root = paths[path_components[0]][path_components[1]]
        return path_from_root
    return None

def load_dict_from_json(document):
    """
    A partir de un documento especificado en la lista de documentos, obtiene
    un diccionario a partir del json contenido en dicho archivo.

    :document: documento a obtener de la lista de documentos

    :return: diccionario construido a partir del json contenido en el archivo
    """
    path_from_root = get_path(document)
    if path_from_root is not None:
        return load_json_file(path_from_root)
    return {}

def replace_file(document, content):
    """
    Sobre escribe un archivo con el contenido especificado.

    :documento: documento a obtener de la lista de documentos

    :content: diccionario con el contenido a escribir en el archivo.
    """
    path_from_root = get_path(document)
    if path_from_root is not None:
        overwrite_json_file(path_from_root, content)

def check_dir_existence(path):
    """
    Verifica la existencia de un directorio (especificado en el parametro path). Valida no solo que el archivo 
    exista sino que también sea un directorio.

    :path: [String] - Ruta relativa al directorio.

    :return: [boolean] - True si el directorio existe, false en caso contrario
    """
    return os.path.exists(path) and os.path.isdir(path)

def remove_dir(path):
    """
    Elimina el directorio indicado en path del disco.

    :path: [String] - Ruta relativa al directorio.

    :return: [boolean] - True si el borrado se realizo con exito, False en caso contrario.
    """
    try:
        shutil.rmtree(path)
        return True
    except:
        return False