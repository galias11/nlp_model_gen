class DataSanitizer:
    def __init__(self):
        pass

    @staticmethod
    def sanitize_text_for_analysis(text=''):
        """
        Elimina los caracteres no deseados que pueda tener un texto.

        :text: [String] - Texto a preparar.

        :return: [String] - Texto prepatado para el análisis.
        """
        sanitized_text = text.replace('\n', ' ')
        sanitized_text = sanitized_text.replace('\t', ' ')
        return sanitized_text
