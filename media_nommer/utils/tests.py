import unittest
from media_nommer.utils.conf import SettingsStore
from media_nommer.utils.mod_importing import import_class_from_module_string
from media_nommer.utils.uri_parsing import get_values_from_media_uri, InvalidUri

class FakeSettingsObj(object):
    """
    This is used to emulate user-provided settings in 
    SettingTests.test_overriding.
    """
    SOME_SETTING = 1

class SettingsTests(unittest.TestCase):
    def setUp(self):
        """
        Create some settings objects with default settings in them.
        """
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

class ModImportingTests(unittest.TestCase):
    def test_valid_import(self):
        """
        Test an import that should be valid.
        """
        import_class_from_module_string('media_nommer.client.api.APIConnection')

    def test_invalid_import(self):
        """
        Test some invalid imports to make sure exception raising is good.
        """
        self.assertRaises(ImportError, import_class_from_module_string,
                          'media_nommer.client.api.NonExist')
        self.assertRaises(ImportError, import_class_from_module_string,
                          'media_nommer.client.invalid_mod.APIConnection')

class MediaUriParsingTests(unittest.TestCase):
    """
    Tests for media_nommer.feederd.backends.get_values_from_media_uri()
    """
    def test_valid_uri_parsing(self):
        """
        Test a valid URI with most options specified (aside from port).
        """
        valid_uri = 's3://SOMEUSER:SOME/PASS@some_bucket/some_dir/some_file.mpg'
        values = get_values_from_media_uri(valid_uri)

        self.assertEqual(values['protocol'], 's3')
        self.assertEqual(values['username'], 'SOMEUSER')
        self.assertEqual(values['password'], 'SOME/PASS')
        self.assertEqual(values['host'], 'some_bucket')
        self.assertEqual(values['path'], 'some_dir/some_file.mpg')
        self.assertEqual(values.has_key('port'), False)

    def test_valid_uri_nopass_parsing(self):
        """
        Test a valid URI with everything but port and password specified.
        """
        valid_uri = 'http://SOMEUSER@some_host.com/some_dir/some_file.mpg'
        values = get_values_from_media_uri(valid_uri)

        self.assertEqual(values['protocol'], 'http')
        self.assertEqual(values['username'], 'SOMEUSER')
        self.assertEqual(values.has_key('password'), False)
        self.assertEqual(values['host'], 'some_host.com')
        self.assertEqual(values['path'], 'some_dir/some_file.mpg')
        self.assertEqual(values.has_key('port'), False)

    def test_valid_uri_minimal_parsing(self):
        """
        Test a valid URI with a more minimal value.
        """
        valid_uri = 'http://some-hostname.org:80/some_dir/some_file.mpg'
        values = get_values_from_media_uri(valid_uri)

        self.assertEqual(values['protocol'], 'http')
        self.assertEqual(values.has_key('username'), False)
        self.assertEqual(values.has_key('password'), False)
        self.assertEqual(values['host'], 'some-hostname.org')
        self.assertEqual(values['path'], 'some_dir/some_file.mpg')
        self.assertEqual(values['port'], '80')

    def test_valid_uri_no_path_parsing(self):
        """
        If a path is omitted, assume that they're talking about the root path.
        """
        valid_uri = 'http://some-hostname.org:80'
        values = get_values_from_media_uri(valid_uri)
        self.assertEqual(values['path'], '/')

    def test_invalid_uri_no_protocol_parsing(self):
        """
        Test an invalid URI that lacks a protocol.
        """
        invalid_uri = 'some-hostname.org:80/some_dir/some_file.mpg'
        self.assertRaises(InvalidUri, get_values_from_media_uri, invalid_uri)
