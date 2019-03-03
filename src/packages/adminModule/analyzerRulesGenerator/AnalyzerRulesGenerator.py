

class AnalyzerRulesGerator:
    def __init__(self):
        pass

    def __create_category_rule_set(self, category):
        """
        Genera un set de reglas para una determinada categoria de las excepciones
        al tokenizer.

        :category: [Dict] - Objeto que contiene las caracteristicas de la excepción 
        para la categoria.

        :return: [Dict] - Set de reglas para el analizador.
        """
        return {
            'identifier': category['name'],
            'alert_message': category['alert_message'],
            'lemma_list': category['dictionary']
        }

    def create_analyzer_rule_set(self, tokenizer_exceptions):
        """
        A partir de un set de excepciones al tokenizer crea un set de reglas
        para el analizador de textos.

        :tokenizer_exceptions: [List] - Arreglo que contiene todas las excepciones 
        para el modelo a crear.

        :return: [List] - Set de reglas para el analizador.
        """
        try:
            rule_set = list([])
            noun_categories = tokenizer_exceptions['nouns']
            for key in noun_categories.keys():
                rule_set.append(self.__create_category_rule_set(noun_categories[key]))
            verb_categories = tokenizer_exceptions['verbs']
            for key in verb_categories.keys():
                rule_set.append(self.__create_category_rule_set(verb_categories[key]))
            return rule_set
        except:
            return None
