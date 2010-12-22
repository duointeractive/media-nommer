from media_nommer.nommerd.conf import default_settings

class SettingsStore(object):
    def __init__(self):
        print "IMPORTED"
        self.update_from_defaults()

    def update_from_defaults(self):
        for setting in dir(default_settings):
            if setting == setting.upper():
                setattr(self, setting, getattr(default_settings, setting))

    def update_from_user_settings(self, user_settings_module):
        for setting in dir(user_settings_module):
            if setting == setting.upper():
                setattr(self, getattr(global_settings, setting))

settings = SettingsStore()
