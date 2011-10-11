"""
This module contains an FileBackend class for working with URIs that have
an file:// URI specified. This is for local files (from ec2nommerd's perspective),
more specifically.
"""
import os
import urlparse
import shutil
from media_nommer.utils import logger
from media_nommer.core.storage_backends.exceptions import InfileNotFoundException
from media_nommer.core.storage_backends.base_backend import BaseStorageBackend

class FileBackend(BaseStorageBackend):
    """
    Abstracts access to local files via the common set of file storage backend
    methods.
    """
    @classmethod
    def download_file(cls, uri, fobj):
        """
        Given a URI, open said file from the local file system.
        
        :param str uri: The URI of a file to open.
        :param file fobj: This is unused in this backend, but here for
            the sake of consistency.
        :rtype: file
        :returns: A file handle to the given file.
        """
        infile_path = cls._get_path_from_uri(uri)
        if not os.path.exists(infile_path):
            message = "The specified input file cannot be found: %s" % infile_path
            raise InfileNotFoundException(message)

        logger.debug("FileBackend.download_file(): " \
                     "Opening of %s completed." % uri)

        infile = open(infile_path, 'rb')
        # Inefficient, but meh. We'll come up with something more clever later.
        for line in infile:
            fobj.write(line)
        
        return fobj

    @classmethod
    def upload_file(cls, uri, fobj):
        """
        Given a file-like object, copy it to the user's specified
        destination path (locally). We have to copy, since the encoded
        file resides in a temporary file that is deleted once the file-like
        object is garbage collected.

        :param str uri: The URI to copy the finished encoding to.
        :param file fobj: The file-like object of the finished encoding.
        :rtype: str
        :returns: The path to the final destination for the encoding.
        """
        # This is the path to the temp file that the encoding was saved to.
        tempfile_path = fobj.name
        # This is the path of the eventual destination file.
        outfile_path = cls._get_path_from_uri(uri)

        logger.debug("FileBackend.upload_file(): "\
                     "Copying tempfile '%s' to outfile %s" % (
            tempfile_path, outfile_path
        ))

        # The temp file will be deleted once the encoding is done, so make
        # a copy where the user requested the final file to end up.
        shutil.copyfile(tempfile_path, outfile_path)

        logger.debug("FileBackend.upload_file(): Copy complete.")

        return outfile_path

    @classmethod
    def _get_path_from_uri(cls, uri):
        """
        Given a URI, return a local path that will eventually be passed to
        the ``open()`` built-in.
        """
        parsed_result = urlparse.urlparse(uri)
        return os.path.abspath(
            os.path.join(parsed_result.netloc, parsed_result.path)
        )