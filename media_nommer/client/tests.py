import unittest
from media_nommer.client import connect
from media_nommer.utils.testing_utils import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

class JobSubmitTests(unittest.TestCase):
    def setUp(self):
        self.connection = connect('http://localhost:8001')
        self.source_path = 's3://%s:%s@%s/%s' % (
            AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY,
            'some_bucket',
            'some_file'
        )
        self.dest_path = 's3://%s:%s@%s/%s' % (
            AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY,
            'some_bucket2',
            'some_dir'
        )

    def test_job_submit(self):
        job_opts = {}
        print "COMEBACK", self.connection.job_submit(self.source_path,
                                                     self.dest_path, job_opts)