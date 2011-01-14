import boto
from boto.s3.resumable_download_handler import ResumableDownloadHandler
from media_nommer.conf import settings
from media_nommer.utils import logger
from media_nommer.utils.uri_parsing import get_values_from_media_uri

class S3Backend(object):
    """
    Abstracts access to S3 via the common set of file storage backend methods.
    """

    @classmethod
    def _get_aws_s3_connection(cls, access_key, secret_access_key):
        """
        Lazy-loading of the S3 boto connection. Refer to this instead of
        referencing self._aws_s3_connection directly.
        
        :rtype: :py:class:`boto.s3.connection.Connection`
        :returns: A boto connection to Amazon's S3 interface.
        """
        return boto.connect_s3(access_key, secret_access_key)

    @classmethod
    def download_file(cls, uri, fobj):
        """
        Given a URI, download the file to the given file-like object.
        
        :rtype: file
        :returns: A file handle to the downloaded file.
        """
        # Breaks the URI into usable componenents.
        values = get_values_from_media_uri(uri)

        conn = cls._get_aws_s3_connection(values['username'], values['password'])
        bucket = conn.get_bucket(values['host'])
        key = bucket.get_key(values['path'])

        logger.debug("S3Backend.download_file(): Downloading: %s" % uri)
        dlhandler = ResumableDownloadHandler(num_retries=10)
        dlhandler.get_file(key, fobj, None)

        logger.debug("S3Backend.download_file(): Download of %s completed." % uri)
        return fobj

    @classmethod
    def upload_file(cls, uri, fobj):
        """
        Given a file-like object, upload it to the specified URI.
        
        :param str uri: The URI to upload the file to.
        :param file fobj: The file-like object to populate the S3 key from.
        :rtype: :py:class:`boto.s3.key.Key`
        :returns: The newly set boto key.
        """
        # Breaks the URI into usable componenents.
        values = get_values_from_media_uri(uri)
        logger.debug("S3Backend.upload_file(): Received: %s" % values)

        conn = cls._get_aws_s3_connection(values['username'], values['password'])
        bucket = conn.create_bucket(values['host'])
        key = bucket.new_key(values['path'])

        logger.debug("S3Backend.upload_file(): Settings contents of '%s' key from %s" % (
            values['path'], fobj.name))
        key.set_contents_from_filename(fobj.name)

        logger.debug("S3Backend.upload_file(): Upload complete.")
        return key
