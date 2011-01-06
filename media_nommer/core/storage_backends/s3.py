import boto
from boto.s3.resumable_download_handler import ResumableDownloadHandler
from media_nommer.conf import settings
from media_nommer.utils.uri_parsing import get_values_from_media_uri

class S3Backend(object):
    @classmethod
    def get_aws_s3_connection(cls, access_key, secret_access_key):
        """
        Lazy-loading of the S3 boto connection. Refer to this instead of
        referencing self._aws_s3_connection directly.
        
        :returns: A boto connection to Amazon's S3 interface.
        """
        return boto.connect_s3(access_key, secret_access_key)

    @classmethod
    def download_file(cls, uri, fobj):
        """
        Given a URI, download the file.
        
        :returns: A file handle to the downloaded file.
        """
        # Breaks the URI into usable componenents.
        values = get_values_from_media_uri(uri)
        conn = cls.get_aws_s3_connection(values['username'], values['password'])
        bucket = conn.get_bucket(values['host'])
        key = bucket.get_key(values['path'])
        dlhandler = ResumableDownloadHandler(num_retries=10)
        dlhandler.get_file(key, fobj, None)
        return fobj
