# @Classes
from nlp_model_gen.packages.adminModule.AdminModuleController import AdminModuleController
from nlp_model_gen.packages.taskManager.TaskManager import TaskManager

class SystemController:
    def __init__(self):
        self.__admin_module = AdminModuleController()
        self.__task_manager = TaskManager()

    def generate_model(self, model_id, model_name, description, author, tokenizer_exceptions, max_dist):
        """
        Crea un nuevo modelo para el análisis de textos.

        :model_id: [String] - Id a asignar al nuevo modelo, el id se correspondera con el
        nombre que tendrá el directorio donde se guarde el modelo.

        :model_name: [String] - Nombre del modelo a crear.

        :description: [String] - Descripción del modelo.

        :author: [String] - Nombre del autor del modelo.

        :tokenizer_exceptions: [Dict] - Set de datos (semilla) que incluyen los datos
        necesarios para crear el modelo.

        :max_dist: [int] - Distancia de demerau levenstein máxima para las deformaciónes del
        modelo.

        :return: [Dict] - Diccionario con el detalle de los resultados de la operación.
        """
        pass

    def delete_word_processor_theme(self, module_key, theme_name):
        """
        Elimina un tema para uno de los componentes del modulo de procesamiento de palabras.
        El tema debe existir y no puede haber ninguna tarea de creación de modelo pendiente o en
        ejecución al momento de realizar el borrado (solo si el tema indicado es el tema activo).

        :module_key: [String] - Clave del modulo sobre el cual se borrará el tema.

        :theme_name: [String] - Nombre del tema a borrar.

        :return: [Dict] - Diccionario con el detalle de los resultados de la operación.
        """
        pass

    def update_theme_conjugator_exceptions(self, theme_name, exception_key, exception_data):
        """
        Actualiza una excepción para un tema particular del conjugador. La excepción y el tema
        deben existir. Además, no podrá haber una tarea de creación de modelo pendiente o en 
        ejecución (solo si el tema indicado es el tema activo).

        :theme_name: [String] - Nombre del tema del conjugador a modificar.

        :exception_key: [String] - Clave de la excepción a actualizar.

        :exception_data: [Dict] - Diccionario con la nueva configuración de la excepción.

        :return: [Dict] - Diccionario con el detalle de los resultados de la operación.
        """
        pass

    def update_word_processor_config_theme(self, module_key, theme_name, config_mod, irregular_groups_mod=None):
        """
        Actualiza / edita un tema de configuración para un componente particular del conjugador. La
        tanto el modulo como el tema deben existir. Además, no puede existir una tarea de creación de
        modelo pendiente o en ejecución al momento de ejecutar esta tarea (solo si el tema indicado es 
        el tema activo)

        :module_key: [String] - Clave del modulo a actualizar.

        :theme_name: [String] - Nombre del tema a actualizar.

        :config_mod: [Dict] - Campos a actualizar, solo son necesarios los campos a modificar.

        :irregular_groups_mod: [Dict] - Campos a actualizar de los grupos irregulares, solo son necesarios
        los campos a actualizar. Solo es requerido cuando se actualiza el modulo de conjugación.

        :return: [Dict] - Diccionario con el detalle de los resultados de la operación.
        """
        pass

    def set_word_processor_active_theme(self, module_key, theme_name):
        """
        Cambia el tema activo para el modulo de procesamiento de palabras, tanto el modulo como el
        tema deben existir. No se podrá realizar esta operación si hay una tarea de creación de modelo
        pendiente o en ejecución.

        :module_key: [String] - Clave del modulo a actualizar.

        :theme_name: [String] - Nombre del tema a utilizar.

        :return: [Dict] - Diccionario con el detalle de los resultados de la operación.
        """
        pass

    def get_word_processor_active_themes(self): 
        """
        Devuelve un objeto con los temas activos para cada modulo del conjugador de palabras

        :return: [Dict] - Diccionario con el detalle de los resultados de la operación.
        """
        pass

    def add_theme_conjugator_exceptions(self, theme_name, exceptions):
        """
        Agrega un set de excepciones a un tema del conjugador. El tema debe existir y, si fuera
        el tema activo en el momento de realizar la operación, no puede haber una operación de 
        creación de modelo pendiente o activa. Además no deben haber excepciones ya registradas
        para las nuevas excepciones a agregar.

        :theme_name: [String] - Nombre del tema.

        :exceptions: [List(Dict)] - Lista de excepciones a agregar para el tema de configuración.

        :return: [Dict] - Diccionario con el detalle de los resultados de la operación.
        """
        pass

    def add_word_processor_config_theme(self, module_key, theme_name, configs, irregular_groups=None):
        """
        Agrega un nuevo tema de configuración para alguno de los submodulos del modulo de 
        procesamiento de palabras. El submodulo debe existir y no debe existir un tema con
        el nombre solicitado ya registrado.

        :module_key: [String] - Clave del submodulo.

        :theme_name: [String] - Nombre del nuevo tema.

        :configs: [Dict] - Configuración del nuevo tema, debe cumplir con la validación de
        schema para el submodulo particular.

        :irregular_groups: [Dict] - Configuración de los grupos irregulares. Solo es necesario
        para los nuevos temas del modulo de conjugación.

        :return: [Dict] - Diccionario con el detalle de los resultados de la operación.
        """
        pass

    def get_word_processor_available_configs(self, module_key):
        """
        Devuelve un listado con los temas de configuración disponibles para el submodulo
        solicitado del modulo de procesamiento de palabras.

        :module_key: [String] - Clave del submodulo.

        :return: [Dict] - Diccionario con el detalle de los resultados de la operación.
        """
        pass

    def delete_model(self, model_id):
        """
        Elimina un modelo. El modelo debe existir, además esta operación no podrá realizarse si
        hay alguna tarea de entrenamiento o análisis de texto pendiente para el modelo.

        :model_id: [String] - Id del modelo.

        :return: [Dict] - Diccionario con el detalle de los resultados de la operación.
        """
        pass

    def edit_model_data(self, model_id, new_model_name, new_description):
        """
        Edita los datos del modelo identificado con el id solicitado. El modelo debe existir.
        No hay restricciones para la realización de esta operación.

        :model_id: [String] - Id del modelo a editar.

        :new_model_name: [String] - Nuevo nombre a aplicar al modelo (si no es provisto se
        mantendrá el actual).

        :new_description: [String] - Nueva descripción a aplicar al modelo (si no es provista
        se mantendrá la actual).

        :return: [Dict] - Diccionario con el detalle de los resultados de la operación.
        """
        pass

    def get_available_models(self):
        """
        Devuelve un listado con los modelos disponibles y sus datos.

        :return: [Dict] - Diccionario con el detalle de los resultados de la operación.
        """
        pass

    def approve_training_examples(self, training_examples_list):
        """
        Aprueba un conjunto de ejemplos de entrenamiento. Los ejemplos deben existir.

        :training_examples_list: [List(String)] - Lista de los ids de los ejemplos a aprobar.

        :return: [Dict] - Diccionario con el detalle de los resultados de la operación.
        """
        pass

    def get_submitted_training_examples(self, model_id):
        """
        Obtiene un listado de los ejemplos de entrenamiento existentes para un determinado modelo.

        :model_id: [String] - Id del modelo para el cual obtener los ejemplos.

        :return: [Dict] - Diccionario con el detalle de los resultados de la operación.
        """
        pass

    def submit_training_examples(self, model_id, examples):
        """
        Registra un set de ejemplos de entrenamiento para un modelo particular. El modelo debe existir
        y los ejemplos deben validar con la schema de validación para los ejemplos.

        :model_id: [String] - Id del modelo.

        :examples: [List(Dict)] - Listado de ejemplos. Debe haber al menos un ejemplo.

        :return: [Dict] - Diccionario con el detalle de los resultados de la operación.
        """
        pass

    def analyze_text(self, model_id, text, only_positives=False):
        """
        Analiza un texto utilizando el modelo deseado. El modelo debe existir. Si no se activa el flag
        de solo positivos, se devolverán todos los resultados independientemente de aquellos que se 
        hayan detectado como positivos.

        :model_id: [String] - Id del modelo.

        :text: [String] - Texto a analizar.

        :only_positives: [boolean] - Flag que indica si solo devolver los resultados positivos del 
        análisis con el modelo. Por defecto sera falsa.

        :return: [Dict] - Diccionario con el detalle de los resultados de la operación.
        """
