"""
Basic job caching module.
"""
import datetime
from media_nommer.conf import settings
from media_nommer.utils import logger
from media_nommer.core.job_state_backend import JobStateBackend
from media_nommer.utils.compat import total_seconds

class JobCache(dict):
    """
    Caches currently active
    :py:class:`media_nommer.core.job_state_backend.EncodingJob` objects.
    This is presently only un-finished jobs, as defined by
    :py:attr:`media_nommer.core.job_state_backend.JobStateBackend.FINISHED_STATES`.
    """
    CACHE = {}

    @classmethod
    def update_job(cls, job):
        """
        Updates a job in the cache. Creates the key if it doesn't
        already exist.


        :type job: :py:class:`EncodingJob <media_nommer.core.job_state_backend.EncodingJob>`
        :param job: The job to update (or create) a cache entry for.
        """
        cls.CACHE[job.unique_id] = job

    @classmethod
    def get_job(cls, job):
        """
        Given a job's unique id, return the job object from the cache.

        :type job: :py:class:`EncodingJob <media_nommer.core.job_state_backend.EncodingJob>`
        :param job: A job's unique ID or a job object.
        :rtype: :py:class:`EncodingJob <media_nommer.core.job_state_backend.EncodingJob>`
        :returns: The cached encoding job.
        """
        if isinstance(job, basestring):
            key = job
        else:
            key = job.unique_id
        return cls.CACHE[key]

    @classmethod
    def remove_job(cls, job):
        """
        Removes a job from the cache.

        :type job: ``str`` or :py:class:`EncodingJob <media_nommer.core.job_state_backend.EncodingJob>`
        :param job: A job's unique ID or a job object.
        """
        if isinstance(job, basestring):
            key = job
        else:
            key = job.unique_id
        del cls.CACHE[key]

    @classmethod
    def is_job_cached(cls, job):
        """
        Given a job object or a unique id, return True if said job is cached,
        and False if not.

        :type job: ``str`` or :py:class:`EncodingJob <media_nommer.core.job_state_backend.EncodingJob>`
        :param job: A job's unique ID or a job object.
        :rtype: bool
        :returns: ``True`` if the given job exists in the cache, ``False``
            if otherwise.
        """
        if isinstance(job, basestring):
            key = job
        else:
            key = job.unique_id
        return cls.CACHE.has_key(key)

    @classmethod
    def get_cached_jobs(cls):
        """
        Returns a dict of all cached jobs. The keys are unique IDs, the
        values are the job objects.

        :rtype: dict
        :returns: A dictionary with the keys being unique IDs of cached jobs,
            and the values being
            :py:class:`EncodingJob <media_nommer.core.job_state_backend.EncodingJob>`
            instances.
        """
        return cls.CACHE

    @classmethod
    def get_jobs_with_state(cls, state):
        """
        Given a valid job state (refer to
        :py:attr:`media_nommer.core.job_state_backend.JobStateBackend.JOB_STATES`),
        return all jobs that currently have this state.

        :param str state: The job state to query by.
        :rtype: ``list`` of :py:class:`EncodingJob <media_nommer.core.job_state_backend.EncodingJob>`
        :returns: A list of jobs matching the given state.
        """
        return [job for id, job in cls.get_cached_jobs.items() if job.job_state == state]

    @classmethod
    def load_recent_jobs_at_startup(cls):
        """
        Loads all of the un-finished jobs into the job cache. This is
        performed when :doc:`../feederd` starts.
        """
        # Use print here because logging isn't fully configured at this point?
        print("Populating job cache from SimpleDB.")
        jobs = JobStateBackend.get_unfinished_jobs()
        for job in jobs:
            cls.update_job(job)

        print("Jobs loaded from SDB to cache:")
        for job in jobs:
            print('* %s (State: %s -- Finished: %s)' % (
                job.unique_id, job.job_state,
                job.is_finished())
            )

    @classmethod
    def refresh_jobs_with_state_changes(cls):
        """
        Looks at the state SQS queue specified by the
        :py:data:`SQS_JOB_STATE_CHANGE_QUEUE_NAME <media_nommer.conf.settings.SQS_JOB_STATE_CHANGE_QUEUE_NAME>`
        setting and refreshes any jobs that have changed. This simply reloads
        the job's details from SimpleDB_.

        :rtype: ``list`` of :py:class:`EncodingJob <media_nommer.core.job_state_backend.EncodingJob>`
        :returns: A list of changed :py:class:`EncodingJob` objects.
        """
        logger.debug("JobCache.refresh_jobs_with_state_changes(): " \
                    "Checking state change queue.")
        # Pops up to 10 changed jobs that we think may have changed. There are
        # some false alarms in here, whch brings us to...
        popped_changed_jobs = JobStateBackend.pop_state_changes_from_queue(10)
        # A temporary list that stores the jobs that actually changed. This
        # will be returned at the completion of this method's path.
        changed_jobs = []

        if popped_changed_jobs:
            logger.debug("Potential job state changes found: %s" % popped_changed_jobs)
            for job in popped_changed_jobs:
                if cls.is_job_cached(job):
                    current_state = cls.get_job(job).job_state
                    new_state = job.job_state

                    if current_state != new_state:
                        logger.info("* Job state changed %s: %s -> %s" % (
                            job.unique_id,
                            # Current job state in cache
                            current_state,
                            # New incoming job state
                            new_state,
                        ))
                        cls.update_job(job)
                        # This one actually changed, append this for returning.
                        changed_jobs.append(job)
                        if new_state == 'ERROR':
                            logger.error('Error trace from ec2nommerd:')
                            logger.error(job.job_state_details)
        return changed_jobs

    @classmethod
    def abandon_stale_jobs(cls):
        """
        On rare occasions, nommers crash so hard that no ``ERROR`` state change
        is made, and the job just gets stuck in a permanent unfinished state
        (``DOWNLOADING``, ``ENCODING``, ``UPLOADING``, etc). Rather than hang
        on to these indefinitely, abandon them by setting their state to
        ``ABANDONED``.

        The threshold for which jobs are considered abandoned is configurable
        via the
        :py:data:`FEEDERD_ABANDON_INACTIVE_JOBS_THRESH <media_nommer.conf.settings.FEEDERD_ABANDON_INACTIVE_JOBS_THRESH>`
        setting.
        """
        logger.debug("JobCache.abandon_stale_jobs(): "\
                     "Looking for stale jobs.")
        for id, job in cls.get_cached_jobs().items():
            if not job.is_finished():
                now_dtime = datetime.datetime.now()
                last_mod = job.last_modified_dtime

                tdelta = now_dtime - last_mod
                inactive_seconds = total_seconds(tdelta)

                if inactive_seconds >= settings.FEEDERD_ABANDON_INACTIVE_JOBS_THRESH:
                    cls.remove_job(job)
                    job.set_job_state('ABANDONED', job.job_state_details)

    @classmethod
    def uncache_finished_jobs(cls):
        """
        Clears jobs from the cache after they have been finished.

        TODO: We'll eventually want to clear jobs from the cache that haven't
        been accessed by the web API recently.
        """
        for id, job in cls.CACHE.items():
            if job.is_finished():
                logger.info("Removing job %s from job cache." % id)
                cls.remove_job(id)
