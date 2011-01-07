"""
Contains the base backend class from which all backends are based from. All
job state backends should sub-class JobStateBackend.
"""
from media_nommer.core.job_state_backends import get_default_backend
from media_nommer.utils.mod_importing import import_class_from_module_string

class BaseEncodingJob(object):
    """
    Serves as a base for encoding jobs on all backends.
    
    TODO: Abstract job states out a little better. Handle the nasties during
    save and init time on the sub-class.
    """
    def __init__(self, source_path, dest_path, nommer, job_options,
                 unique_id=None, job_state=None, job_state_details=None,
                 notify_url=None, creation_dtime=None,
                 last_modified_dtime=None):
        """
        Document me.
        """
        self.source_path = source_path
        self.dest_path = dest_path
        # __import__ doesn't like unicode, cast this to a str.
        self.nommer_str = str(nommer)
        self.job_options = job_options
        self.unique_id = unique_id
        self.job_state = job_state
        self.job_state_details = job_state_details
        self.notify_url = notify_url
        self.creation_dtime = creation_dtime
        self.last_modified_dtime = last_modified_dtime

        # Reference to the global job state backend instance.
        self.backend = get_default_backend()

    def __repr__(self):
        """
        String representation of the object. Just show the unique ID.
        """
        return u'EncodingJob: %s' % self.unique_id

    @property
    def nommer(self):
        """
        Returns the correct Nommer instance for this job.
        """
        return import_class_from_module_string(self.nommer_str)(self)

    def save(self):
        """
        Saves this job to your job state backend, via self.backend.
        
        :returns: The job's unique ID.
        """
        raise NotImplemented()

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

    def is_finished(self):
        """
        Returns True if this job is in a finished state.
        """
        # Break job states into a list of tuples: (job state name, value)
        finished_states = self.backend.FINISHED_STATES
        # self.job_state returns the value from the DB, so just get the values.
        finished_states = [self.backend.JOB_STATES[value] for value in finished_states]
        # If current state matches the list of unfinished values, unfinished.
        return self.job_state in finished_states

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
        'ABANDONED': 'ABANDONED',
    }
    # Any jobs in the following states are considered "finished" in that we
    # won't do anything else with them.
    FINISHED_STATES = ['FINISHED', 'ERROR', 'ABANDONED']

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

    def pop_state_changes_from_queue(self, num_to_pop):
        """
        Stub
        """
        pass
    pop_state_changes_from_queue.enabled = False
