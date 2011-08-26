"""
Tests for the storage backends and support classes.
"""
import os
import unittest2
import tempfile
from media_nommer.core.storage_backends.s3 import S3Backend
from media_nommer.core.storage_backends.http import HTTPBackend
from media_nommer.core.storage_backends.file import FileBackend
from media_nommer.utils.testing_utils import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

class HTTPBackendTests(unittest2.TestCase):
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


class S3BackendTests(unittest2.TestCase):
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


class FileBackendTests(unittest2.TestCase):
    """
    Tests for the FileBackend class.
    """
    def test_file_download(self):
        """
        Tests a local file 'download'. All this does is open the source file,
        since media-nommer doesn't modify it in-place. The ``fobj`` that we pass
        is unused.
        """
        storage = FileBackend
        # This will be a fake source file.
        fake_infile = tempfile.NamedTemporaryFile()
        # Path to the fake source file.
        file_uri = 'file://%s' % fake_infile.name
        # This is here for API compatibility, but is unused in this backend.
        fobj = tempfile.NamedTemporaryFile()
        result = storage.download_file(file_uri, fobj)
        self.assertIsInstance(result, file)

    def test_file_upload(self):
        """
        Tests a local file 'upload'. The end result is the encoded temporary
        file is copied to the destination given by the user.
        """
        storage = FileBackend
        # This will be a fake source file.
        fake_encoded_file = tempfile.NamedTemporaryFile()
        # This will represent the user's destination URI.
        fake_dest_file = tempfile.NamedTemporaryFile()
        result = storage.upload_file(fake_dest_file.name, fake_encoded_file)
        self.assertIsInstance(result, basestring)