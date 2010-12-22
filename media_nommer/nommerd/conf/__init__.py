"""
Import the 'settings' object in this module to get the master list of global
settings for nommerd. This involves pulling the default values, then
overriding them with the user's settings.

Keep in mind that these settings are only important to nommerd.
"""
from media_nommer.nommerd.conf import default_settings

class SettingsStore(object):
    """
    A really basic Python object that stores all of the settings from which
    nommerd runs on. Settings are just attributes on this object, and are
    all uppercase.
    """
    def __init__(self):
        """
        Pull the default settings at load time. Later on, the nommerd Twisted 
        plugin over-writes these values with the user's settings 
        where applicable.
        """
        self.update_settings_from_module(default_settings)

    def update_settings_from_module(self, settings_module):
        """
        Sets attributes on this object based on the setting found in the
        given 'settings_module' module.
        """
        for setting in dir(settings_module):
            if setting == setting.upper():
                setattr(self, setting, getattr(settings_module, setting))

# This is the object you'll want to imoprt to get at the settings values.
# They are attributes on this object, and are all uppercase.
settings = SettingsStore()
