"""
This module contains tasks that are executed at intervals, and is imported at
the time the server is started.
"""
from twisted.internet import task, threads, reactor
from media_nommer.core.job_state_backends import get_default_backend
from media_nommer.feederd.job_cache import JobCache

def threaded_check_for_job_state_changes():
    """
    Doc me
    """
    JobCache.refresh_jobs_with_state_changes()

def task_check_for_job_state_changes():
    """
    Checks for job state changes in another thread.
    """
    reactor.callInThread(threaded_check_for_job_state_changes)
    
if get_default_backend().pop_state_changes_from_queue.enabled:
    task.LoopingCall(task_check_for_job_state_changes).start(10, now=False)
    
def threaded_abandon_stale_jobs():
    """
    Doc me
    """
    JobCache.abandon_stale_jobs()
    
def task_abandon_stale_jobs():
    reactor.callInThread(threaded_abandon_stale_jobs)
task.LoopingCall(task_abandon_stale_jobs).start(10, now=False)