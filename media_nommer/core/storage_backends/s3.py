import boto
from media_nommer.conf import settings

class S3Backend(object):
    def __init__(self, connection_str):
        # Start as a None value so we can lazy load.
        self._aws_s3_connection = None

    @property
    def aws_s3_connection(self):
        """
        Lazy-loading of the S3 boto connection. Refer to this instead of
        referencing self._aws_s3_connection directly.
        
        Returns:
            A boto connection to Amazon's S3 interface.
        """
        if not self._aws_s3_connection:
            self._aws_s3_connection = boto.connect_s3(
                settings.AWS_ACCESS_KEY_ID,
                settings.AWS_SECRET_ACCESS_KEY)
        return self._aws_s3_connection
