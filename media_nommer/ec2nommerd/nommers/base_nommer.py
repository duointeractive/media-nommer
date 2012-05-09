"""
Classes in this module serve as a basis for Nommers. This should be thought
of as a protocol or a foundation to assist in maintaining a consistent API
between Nommers.
"""
import os
import traceback
import tempfile
import shutil
from media_nommer.utils import logger
from media_nommer.ec2nommerd.node_state import NodeStateManager
from media_nommer.core.storage_backends import get_backend_for_uri

class BaseNommer(object):
    """
    This is a base class that can be sub-classed by each Nommer to serve
    as a foundation. Required methods raise a NotImplementedError exception
    by default, unless overridden by child classes.

    :ivar EncodingJob job: The encoding job this nommer is handling.
    """
    def __init__(self, job):
        self.job = job

    def onomnom(self):
        """
        Start nomming. If you're going to override this, make sure to follow
        the same basic job state updating flow if possible.
        """
        # Have to create a temporary directory, since ffmpeg's libx264 encoder
        # doesn't obey alternate logfile paths. I'm sure other software
        # has similar limitations, so let's just not take any chances.
        self.temp_cwd = tempfile.mkdtemp()

        try:
            self._onomnom()
        except:
            # If we run into any un-handled exceptions, error out the job
            # and set as its state details.
            self.wrapped_set_job_state('ERROR', details=traceback.format_exc())
            traceback.print_exc()

        # Clean up the temporary CWD used during nomming.
        shutil.rmtree(self.temp_cwd, ignore_errors=True)

    def _onomnom(self):
        """
        Call your encoder here, do work. Make sure to update job state as
        it progresses, if you can.
        
        Needs to set one of the two job states: FINISHED, ERROR
        """
        raise NotImplementedError

    def wrapped_set_job_state(self, *args, **kwargs):
        """
        Wraps set_job_state() to perform extra actions before and/or after
        job state updates.
        
        :param str new_state: The job state to set.
        """
        # Tracks the fact that we did something, prevents the node from
        # terminating itself.
        NodeStateManager.i_did_something()
        self.job.set_job_state(*args, **kwargs)

    def download_source_file(self):
        """
        Download the source file to a temporary file.
        """
        self.wrapped_set_job_state('DOWNLOADING')

        # This is the remote path.
        file_uri = self.job.source_path
        logger.debug("BaseNommer.download_source_file(): " \
                     "Attempting to download %s" % file_uri)
        # Figure out which backend to use for the protocol in the URI.
        storage = get_backend_for_uri(file_uri)
        # Create a temporary file which will be auto deleted when
        # garbage collected.
        fobj = tempfile.NamedTemporaryFile(mode='w+b', delete=True)
        # Using the correct backend, download the file to the given
        # file-like object.
        storage.download_file(file_uri, fobj)
        # flush and fsync to force writing to the file object. Doesn't always
        # happen otherwise.
        fobj.flush()
        os.fsync(fobj.fileno())

        logger.debug("BaseNommer.download_source_file(): " \
                     "Downloaded %s to %s" % (file_uri, fobj.name))

        # As soon as this fobj is garbage collected, it is closed(). Be
        # careful to continue its existence if you need it.
        return fobj

    def upload_to_destination(self, fobj):
        """
        Upload the output file to the destination specified by the user.
        """
        self.wrapped_set_job_state('UPLOADING')

        file_uri = self.job.dest_path
        logger.debug("BaseNommer.upload_to_destination(): " \
                     "Attempting to upload %s to %s" % (fobj.name, file_uri))
        storage = get_backend_for_uri(file_uri)
        storage.upload_file(file_uri, fobj)
        logger.debug("BaseNommer.upload_to_destination(): " \
                     "Finished uploading %s to %s" % (fobj.name, file_uri))
