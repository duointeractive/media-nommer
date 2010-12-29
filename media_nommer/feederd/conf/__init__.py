"""
Import the :py:obj:`media_nommer.feederd.conf.settings` object in this module to get the master list of 
global settings for feederd. This involves pulling the default values, then
overriding them with the user's settings.

.. tip:: Keep in mind that these settings and this module are only import
         to feederd, not the rest of media-nommer's components.
"""
from media_nommer.feederd.conf import default_settings

class SettingsStore(object):
    """
    A really basic Python object that stores all of the settings from which
    feederd runs on. Settings are just attributes on this object, and are
    all uppercase.
    """
    def __init__(self):
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


settings = SettingsStore()
"""
This is the object you'll want to import to get at the settings values.
They are attributes on this object, and are all uppercase.
"""
