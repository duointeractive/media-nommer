"""
Contains some general exceptions specific to the nommerd daemon.
"""

class NommerDaemonException(Exception):
    """
    Exception: Serves as the base exception that other service-related 
    exception objects are sub-classed from.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class NoConfigFileException(NommerDaemonException):
    """
    Raised when no configuration file could be found.
    """
    pass
