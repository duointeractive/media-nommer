"""
Tests for the storage backends and support classes.
"""
import os
import unittest
import tempfile
from media_nommer.core.storage_backends.http import HTTPBackend
from media_nommer.utils.testing_utils import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

class HTTPBackendTests(unittest.TestCase):
    """
    Tests for the HTTPBackend class.
    """
    def test_http_download(self):
        """
        Tests an HTTP download.
        """
        storage = HTTPBackend
        fobj = tempfile.NamedTemporaryFile()
        file_uri = 'http://s3.amazonaws.com/ligonier-media/full_res_30s_test.master.mp4'
        storage.download_file(file_uri, fobj)
        self.assertEqual(os.path.getsize(fobj.name), 6909952)


class S3BackendTests(unittest.TestCase):
    """
    Tests for the S3Backend class.
    """
    def test_s3_download(self):
        """
        Tests an S3 download.
        """
        storage = S3Backend
        fobj = tempfile.NamedTemporaryFile()
        file_uri = 's3://%s:%s@nommer_in/roving_web.wmv' % (
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        storage.download_file(file_uri, fobj)