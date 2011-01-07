"""
Basic job caching module.
"""
from media_nommer.core.job_state_backends import get_default_backend

class JobCache(dict):
    CACHE = {}
    
    @classmethod
    def load_recent_jobs_at_startup(cls):
        """
        Loads all of the un-finished jobs into the job cache.
        """
        jobs = get_default_backend().get_unfinished_jobs()
        for job in jobs:
            cls.CACHE[job.unique_id] = job
            
        print "JOBS LOADED:"
        for job in jobs:
            print '* %s' % job.unique_id
    
    @classmethod
    def refresh_jobs_with_state_changes(cls):
        """
        Looks at the state change queue (if your backend has one), and
        partially refreshes the object cache based on which jobs have changed.
        """
        changed_jobs = get_default_backend().pop_state_changes_from_queue(10)
        
        if changed_jobs:
            print "CHANGES ARRIVED", changed_jobs
            for job in changed_jobs:
                print "CHANGED", job, job.unique_id
                cls.CACHE[job.unique_id] = job
                
    @classmethod
    def abandon_stale_jobs(cls):
        """
        On rare occasions, nommers crash so hard that no ERROR state change is
        made, and the job just gets stuck in a permanent unfinished state
        (DOWNLOADING, ENCODING, UPLOADING, etc). Rather than hang on to these
        indefinitely, abandon them.
        """
        print "ABANDONING"