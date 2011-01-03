"""
Exceptions and base classes that are generally useful for other modules.
No module-specific exceptions should reside here!
"""
class BaseException(Exception):
    """
    Serves as the base exception that other media-nommer exception objects
    are sub-classed from.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)