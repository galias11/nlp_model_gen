GENERIC_ERROR = {
    'error_code': 'E-0001', 
    'description': 'Error generico', 
    'source': {'class': 'N/A', 'method': 'N/A'},
    'log': None
}
ERROR_DATA = {
    'E-0002': {
        'description': 'Error al obtener colección de datos en la base de datos',
        'source': {'class': '', 'method': 'db_check_collection'},
        'log': 'L-0085'
    },
    'E-0003': {
        'description': 'Error al obtener elementos de la base de datos',
        'source': {'class': '', 'method': 'db_get_item'},
        'log': 'L-0086'
    },
    'E-0004': {
        'description': 'Error al obtener elementos de la base de datos',
        'source': {'class': '', 'method': 'db_get_items'},
        'log': 'L-0087'
    },
    'E-0005': {
        'description': 'Error al insertar elementos en la base de datos',
        'source': {'class': '', 'method': 'db_insert_item'},
        'log': 'L-0088'
    },
    'E-0006': {
        'description': 'Error al insertar elementos en la base de datos',
        'source': {'class': '', 'method': 'db_insert_items'},
        'log': 'L-0089'
    },
    'E-0007': {
        'description': 'Error al actualizar elementos en la base de datos',
        'source': {'class': '', 'method': 'db_update_item'},
        'log': None
    },
    'E-0008': {
        'description': 'Error al actualizar elementos en la base de datos',
        'source': {'class': '', 'method': 'db_update_many'},
        'log': None
    },
    'E-0009': {
        'description': 'Error al eliminar elemento de la base de datos',
        'source': {'class': '', 'method': 'db_delete_item'},
        'log': 'L-0090'
    },
    'E-0010': {
        'description': 'Error al eliminar elementos de la base de datos',
        'source': {'class': '', 'method': 'db_delete_items'},
        'log': 'L-0091'
    },
    'E-0011': {
        'description': 'Error al eliminar colección de la base de datos',
        'source': {'class': '', 'method': 'db_drop_collection'},
        'log': 'L-0092'
    },
    'E-0012': {
        'description': 'Error al procesar operación en batch',
        'source': {'class': '', 'method': 'db_batch_operation'},
        'log': 'L-0093'
    },
    'E-0013': {
        'description': 'Error al leer archivo JSON',
        'source': {'class': '', 'method': 'load_json_file'},
        'log': 'L-0357'
    },
    'E-0014': {
        'description': 'Error al escribir archivo JSON',
        'source': {'class': '', 'method': 'overwrite_json_file'},
        'log': 'L-0358'
    },
    'E-0015': {
        'description': 'Error al escribir archivo JSON',
        'source': {'class': '', 'method': 'remove_dir'},
        'log': 'L-0083'
    },
    'E-0016': {
        'description': 'Error al escribir archivo',
        'source': {'class': '', 'method': 'dictionary_to_disk'},
        'log': 'L-0359'
    },
    'E-0017': {
        'description': 'Error al obtener archivos',
        'source': {'class': '', 'method': 'get_files_in_dir'},
        'log': 'L-0360'
    },
    'E-0018': {
        'description': 'Error al copiar archivos',
        'source': {'class': '', 'method': 'copy_file'},
        'log': 'L-0361'
    },
}
