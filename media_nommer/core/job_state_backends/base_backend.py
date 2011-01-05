"""
Contains the base backend class from which all backends are based from. All
job state backends should sub-class JobStateBackend.
"""
from media_nommer.core.job_state_backends import get_default_backend

class BaseEncodingJob(object):
    def __init__(self, source_path, dest_path, preset, job_options,
                 unique_id=None, job_state=None, notify_url=None):
        self.source_path = source_path
        self.dest_path = dest_path
        self.preset = preset
        self.job_options = job_options
        self.unique_id = unique_id
        self.job_state = job_state
        # Reference to the global job state backend instance.
        self.backend = get_default_backend()

    def save(self):
        raise NotImplemented()

class BaseJobStateBackend(object):
    """
    This is a base class that can be sub-classed by each backend to serve
    as a foundation. Required methods raise a NotImplemented exception
    by default, unless overridden by child classes.
    """
    JOB_STATES = {
        'PENDING': 'PENDING'
    }
    def __init__(self, *args, **kwargs):
        pass

    def wipe_all_job_data(self, *args, **kwargs):
        """
        This method should completely wipe/empty the job DB and any queue
        services being used for job state tracking.
        """
        raise NotImplemented()

    def get_unfinished_jobs(self, *args, **kwargs):
        """
        This method should return a list of unfinished jobs.
        """
        raise NotImplemented()

    def create_new_job_in_db(self, *args, **kwargs):
        """
        This method should create a new job.
        """
        raise NotImplemented()

    def _generate_unique_job_id(self, encoding_job):
        """
        Given an encoding job, generate a unique identifier for the job. This
        is used in databases as a primary key replacement, for those that
        have no such concept. It does not apply to all DB systems, so this
        one is optional.
        """
        pass

    def save_job(self, encoding_job):
        """
        Given an EncodingJob object, save it to the job state storage backend.
        """
        raise NotImplemented()

    def get_job_class(self):
        """
        Returns a reference to this backend's EncodingJob sub-class.
        """
        raise NotImplemented()
