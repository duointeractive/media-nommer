"""
Classes in this module serve as a basis for Nommers. This should be thought
of as a protocol or a foundation to assist in maintaining a consistent API
between Nommers.
"""
import os
import tempfile
from media_nommer.core.storage_backends import get_storage_backend_for_uri

class BaseNommer(object):
    """
    This is a base class that can be sub-classed by each Nommer to serve
    as a foundation. Required methods raise a NotImplemented exception
    by default, unless overridden by child classes.
    """
    def __init__(self, job):
        self.job = job

    def download_source_file(self):
        file_uri = self.job.source_path
        print "ATTEMPTING TO DOWNLOAD", file_uri
        storage = get_storage_backend_for_uri(file_uri)
        fobj = tempfile.NamedTemporaryFile(mode='w+b', delete=True)
        storage.download_file(file_uri, fobj)
        fobj.flush()
        os.fsync(fobj.fileno())
        print "DOWNLOADED", fobj, fobj.name
