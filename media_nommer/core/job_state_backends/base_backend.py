"""
Contains the base backend class from which all backends are based from. All
job state backends should sub-class JobStateBackend.
"""

class JobStateBackend(object):
    """
    This is a base class that can be sub-classed by each backend to serve
    as a foundation. Required methods raise a NotImplemented exception
    by default, unless overridden by child classes.
    """

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
