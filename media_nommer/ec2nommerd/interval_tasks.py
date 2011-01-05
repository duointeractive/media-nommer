"""
This module contains tasks that are executed at intervals, and is imported at
the time the server is started.
"""
import time
from twisted.internet import task, threads, reactor
from twisted.python import log
from media_nommer.conf import settings
from media_nommer.core.job_state_backends import get_default_backend

def task_check_for_new_jobs():
    """
    Looks at the number of currently active threads and compares it against
    the MAX_ENCODING_JOBS_PER_EC2_INSTANCE setting. If we are under the max,
    fire up another thread for encoding additional job(s). 
    """
    num_active_threads = len(reactor.getThreadPool().working)
    max_threads = settings.MAX_ENCODING_JOBS_PER_EC2_INSTANCE
    if num_active_threads < max_threads:
        # We have more room for encoding threads, determine how many.
        num_msgs_to_get = max(0, max_threads - num_active_threads)
        print "Job check tic. Starting as many as", num_msgs_to_get
        # Reference to our instantiated job state backend.
        job_state_backend = get_default_backend()
        # This is an iterable of BaseEncodingJob sub-classed instances for
        # each job returned from the queue.
        jobs = job_state_backend.pop_job_from_queue(num_msgs_to_get)

        for job in jobs:
            # For each job returned, render in another thread.
            reactor.callInThread(task_render_job, job)
task.LoopingCall(task_check_for_new_jobs).start(10, now=False)

def task_render_job(job):
    """
    Calls the incoming bucket checking functions in a separate thread to prevent
    this long call from blocking us.
    
    TODO: Figure out how to not spawn a new thread with each loop of this.
    That is expensive. Earlier attempts failed, please be my guest.
    """
    print "JOB THREAD", job.unique_id
