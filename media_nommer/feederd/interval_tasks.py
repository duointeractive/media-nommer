"""
This module contains tasks that are executed at intervals, and is imported at
the time the server is started. Much of feederd's 'intelligence' can be
found here.
"""
from twisted.internet import task, reactor
from media_nommer.conf import settings
from media_nommer.utils import logger
from media_nommer.feederd.job_cache import JobCache
from media_nommer.feederd.ec2_instance_manager import EC2InstanceManager

def threaded_check_for_job_state_changes():
    """
    Checks the SQS queue specified in settings.SQS_JOB_STATE_CHANGE_QUEUE_NAME
    for announcements of state changes from external nommers like
    EC2FFmpegNommer. This lets feederd know it needs to get updated job
    details from the SimpleDB domain defined in settings.SIMPLEDB_JOB_STATE_DOMAIN.
    """
    JobCache.refresh_jobs_with_state_changes()
    # If jobs have completed, remove them from the job cache.
    JobCache.uncache_finished_jobs()

def task_check_for_job_state_changes():
    """
    Checks for job state changes in a non-blocking manner.
    """
    reactor.callInThread(threaded_check_for_job_state_changes)
task.LoopingCall(task_check_for_job_state_changes).start(
    settings.FEEDERD_JOB_STATE_CHANGE_CHECK_INTERVAL, now=False)

def threaded_prune_jobs():
    """
    Sometimes failure happens, but a Nommer doesn't handle said failure
    gracefully. Instead of state changing to ERROR, it gets stuck in
    some un-finished state in the SimpleDB domain defined in
    settings.SIMPLEDB_JOB_STATE_DOMAIN.
    
    This process finds jobs that haven't been updated in a very long time
    (a day or so) that are probably dead. It marks them with an ABANDONED
    state, letting us know something went really wrong.
    """
    JobCache.abandon_stale_jobs()
    # Expire any newly abandoned jobs, too. Removes them from job cache.
    JobCache.uncache_finished_jobs()

def task_prune_jobs():
    """
    Prune expired or abandoned jobs from the settings.SIMPLEDB_JOB_STATE_DOMAIN
    domain and feederd's job cache.
    """
    reactor.callInThread(threaded_prune_jobs)
task.LoopingCall(task_prune_jobs).start(
    settings.FEEDERD_PRUNE_JOBS_INTERVAL, now=False)

def threaded_manage_ec2_instances():
    """
    Looks at the current number of jobs needing encoding and compares them
    to the pool of currently running EC2 instances. Spawns more EC2 instances
    as needed.
    """
    EC2InstanceManager.spawn_if_needed()

def task_manage_ec2_instances():
    """
    Calls the instance creation logic in a non-blocking manner.
    """
    reactor.callInThread(threaded_manage_ec2_instances)

# Only call the instance auto-spawning if enabled.
if settings.FEEDERD_ALLOW_EC2_LAUNCHES:
    logger.debug("feederd will automatically scale EC2 instances.")
    task.LoopingCall(task_manage_ec2_instances).start(
        settings.FEEDERD_AUTO_SCALE_INTERVAL, now=True)
