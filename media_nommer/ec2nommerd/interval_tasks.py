"""
This module contains tasks that are executed at intervals, and is imported at
the time the server is started.
"""
from twisted.internet import task, reactor
from media_nommer.conf import settings
from media_nommer.utils import logger
from media_nommer.core.job_state_backend import JobStateBackend
from media_nommer.ec2nommerd.node_state import NodeStateManager

def threaded_encode_job(job):
    """
    Given a job, run it through its encoding workflow in a non-blocking manner.
    """
    # Update the timestamp for when the node last did something so it
    # won't terminate itself.
    NodeStateManager.i_did_something()
    job.nommer.onomnom()

def task_check_for_new_jobs():
    """
    Looks at the number of currently active threads and compares it against
    the MAX_ENCODING_JOBS_PER_EC2_INSTANCE setting. If we are under the max,
    fire up another thread for encoding additional job(s). 
    """
    num_active_threads = NodeStateManager.get_num_active_threads()
    max_threads = settings.MAX_ENCODING_JOBS_PER_EC2_INSTANCE
    num_jobs_to_pop = max(0, max_threads - num_active_threads)

    if num_jobs_to_pop > 0:
        # We have more room for encoding threads, determine how many.
        logger.debug("task_check_for_new_jobs: " \
                     "Popping up to %d new jobs." % num_jobs_to_pop)
        # This is an iterable of BaseEncodingJob sub-classed instances for
        # each job returned from the queue.
        jobs = JobStateBackend.pop_new_jobs_from_queue(num_jobs_to_pop)
        if jobs:
            logger.debug("* Popped %d jobs from the queue." % len(jobs))

        for job in jobs:
            # For each job returned, render in another thread.
            logger.debug("* Starting encoder thread for job: %s" % job.unique_id)
            reactor.callInThread(threaded_encode_job, job)
task.LoopingCall(task_check_for_new_jobs).start(
    settings.NOMMERD_NEW_JOB_CHECK_INTERVAL, now=True)

def threaded_heartbeat():
    """
    Send some basic state data to a SimpleDB domain, for feederd to see.
    """
    if settings.NOMMERD_TERMINATE_WHEN_IDLE:
        # thread_count_mod factors out this thread when counting active threads.
        is_terminated = NodeStateManager.contemplate_termination(thread_count_mod= -1)
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
