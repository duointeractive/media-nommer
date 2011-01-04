"""
Import the :py:obj:`media_nommer.conf.settings` object in this module to 
get the master list of global settings for feederd, nommerd, and optionally,
scavengerd. This involves pulling the default values, then overriding them with 
the user's settings.

.. tip:: These settings do not apply to the client library.
"""
from media_nommer.conf import default_settings
from media_nommer.utils.conf import SettingsStore

settings = SettingsStore(default_settings)
"""
This is the object you'll want to import to get at the settings values.
They are attributes on this object, and are all uppercase.
"""
