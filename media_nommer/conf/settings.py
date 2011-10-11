"""
This module contains default global settings. When 
:doc:`../ec2nommerd` and :doc:`../feederd` daemons are started,  
:py:func:`media_nommer.conf.update_settings_from_module` takes the settings
that the user explicitly set and overrides these defaults.

You may override any of these global defaults in your ``nomconf.py`` file.
You will need to at the least provide the following settings:

* :py:data:`AWS_ACCESS_KEY_ID`
* :py:data:`AWS_SECRET_ACCESS_KEY`
* :py:data:`EC2_KEY_NAME`
"""

######################
#General AWS settings
######################

AWS_ACCESS_KEY_ID = None
"""Default: ``None`` **(User must provide)**

These AWS_ credentials are used for job state management via SimpleDB_, and
queueing with SQS_."""
AWS_SECRET_ACCESS_KEY = None
"""Default: ``None`` **(User must provide)**

These AWS_ credentials are used for job state management via SimpleDB_, and
queueing with SQS_."""

CONFIG_S3_BUCKET = 'nommer_config'
"""Default: ``'nommer_config'``

The S3_ bucket to store a copy of ``nomconf.py`` for nommer instances."""

SQS_NEW_JOB_QUEUE_NAME = 'media_nommer'
"""Default: ``'media_nommer'``

The SQS_ queue used to notify :doc:`../ec2nommerd` of new jobs."""
SQS_JOB_STATE_CHANGE_QUEUE_NAME = 'media_nommer_jstate'
"""Default: ``'media_nommer_jstate'``

The SQS_ queue used to notify :doc:`../feederd` of changes in job state.
For example, when a job goes from ``PENDING`` to ``DOWNLOADING`` or 
``ENCODING``."""

SIMPLEDB_JOB_STATE_DOMAIN = 'media_nommer'
"""Default: ``'media_nommer'``

The SimpleDB_ domain name for storing encoding job state in. For example,
the date the job was created, the current state of the job (``PENDING``,
``ENCODING``, ``FINISHED``, etc.), and the Nommer being used to do the
encoding."""
SIMPLEDB_EC2_NOMMER_STATE_DOMAIN = 'media_nommer_ec2nommer_state'
"""Default: ``'media_nommer_ec2nommer_state'``

The SimpleDB_ domain for storing heartbeat information from the
EC2_ encoder instances."""

########################
# EC2 instance settings
########################

EC2_KEY_NAME = None
"""Default: ``None`` **(User must provide)**

The AWS_ SSH key name with which to launch the EC2_ instances."""
EC2_SECURITY_GROUPS = ['media_nommer']
"""Default: ``['media_nommer']``

The AWS_ security groups to create EC2_ instances under."""
EC2_AMI_ID = 'ami-37f13d5e'
"""Default: ``The latest upstream AMI compatible with this git revision.``

The AMI ID for the media-nommer EC2_ instance."""
EC2_INSTANCE_TYPE = 'm1.large'
"""Default: ``'m1.large'``

The type of instance to run on. Must be at least ``m1.large``. ``t1.micro`` 
and ``t1.small`` instances are *NOT* supported by the default AMI."""

###############################
# Intelligent scaling settings
###############################

MAX_ENCODING_JOBS_PER_EC2_INSTANCE = 2
"""Default: ``2``

The maximum number of jobs that should ever run on a single EC2_ instance at
the same time."""
MAX_NUM_EC2_INSTANCES = 3
"""Default: ``3``

The maximum number of EC2 instances to run at a time."""
JOB_OVERFLOW_THRESH = 2
"""Default: ``2``

If the number of unfinished jobs exceeds our capacity 
(:py:data:`MAX_ENCODING_JOBS_PER_EC2_INSTANCE` * 
``<Number of Active EC2 instances>``) by this number of jobs, look at starting 
new instances if we have not already exceeded 
:py:data:`MAX_NUM_EC2_INSTANCES`."""

###################
# feederd settings
###################

FEEDERD_JOB_STATE_CHANGE_CHECK_INTERVAL = 60
"""Default: ``60``

How often :doc:`../feederd` will check for job state changes."""
FEEDERD_PRUNE_JOBS_INTERVAL = 60 * 5
"""Default: ``60 * 5``

How often :doc:`../feederd` will check for abandoned or expired jobs."""
FEEDERD_ALLOW_EC2_LAUNCHES = True
"""Default: ``True``

When ``True``, allow the launching of new EC2_ encoder instances."""
FEEDERD_ABANDON_INACTIVE_JOBS_THRESH = 3600 * 24
"""Default: ``3600 * 24``

If a job sticks in an un-finished state after this long (in seconds), it
is considered abandoned, and :doc:`../feederd` will kill discard it."""
FEEDERD_AUTO_SCALE_INTERVAL = 60
"""Default: ``60``

How often :doc:`../feederd` should see if it needs to spawn additional
EC2_ instances."""

###################
# nommerd settings
###################

NOMMERD_TERMINATE_WHEN_IDLE = True
"""Default: ``True``

When ``True``, allow the termination of idle EC2_ instances based on 
the :py:data:`NOMMERD_MAX_INACTIVITY` setting. It is important to keep in
mind that you pay for an entire hour when you start an EC2 instance, so
setting this timeout to anything below 45 minutes is probably a waste
of money. This timeout is in seconds."""
NOMMERD_MAX_INACTIVITY = 60 * 50
"""Default: ``60 * 50``

How many seconds of inactivity (not working on any jobs) before an
instance will terminate itself."""
NOMMERD_HEARTBEAT_INTERVAL = 60
"""Default: ``60``

Used by EC2_ nodes to determine how long to wait between sending a status 
update via SimpleDB_. The node will also check for inactivity greater than the 
configured value in :py:data:`NOMMERD_MAX_INACTIVITY`, and terminate itself if 
inactivity has exceeded that value, and :py:data:`NOMMERD_TERMINATE_WHEN_IDLE` 
is ``True``.
"""
NOMMERD_NEW_JOB_CHECK_INTERVAL = 60
"""Default: ``60``

An interval (in seconds) to wait between calls to AWS_ to check for new 
jobs."""
NOMMERD_QTFASTSTART_BIN_PATH = '/home/nom/.virtualenvs/media_nommer/bin/qtfaststart'
"""
The path to the qtfaststart bin used by ec2nommerd.
"""

##################
#General settings
##################

STORAGE_BACKENDS = {
    's3': 'media_nommer.core.storage_backends.s3.S3Backend',
    'http': 'media_nommer.core.storage_backends.http.HTTPBackend',
    'https': 'media_nommer.core.storage_backends.http.HTTPBackend',
    'file': 'media_nommer.core.storage_backends.file.FileBackend',
}
"""Default: (All included storage backends)

Storage backends. The protocol is the key, the value is the backend class 
used to work with said protocol."""
