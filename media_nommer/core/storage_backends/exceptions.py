"""
Storage backend exceptions
"""
class StorageException(Exception):
    """
    A generic Storage backend-related exception. Try to be more specific in your 
    code, just use this as a parent class.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class InfileNotFoundException(StorageException):
    """
    Raised by storage backends when the given source_path (the media to encode)
    cannot be found. 
    """
    pass