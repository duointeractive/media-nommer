import unittest
import tempfile
from media_nommer.core.storage_backends.s3 import S3Backend
from media_nommer.utils.testing_utils import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

class S3BackendTests(unittest.TestCase):
    def test_s3_download(self):
        """
        Tests an S3 download.
        """
        storage = S3Backend
        fobj = tempfile.NamedTemporaryFile()
        file_uri = 's3://%s:%s@nommer_in/roving_web.wmv' % (AWS_ACCESS_KEY_ID,
                                                            AWS_SECRET_ACCESS_KEY)
        storage.download_file(file_uri, fobj)

    def test_s3_upload(self):
        """
        Tests an S3 download.
        """
        storage = S3Backend
        fobj = tempfile.NamedTemporaryFile(mode='w+b')
        fobj.write('THIS IS A TEST')
        fobj.flush()
        fobj.seek(0)
        file_uri = 's3://%s:%s@nommer_out/upload.test' % (AWS_ACCESS_KEY_ID,
                                                          AWS_SECRET_ACCESS_KEY)
        storage.upload_file(file_uri, fobj)
