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
    Caches currently active EncodingJob objects. This is presently only
    un-finished jobs.
    """
    CACHE = {}

    @classmethod
    def update_job(cls, job):
        """
        Updates a job in the cache. Creates the key if it doesn't
        already exist.
        """
        cls.CACHE[job.unique_id] = job

    @classmethod
    def get_job(cls, job):
        """
        Given a job's unique id, return the job object from the cache.
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
        """
        return cls.CACHE

    @classmethod
    def get_jobs_with_state(cls, state):
        """
        Given a valid job state (refer to 
        media_nommer.core.job_state_backend.JobStateBackend.JOB_STATES),
        return all jobs that currently have this state
        """
        return [job for id, job in cls.get_cached_jobs.items() if job.job_state == state]

    @classmethod
    def load_recent_jobs_at_startup(cls):
        """
        Loads all of the un-finished jobs into the job cache.
        """
        logger.info("Populating job cache from SimpleDB.")
        jobs = JobStateBackend.get_unfinished_jobs()
        for job in jobs:
            cls.update_job(job)

        logger.info("Jobs loaded from SDB to cache:")
        for job in jobs:
            logger.info('* %s (%s -- %s)' % (
                job.unique_id, job.job_state,
                job.is_finished())
            )

    @classmethod
    def refresh_jobs_with_state_changes(cls):
        """
        Looks at the state change queue (if your backend has one), and
        partially refreshes the object cache based on which jobs have changed.
        """
        logger.debug("JobCache.refresh_jobs_with_state_changes(): Checking state change queue.")
        changed_jobs = JobStateBackend.pop_state_changes_from_queue(10)

        if changed_jobs:
            logger.info("Job state changes found: %s" % changed_jobs)
            for job in changed_jobs:
                if cls.is_job_cached(job):
                    logger.info("* Job state changed %s: %s -> %s" % (
                        job.unique_id,
                        # Current job state in cache
                        cls.get_job(job).job_state,
                        # New incoming job state
                        job.job_state,
                    ))
                    cls.update_job(job)

    @classmethod
    def abandon_stale_jobs(cls):
        """
        On rare occasions, nommers crash so hard that no ERROR state change is
        made, and the job just gets stuck in a permanent unfinished state
        (DOWNLOADING, ENCODING, UPLOADING, etc). Rather than hang on to these
        indefinitely, abandon them.
        """
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
