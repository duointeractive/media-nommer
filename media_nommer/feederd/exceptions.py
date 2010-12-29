"""
Contains some general exceptions specific to the feederd daemon.
"""

class feederdaemonException(Exception):
    """
    Exception: Serves as the base exception that other service-related 
    exception objects are sub-classed from.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class NoConfigFileException(feederdaemonException):
    """
    Raised when a feederd config module can't be found.
    """
    pass
