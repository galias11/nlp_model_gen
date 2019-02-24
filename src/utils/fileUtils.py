# @Vendors
import os
import json
import shutil

# @Constants
from src.constants.constants import DIR_PATH_SEPARATOR, PATH_SEPARATOR

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

def dictionary_to_disk(path, dictionary):
    """
    Guarda un diccionario a un archivo en disco.

    :param path: ruta absoluta o relativa al archivo a crear.

    :param dictionary: diccionario a guardar.
    """
    arch = open(path, 'w')
    arch.write(json.dumps(dictionary))
    arch.close()

def create_dir_if_not_exist(path):
    """
    Crea un directorio con el path pasado como parametro si es que no existe.

    :param path: ruta absoluta o relativa del directorio.
    """
    try:
        os.stat(path)
    except:
        os.mkdir(path)

def build_path(base_dir, file_name, extension=''):
    """
    Construye un path a partir de un directorio base y un nombre para el directorio.

    :base_dir: [String] - Directorio base.

    :dir_name: [String] - Nombre del directorio a crear.

    :return: [String] - Ruta creada.
    """
    return base_dir + DIR_PATH_SEPARATOR + file_name + extension

def get_files_in_dir(root_path, extension):
    """
    Devuelve una colección de todos los archivos dentro de un directorio con la extensión
    requerida.

    :root_path: [String] - Ruta raiz del directorio de búsqueda.

    :extensión: [String] - Extensión deseada para los archivos.

    :return: [List(File)] - Lista con los punteros a cada uno de los archivos.
    """
    files = list([])
    for file in os.scandir(root_path):
        if os.path.isdir(file):
            files.extend(get_files_in_dir(file.path, extension))
        if file.path.endswith(extension):
            files.append(file.path)
    return files

def copy_file(source, destination):
    """
    Copia el archivo en el path "source" al directorio indicado en el path "desitination".
    Destination debe ser un directorio.

    :source: [String] - Ruta al archivo a copiar.

    :destination: [String] - Ruta a donde copiar el archivo.
    """
    shutil.copyfile(source, destination)
    