import unittest
from media_nommer.nommerd.nommers.base_nommer import BaseNommer
from media_nommer.nommerd.nommers.exceptions import NommerConfigException

# This is an example set of settings to make testing a little less repetitive.
EXAMPLE_WORKFLOW_SETTINGS = {
    'NAME': 'test_workflow',
    'DESCRIPTION': 'A test workflow',
    'AWS_ACCESS_KEY_ID': 'XXXXXXXXXXXXXXXXXXXX',
    'AWS_SECRET_ACCESS_KEY': 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY',
    'S3_IN_BUCKET': 'nommer_in',
    'S3_OUT_BUCKET': 'nommer_in',
}

class BaseNommerTests(unittest.TestCase):
    """
    Unit tests for the BaseNommer class, which serves as a foundation for
    the various Nommer classes.
    """
    def test_missing_settings(self):
        """
        Create a BaseNommer with some missing required values.
        """
        # Create a copy so we don't mess up the defaults.
        SETTINGS_WITH_MISSING = EXAMPLE_WORKFLOW_SETTINGS.copy()
        # Simulate a user forgetting a setting by deleting a setting.
        del SETTINGS_WITH_MISSING['S3_OUT_BUCKET']
        # This should raise a NommerConfigException.
        self.assertRaises(NommerConfigException, BaseNommer, SETTINGS_WITH_MISSING)

    def test_good_settings(self):
        """
        This should behave normally, all values have been specified.
        """
        GOOD_SETTINGS = EXAMPLE_WORKFLOW_SETTINGS
        nommer = BaseNommer(GOOD_SETTINGS)

    def test_missing_optional(self):
        """
        Make sure optional settings can be omitted.
        """
        # Create a copy so we don't mess up the defaults.
        SETTINGS_WITH_MISSING = EXAMPLE_WORKFLOW_SETTINGS.copy()
        # Simulate a user forgetting an optional setting.
        del SETTINGS_WITH_MISSING['DESCRIPTION']
        # This should be fine, as DESCRIPTION is optional.
        nommer = BaseNommer(SETTINGS_WITH_MISSING)
