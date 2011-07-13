"""
This module contains an HTTPBackend class for working with URIs that have
an http:// or https:// protocol specified.
"""
import urllib2
from media_nommer.utils import logger
from media_nommer.core.storage_backends.exceptions import InfileNotFoundException
from media_nommer.core.storage_backends.base_backend import BaseStorageBackend

class HTTPBackend(BaseStorageBackend):
    """
    Abstracts access to HTTP via the common set of file storage backend methods.

    .. note:: ``upload_file`` is not implemented yet, not sure how
        it should work.
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
        request = urllib2.Request(uri)

        try:
            download = urllib2.urlopen(request)
        except urllib2.URLError, e:
            message = "The specified input file cannot be found: %s" % e
            raise InfileNotFoundException(message)

        fobj.write(download.read())

        logger.debug("HTTPBackend.download_file(): " \
                     "Download of %s completed." % uri)
        return fobj
