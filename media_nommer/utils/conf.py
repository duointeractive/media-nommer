"""
Settings-related classes and helper methods. feederd and scanvegerd both
make use of these.
"""
from media_nommer.utils.exceptions import BaseException

class SettingsStore(object):
    """
    A really basic Python object that stores all of the settings from which
    feederd runs on. Settings are just attributes on this object, and are
    all uppercase.
    """
    def __init__(self, default_settings):
        """
        Pull the default settings at load time. Later on, the feederd Twisted 
        plugin over-writes these values with the user's settings 
        where applicable.
        """
        self.update_settings_from_module(default_settings)

    def update_settings_from_module(self, settings_module):
        """
        Sets attributes on this object based on the setting found in the
        given 'settings_module' module.
        
        :param settings_module: The settings  module to update from.
        """
        for setting in dir(settings_module):
            if setting == setting.upper():
                setattr(self, setting, getattr(settings_module, setting))
                
class NoConfigFileException(BaseException):
    """
    Raised when a feederd config module can't be found.
    """
    pass
