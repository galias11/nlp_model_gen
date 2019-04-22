# @Error handler
from nlp_model_gen.packages.errorHandler.ErrorHandler import ErrorHandler

class AnalyzerException:
    def __init__(self, base_form, token_text, enabled):
        self.__base_form = base_form
        self.__token_text = token_text
        self.__enabled = enabled

    def check_exception(self, token_text, base_form):
        """
        Valida si la excepción corresponde con el texto del token y la forma base,
        si esto es asi y, además, la excepción esta activada devuelve True.

        :token_text: [String] - Texto del token (el detectado).

        :base_form: [String] - Forma base que matchea el token.

        :return: [boolean] - True si la forma matchea y además la excepción esta 
        activada.
        """
        return self.match_exception(token_text, base_form) and self.__enabled

    def match_exception(self, token_text, base_form):
        """
        Valida que los datos de una excepción sean coincidentes con los datos de
        esta excepción.

        :token_text: [String] - Texto del token (el detectado).

        :base_form: [String] - Forma base que matchea el token.

        :return: [Boolean] - True si la excepción matchea, False en caso contrario.
        """
        return token_text == self.__token_text and base_form == self.__base_form

    def enable(self):
        """
        Activa la excepción, la misma no debe encontrarse ya activada
        """
        pass

    def disable(self):
        """
        Desactiva la excepción, la misma no debe estar desactivada previamente.
        """
        pass
