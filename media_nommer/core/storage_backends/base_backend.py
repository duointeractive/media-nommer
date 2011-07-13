class BaseStorageBackend(object):
    """
    This class serves as a protocol for storage backends. Each storage backend
    should override the following methods, if supported by whatever protocols
    they interact with.
    """
    @classmethod
    def download_file(cls, uri, fobj):
        """
        Given a URI, download the file to the ``fobj`` file-like object.

        :param str uri: The URI of a file to download.
        :param file fobj: A file-like object to download the file to.
        :rtype: file
        :returns: A file handle to the downloaded file.
        """
        msg = "Backend doesn't implement download_file()"
        raise NotImplementedError(msg)

    @classmethod
    def upload_file(cls, uri, fobj):
        """
        Given a file-like object, upload it to the specified URI.

        :param str uri: The URI to upload the file to.
        :param file fobj: The file-like object to upload.
        :returns: Return value and type depends on backend.
        """
        msg = "Backend doesn't implement upload_file()"
        raise NotImplementedError(msg)