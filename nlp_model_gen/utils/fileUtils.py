# @Vendors
import os
import json
import shutil

# @Logger
from nlp_model_gen.packages.logger.Logger import Logger

# @Logger colors
from nlp_model_gen.packages.logger.assets.logColors import ERROR_COLOR

# @Constants
from nlp_model_gen.constants.constants import DEFAULT_REPLACE_WILDCARD, DIR_PATH_SEPARATOR, PATH_SEPARATOR

# @Base cfg
from nlp_model_gen.base import CURRENT_BASE_PATH

def get_absoulute_path(path):
    """
    Devuelve la ruta absoluta para un path relativo al root desde donde se ejecuta
    el paquete.

    :path: [String] - ruta relativa a la raíz del paquete
    """
    return CURRENT_BASE_PATH + DIR_PATH_SEPARATOR + path

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

# @Paths
paths = load_json_file(get_absoulute_path('/paths.json'))

def overwrite_json_file(path_from_root, content):
    """
    Sobreescribe el archivo indicado con el contenido del diccionario recibido.

    :path_from_root: cadena con la ruta relativa a la raíz.

    :content: diccionario con el contenido a escribir en el archivo.
    """
    absolute_path = get_absoulute_path(path_from_root)
    file = open(absolute_path, 'w')
    file.write(content)

def get_path(element):
    """
    A partir de un elemento especificado en el archivo de rutas obtiene la
    ruta relativa desde la raíz al recurso.

    :element: elemento perteneciente a la lista de rutas.

    :return: cadena conteniendo la ruta relativa desde la raíz al recurso
    """
    path_components = element.split(PATH_SEPARATOR)
    if len(path_components) == 2:
        path_from_root = paths[path_components[0]][path_components[1]]
        return path_from_root.replace(DEFAULT_REPLACE_WILDCARD, CURRENT_BASE_PATH)
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

def check_dir_existence(path_from_root):
    """
    Verifica la existencia de un directorio (especificado en el parametro path). Valida no solo que el archivo 
    exista sino que también sea un directorio.

    :path_from_root: [String] - Ruta relativa al directorio.

    :return: [boolean] - True si el directorio existe, false en caso contrario
    """
    absolute_path = get_absoulute_path(path_from_root)
    return os.path.exists(absolute_path) and os.path.isdir(absolute_path)

def remove_dir(path_from_root, is_absolute_path=False):
    """
    Elimina el directorio indicado en path del disco.

    :path_from_root: [String] - Ruta relativa al directorio.

    :return: [boolean] - True si el borrado se realizo con exito, False en caso contrario.
    """
    try:
        if not is_absolute_path:
            absolute_path = get_absoulute_path(path_from_root)
            shutil.rmtree(absolute_path)
        else:
            shutil.rmtree(path_from_root)
        return True
    except Exception as e:
        Logger.log('L-0083', [{'text': e, 'color': ERROR_COLOR}])
        return False

def dictionary_to_disk(path_from_root, dictionary):
    """
    Guarda un diccionario a un archivo en disco.

    :path_from_root: ruta absoluta o relativa al archivo a crear.

    :dictionary: diccionario a guardar.
    """
    absolute_path = get_absoulute_path(path_from_root)
    arch = open(absolute_path, 'w')
    arch.write(json.dumps(dictionary))
    arch.close()

def create_dir_if_not_exist(path_from_root):
    """
    Crea un directorio con el path pasado como parametro si es que no existe.

    :path_from_root: ruta absoluta o relativa del directorio.
    """
    try:
        absolute_path = get_absoulute_path(path_from_root)
        os.stat(absolute_path)
    except:
        os.mkdir(absolute_path)

def build_path(base_dir, file_name, extension='', add_absolute_root=False):
    """
    Construye un path a partir de un directorio base y un nombre para el directorio.

    :base_dir: [String] - Directorio base.

    :dir_name: [String] - Nombre del directorio a crear.

    :add_absolute_root: [boolean] - Indica si se debe adicionar la raiz absoluta. True por defecto

    :return: [String] - Ruta creada.
    """
    root_path = ''
    if add_absolute_root:
        root_path = CURRENT_BASE_PATH + DIR_PATH_SEPARATOR
    return root_path + base_dir + DIR_PATH_SEPARATOR + file_name + extension

def get_files_in_dir(absolute_path, extension):
    """
    Devuelve una colección de todos los archivos dentro de un directorio con la extensión
    requerida.

    :root_path: [String] - Ruta absoluta del directorio de búsqueda.

    :extensión: [String] - Extensión deseada para los archivos.

    :return: [List(File)] - Lista con los punteros a cada uno de los archivos.
    """
    files = list([])
    for file in os.scandir(absolute_path):
        if os.path.isdir(file):
            files.extend(get_files_in_dir(file.path, extension))
        if file.path.endswith(extension):
            files.append(file.path)
    return files

def copy_file(source, destination, is_absolute_path=False):
    """
    Copia el archivo en el path "source" al directorio indicado en el path "desitination".
    Destination debe ser un directorio.

    :source: [String] - Ruta al archivo a copiar.

    :is_absolute_path: [boolean] - Indica si las rutas provistas son absolutas

    :destination: [String] - Ruta a donde copiar el archivo.
    """
    abs_source_path = source
    abs_destination_path = destination
    if not is_absolute_path:
        abs_source_path = get_absoulute_path(source)
        abs_destination_path = get_absoulute_path(destination)
    shutil.copyfile(abs_source_path, abs_destination_path)
    