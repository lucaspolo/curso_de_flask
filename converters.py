from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


class ListConverter(BaseConverter):
    """nome+nome2+nome3+nome..."""

    def to_python(self, value):
        """
            Método reponsável para converter um tipo do Python
        """
        return value.split('+')


    def to_url(self, values):
        """
            Método responsável para converter tipo Python para URL.
            Caso seja uma string ele irá manter, senão irá fazer o join colocando '+' entre os parâmetros
        """
        return '+'.join(
            BaseConverter.to_url(self, item) for item in values
        ) if not isinstance(values, str) else BaseConverter.to_url(self,values)
