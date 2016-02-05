class YomError(Exception):
    """ Common Yom exception class """
    pass


class YomConnectionError(YomError):
    """ Invalid response from Yandex server """


class YomContentError(YomError):
    """ Invalid data on server """
    pass


class YomValidationError(YomError):
    """ Invalid input data """
    pass
