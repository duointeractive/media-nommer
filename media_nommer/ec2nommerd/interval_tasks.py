"""
This module contains tasks that are executed at intervals, and is imported at
the time the server is started.
"""
from twisted.internet import task, reactor
from media_nommer.conf import settings
from media_nommer.core.job_state_backend import JobStateBackend
from media_nommer.ec2nommerd.node_state import NodeStateManager

def threaded_encode_job(job):
    """
    Given a job, run it through its encoding workflow in a non-blocking manner.
    """
    print "JOB OBJ", job
    print "JOB SOURCE", job.source_path
    NodeStateManager.i_did_something()
    job.nommer.onomnom()

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
        # This is an iterable of BaseEncodingJob sub-classed instances for
        # each job returned from the queue.
        jobs = JobStateBackend.pop_new_jobs_from_queue(num_msgs_to_get)
        print "Queue checked, found", len(jobs)

        for job in jobs:
            # For each job returned, render in another thread.
            print "* Starting encoder thread"
            reactor.callInThread(threaded_encode_job, job)
task.LoopingCall(task_check_for_new_jobs).start(
    settings.NOMMERD_NEW_JOB_CHECK_INTERVAL, now=True)

def threaded_heartbeat():
    """
    Send some basic state data to a SimpleDB domain, for feederd to see.
    """
    if settings.NOMMERD_TERMINATE_WHEN_IDLE:
        is_terminated = NodeStateManager.contemplate_termination()
    else:
        is_terminated = False

    if not is_terminated:
        NodeStateManager.send_instance_state_update()

def task_heartbeat():
    """
    Fires off a threaded task to check in with feederd via SimpleDB. There
    is a domain that contains all of the running EC2 instances and their
    unique IDs, along with some state data.
    """
    reactor.callInThread(threaded_heartbeat)
task.LoopingCall(task_heartbeat).start(
    settings.NOMMERD_HEARTBEAT_INTERVAL, now=False)
