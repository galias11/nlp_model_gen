class ModelManagerController:
    __models = list([])
    __model_loader = None
    __init_success = False

    def __init__(self):
        pass

    def __initialize(self):
        """
        Inicializa el modulo.
        """

    def __load_spacy(self):
        """
        Carga la libreria de spacy, si el resultado es existo se cambia a true el valor
        de la flag init_success
        """
        pass

    def load_model(self, model_name):
        """
        Carga el modelo requerido en memoria.

        :model_name: [String] - Nombre del modelo.

        :return: [boolean] - True si fue exitoso, false en caso contrario.
        """
        pass

    def get_available_models(self):
        """
        Devuelve una lista de los modelos disponibles y sus caracteristicas.

        :return: [List(Dict)] - Lista de los modelos disponibles y sus caracteristicas.
        """
        pass

    def analyze_text(self, model_name, text):
        """
        Analiza un texto con el modelo solicitado.

        :model_name: [String] - Nombre del modelo a utilizar.

        :text: [String] - Texto a analizar.

        :return: [Dict] - Resultados del análisis.
        """
        pass

    def train_model(self, model_name, training_data):
        """
        Aplica un set de datos de entrenamiento al modelo solicitado.

        :model_name: [String] - Nombre del modelo a entrenar.

        :training_data: [List(Dict)] - Set de datos de entrenamiento.

        :return: [boolean] - True si el proceso ha sido exitoso, False en caso contrario.
        """
        pass

    def create_model(self, model_name, description, author, path, tokenizer_exceptions):
        """
        Crea un nuevo modelo. Crea los datos necesarios y lo guarda tanto en disco como su
        referencia en la base de datos.

        :model_name: [String] - Nombre del modelo.

        :description: [String] - Descripción.

        :author: [String] - Referencia del autor del modelo.

        :path: [String] - Path relativo donde guardar el modelo.

        :tokenizer_exceptions: [List(Dict)] - Lista de excepciones del modulo tokenizer del modelo.

        :return: [boolean] - True si el proceso ha sido exitoso, False en caso contrario.
        """
        pass

    def edit_model(self, model_name, description):
        """
        Permite editar la descripción de un modelo. El modelo debe existir.

        :model_name: [String] - Nombre del modelo.

        :description: [String] - Nueva descripción.

        :return: [boolean] - True si la modificación se ha realizado correctamente, False en caso contrario.
        """
        pass
