"""
This module contains settings-related things that are used by 
:doc:`../ec2nommerd` and :doc:`../feederd`. You will most likely be interested 
in the :py:mod:`settings <media_nommer.conf.settings>` 
module within this one, as that's where all of the settings and their 
values reside.

When the :doc:`../ec2nommerd` and :doc:`../feederd` Twisted_ plugins start,
they use the :py:func:`update_settings_from_module` to override the defaults
in the :py:mod:`settings <media_nommer.conf.settings>` module with those
specified by the user, typically via a user-provided module named 
``nomconf.py`` (though that name can change with command line arguments).

If you need access to settings, simply import the global settings like this:

.. code-block:: python

    from media_nommer.conf import settings
"""
from media_nommer.conf import settings

def update_settings_from_module(settings_module):
    """
    Given another module with settings in uppercase variables on the
    module, override the defaults in 
    :py:mod:`media_nommer.conf.settings` with the values from the given
    module.
    
    :param module settings_module: A module with settings as upper-case
        attributes set. This is typically ``nomconf.py``, although the user
        can elect to name them something else.
    """
    for setting in dir(settings_module):
        if setting == setting.upper():
            setattr(settings, setting, getattr(settings_module, setting))
