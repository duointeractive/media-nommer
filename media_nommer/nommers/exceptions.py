"""
General exceptions that are generally useful for all/most Nommer sub-classes.
"""
class NommerException(Exception):
    """
    A generic Nommer-related exception. Try to be more specific in your code,
    just use this as a parent class.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class NommerConfigException(NommerException):
    """
    Raise this when there is a configuration error with a Nommer.
    """
    pass
