import unittest
from media_nommer.utils.conf import SettingsStore

class FakeSettingsObj(object):
    SOME_SETTING = 1

class SettingsTests(unittest.TestCase):
    def setUp(self):
        self.fake_defaults = FakeSettingsObj()
        self.settings = SettingsStore(self.fake_defaults)

    def test_overriding(self):
        """
        Tests overriding default settings with the user-specified settings.
        """
        # Pretend that this is the global default for some arbitrary setting.
        self.settings.SOME_SETTING = 1
        # Pretend like this is the user's settings module.
        user_vals = FakeSettingsObj()
        # The user has changed some setting to a non-default value.
        user_vals.SOME_SETTING = 2
        user_settings = SettingsStore(user_vals)
        # Now load the user's settings over the defaults, like the daemon does.
        self.settings.update_settings_from_module(user_settings)
        # Make sure the new setting matches the user's values.
        self.assert_(self.settings.SOME_SETTING == user_settings.SOME_SETTING)
