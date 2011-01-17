"""
Some logging configuration and shortcut methods.
"""
from twisted.python import log

def debug(message):
    """
    Shortcut to logging a debug message through Twisted's logging module.
    
    :param str message: The message to log.
    """
    log.msg(message)

def info(message):
    """
    Shortcut to logging an info message through Twisted's logging module.
    
    :param str message: The message to log.
    """
    log.msg(message)

def warning(message):
    """
    Shortcut to logging a warning message through Twisted's logging module.
    
    :param str message: The message to log.
    """
    log.msg(message)

def error(message_or_obj=None):
    """
    This isn't really a shortcut, but it's here for the sake of consistency.
    If no message or object is specified, any currently raised exceptions
    will have their traceback logged.
    
    :param message_or_obj: Either a string, an object (to be repr'd), or
        nothing (if this is called within an 'except' statement) to print a
        traceback to the observer.
    """
    log.err(message_or_obj)
