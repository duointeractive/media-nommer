"""
This module contains tasks that are executed at intervals, and is imported at
the time the server is started. Much of :doc:`../feederd`'s 'intelligence'
can be found here.

All functions prefixed with ``task_`` are task functions that are registered
with the Twisted_ reactor. All functions prefixed with ``threaded_`` are
the interesting bits that actually do things.
"""
from twisted.internet import task, reactor
from media_nommer.conf import settings
from media_nommer.utils import logger
from media_nommer.feederd.job_cache import JobCache
from media_nommer.feederd.ec2_instance_manager import EC2InstanceManager
from media_nommer.feederd import job_state_notifier

def threaded_check_for_job_state_changes():
    """
    Checks the SQS queue specified in the
    :py:data:`SQS_JOB_STATE_CHANGE_QUEUE_NAME <media_nommer.conf.settings.SQS_JOB_STATE_CHANGE_QUEUE_NAME>`
    setting for announcements of state changes from the EC2_ instances running
    :doc:`../ec2nommerd`. This lets :doc:`../feederd` know it needs to get
    updated job details from the SimpleDB_ domain defined in the
    :py:data:`SIMPLEDB_JOB_STATE_DOMAIN <media_nommer.conf.settings.SIMPLEDB_JOB_STATE_DOMAIN>`
    setting.
    """
    changed_jobs = JobCache.refresh_jobs_with_state_changes()
    for job in changed_jobs:
        job_state_notifier.send_notification(job)
    # If jobs have completed, remove them from the job cache.
    JobCache.uncache_finished_jobs()

def task_check_for_job_state_changes():
    """
    Checks for job state changes in a non-blocking manner.

    Calls :py:func:`threaded_check_for_job_state_changes`.
    """
    reactor.callInThread(threaded_check_for_job_state_changes)

def threaded_prune_jobs():
    """
    Sometimes failure happens, but a Nommer doesn't handle said failure
    gracefully. Instead of state changing to ``ERROR``, it gets stuck in
    some un-finished state in the SimpleDB_ domain defined in
    :py:data:`SIMPLEDB_JOB_STATE_DOMAIN <media_nommer.conf.settings.SIMPLEDB_JOB_STATE_DOMAIN>`
    setting.

    This process finds jobs that haven't been updated in a very long time
    (a day or so) that are probably dead. It marks them with an ``ABANDONED``
    state, letting us know something went really wrong.
    """
    JobCache.abandon_stale_jobs()
    # Expire any newly abandoned jobs, too. Removes them from job cache.
    JobCache.uncache_finished_jobs()

def task_prune_jobs():
    """
    Prune expired or abandoned jobs from the domain specified in the
    :py:data:`SIMPLEDB_JOB_STATE_DOMAIN <media_nommer.conf.settings.SIMPLEDB_JOB_STATE_DOMAIN>`
    setting. Also prunes :doc:`../feederd`'s job cache.

    Calls :py:func:`threaded_prune_jobs`.
    """
    reactor.callInThread(threaded_prune_jobs)

def threaded_manage_ec2_instances():
    """
    Looks at the current number of jobs needing encoding and compares them
    to the pool of currently running EC2_ instances. Spawns more instances
    as needed.

    See source of
    :py:meth:`media_nommer.feederd.ec2_instance_manager.EC2InstanceManager.spawn_if_needed`
    for the logic behind this.
    """
    EC2InstanceManager.spawn_if_needed()

def task_manage_ec2_instances():
    """
    Calls the instance creation logic in a non-blocking manner.

    Calls :py:func:`threaded_manage_ec2_instances`.
    """
    reactor.callInThread(threaded_manage_ec2_instances)

def register_tasks():
    """
    Registers all tasks. Called by the :doc:`../feederd` Twisted_ plugin.
    """
    task.LoopingCall(task_check_for_job_state_changes).start(
                            settings.FEEDERD_JOB_STATE_CHANGE_CHECK_INTERVAL,
                            now=False)

    task.LoopingCall(task_prune_jobs).start(
                            settings.FEEDERD_PRUNE_JOBS_INTERVAL,
                            now=True)

    # Only register the instance auto-spawning if enabled.
    if settings.FEEDERD_ALLOW_EC2_LAUNCHES:
        logger.debug("feederd will automatically scale EC2 instances.")
        task.LoopingCall(task_manage_ec2_instances).start(
                            settings.FEEDERD_AUTO_SCALE_INTERVAL, now=False)
