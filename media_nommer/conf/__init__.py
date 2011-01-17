"""
Import the :py:obj:`media_nommer.conf.settings` object in this module to 
get the master list of global settings for feederd, ec2nommerd, and optionally,
scavengerd. This involves pulling the default values, then overriding them with 
the user's settings.

.. tip:: These settings do not apply to the client library.
"""
from media_nommer.conf import settings

def update_settings_from_module(settings_module):
    """
    Given another module with settings in it (usually the user-specified
    settings), override the defaults with the given values.
    
    :param module settings_module: A module with settings as upper-case
        attributes set.
    """
    for setting in dir(settings_module):
        if setting == setting.upper():
            setattr(settings, setting, getattr(settings_module, setting))
