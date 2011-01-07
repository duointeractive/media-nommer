"""
Contains the base backend class from which all backends are based from. All
job state backends should sub-class JobStateBackend.
"""
import simplejson
from media_nommer.core.job_state_backends import get_default_backend
from media_nommer.utils.mod_importing import import_class_from_module_string

class BaseEncodingJob(object):
    def __init__(self, source_path, dest_path, nommer_str, job_options,
                 unique_id=None, job_state=None, job_state_details=None,
                 notify_url=None):
        self.source_path = source_path
        self.dest_path = dest_path
        # __import__ doesn't like unicode, cast this to a str.
        self.nommer_str = str(nommer_str)
        self.unique_id = unique_id
        self.job_state = job_state
        self.job_state_details = job_state_details
        # Reference to the global job state backend instance.
        self.backend = get_default_backend()

        if isinstance(job_options, basestring):
            self.job_options = simplejson.loads(job_options)
        else:
            self.job_options = job_options

    def set_job_state(self, job_state, details=None):
        """
        Sets the job's state and saves it to the backend.
        """
        if not self.backend.JOB_STATES.has_key(job_state):
            raise Exception('Invalid job state: %s' % job_state)

        self.job_state = self.backend.JOB_STATES[job_state]
        self.job_state_details = details
        if details and isinstance(details, basestring):
            # Get within AWS's limitations. We'll assume that the error message
            # is probably near the tail end of the output (hopefully). Not
            # a great assumption, but it'll have to do.
            self.job_state_details = details[-1023:]

        # Write the changes to the backend.
        self.save()
        # Announce a change in state, if the backend supports such a thing.
        self._send_state_change_notification()

    def _send_state_change_notification(self):
        """
        Some backends need to push a notification out to feederd in some way
        when job states change. This is an optional method for that purpose.
        """
        pass

    @property
    def nommer(self):
        """
        Returns the correct Nommer instance for this job.
        """
        print "TRYING TO IMPORT", self.nommer_str, type(self.nommer_str)
        return import_class_from_module_string(self.nommer_str)(self)

    def save(self):
        """
        Saves this job to your job state backend, via self.backend.
        
        :returns: The job's unique ID.
        """
        raise NotImplemented()

class BaseJobStateBackend(object):
    """
    This is a base class that can be sub-classed by each backend to serve
    as a foundation. Required methods raise a NotImplemented exception
    by default, unless overridden by child classes.
    """
    JOB_STATES = {
        'PENDING': 'PENDING',
        'DOWNLOADING': 'DOWNLOADING',
        'ENCODING': 'ENCODING',
        'UPLOADING': 'UPLOADING',
        'FINISHED': 'FINISHED',
        'ERROR': 'ERROR',
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

    def get_job_class(self):
        """
        Returns a reference to this backend's EncodingJob sub-class.
        """
        raise NotImplemented()

    def pop_job_from_queue(self, num_to_pop):
        """
        Pops jobs from the queue, returning a list of your backend's 
        BaseEncodingJob sub-class instances.
        
        .. warning: Once popped, jobs are removed from the queue.
        
        :returns: A list of your backend's BaseEncodingJob sub-class instances.
        """
        raise NotImplemented()
