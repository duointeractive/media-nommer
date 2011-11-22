"""
This module contains an S3Backend class for working with URIs that have
an s3:// protocol specified.
"""
import boto
from media_nommer.utils import logger
from media_nommer.utils.uri_parsing import get_values_from_media_uri
from media_nommer.core.storage_backends.exceptions import InfileNotFoundException
from media_nommer.core.storage_backends.base_backend import BaseStorageBackend

class S3Backend(BaseStorageBackend):
    """
    Abstracts access to S3 via the common set of file storage backend methods.
    """
    @classmethod
    def _get_aws_s3_connection(cls, access_key, secret_access_key):
        """
        Lazy-loading of the S3 boto connection. Refer to this instead of
        referencing self._aws_s3_connection directly.

        :param str access_key: The AWS_ Access Key needed to get to the
            file in question.
        :param str secret_access_key: The AWS_ Secret Access Key needed to get
            to the file in question.
        :rtype: :py:class:`boto.s3.connection.Connection`
        :returns: A boto connection to Amazon's S3 interface.
        """
        return boto.connect_s3(access_key, secret_access_key)

    @classmethod
    def download_file(cls, uri, fobj):
        """
        Given a URI, download the file to the ``fobj`` file-like object.

        :param str uri: The URI of a file to download.
        :param file fobj: A file-like object to download the file to.
        :rtype: file
        :returns: A file handle to the downloaded file.
        """
        # Breaks the URI into usable componenents.
        values = get_values_from_media_uri(uri)

        conn = cls._get_aws_s3_connection(values['username'],
                                          values['password'])
        bucket = conn.get_bucket(values['host'])
        key = bucket.get_key(values['path'])

        logger.debug("S3Backend.download_file(): " \
                     "Downloading: %s" % uri)

        try:
            key.get_contents_to_file(fobj)
        except AttributeError:
            # Raised by ResumableDownloadHandler in boto when the given S3
            # key can't be found.
            message = "The specified input file cannot be found."
            raise InfileNotFoundException(message)

        logger.debug("S3Backend.download_file(): " \
                     "Download of %s completed." % uri)
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

        conn = cls._get_aws_s3_connection(values['username'],
                                          values['password'])
        bucket = conn.create_bucket(values['host'])
        key = bucket.new_key(values['path'])

        logger.debug("S3Backend.upload_file(): "\
                     "Settings contents of '%s' key from %s" % (
            values['path'], fobj.name))
        key.set_contents_from_filename(fobj.name)

        logger.debug("S3Backend.upload_file(): Upload complete.")
        return key
