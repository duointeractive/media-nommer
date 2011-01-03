"""
Import the :py:obj:`media_nommer.scavengerd.conf.settings` object in this module 
to get the master list of global settings for scavengerd. This involves pulling 
the default values, then overriding them with the user's settings.

.. tip:: Keep in mind that these settings and this module are only import
         to feederd, not the rest of media-nommer's components.
"""
from media_nommer.scavengerd.conf import default_settings
from media_nommer.utils.conf import SettingsStore

settings = SettingsStore(default_settings)
"""
This is the object you'll want to import to get at the settings values.
They are attributes on this object, and are all uppercase.
"""
