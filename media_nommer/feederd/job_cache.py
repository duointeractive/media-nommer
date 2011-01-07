"""
Basic job caching module.
"""
from media_nommer.core.job_state_backends import get_default_backend

class JobCache(dict):
    CACHE = {'1':0}
    
    @classmethod
    def load_recent_jobs_at_startup(cls):
        print "POPULATING CACHE"
    
    @classmethod
    def refresh_jobs_with_state_changes(cls):
        cls.CACHE['1'] += 1
        print "CHECKIN!", cls.CACHE