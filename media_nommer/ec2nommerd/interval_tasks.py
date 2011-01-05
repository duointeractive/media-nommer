"""
This module contains tasks that are executed at intervals, and is imported at
the time the server is started.
"""
import time
from twisted.internet import task, threads, reactor
from twisted.python import log
from media_nommer.conf import settings
from media_nommer.core.job_state_backends import get_default_backend

def run_every_second():
    """
    Just an example task.
    """
    num_active_threads = len(reactor.getThreadPool().working)
    max_threads = settings.MAX_ENCODING_JOBS_PER_EC2_INSTANCE
    if num_active_threads < max_threads:
        num_msgs_to_get = max(0, max_threads - num_active_threads)
        print "Starting as many as", num_msgs_to_get
        job_state_backend = get_default_backend()
        jobs = job_state_backend.pop_job_from_queue(num_msgs_to_get)
task.LoopingCall(run_every_second).start(10, now=False)

def threaded_check_job_queue():
    """
    Checks all S3 In Buckets for incoming files to encode.
    """
    #print "STARTING CHECK"
    #time.sleep(5)
    #print "FINISHED CHECK"
    pass

def task_check_job_queue():
    """
    Calls the incoming bucket checking functions in a separate thread to prevent
    this long call from blocking us.
    
    TODO: Figure out how to not spawn a new thread with each loop of this.
    That is expensive. Earlier attempts failed, please be my guest.
    """
    reactor.callInThread(threaded_check_job_queue)
    #d = threads.deferToThread(threaded_check_job_queue)
    #d.addCallback(callback_check_s3_in_buckets)
task.LoopingCall(task_check_job_queue).start(10, now=True)
