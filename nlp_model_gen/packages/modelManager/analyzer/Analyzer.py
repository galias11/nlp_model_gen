class Analyzer:
    __rule_set: None

    def __init__(self, rule_set):
        self.__rule_set = rule_set

    def analyze_token(self, token):
        """
        Utiliza un rule set para analizar un token. Si el token analizado
        se detecta como un positivo, se actualiza el mismo para indicar la
        detección.

        :token: [Token] - Token a a analizar.
        """
        if self.__rule_set is None:
            return
        for category in self.__rule_set:
            if token.get_base_form() in category['lemma_list']:
                token.set_theme_detected(category['identifier'], category['alert_message'])
                return
        