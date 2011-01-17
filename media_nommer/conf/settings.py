"""
This file contains the global default configuration. When the
daemons start, these are loaded as initial values, then the user's settings
override anything here.
"""

"""
General AWS settings
"""
# These AWS credentials are used for job state management via SimpleDB, and
# queueing with SQS.
AWS_ACCESS_KEY_ID = None
AWS_SECRET_ACCESS_KEY = None

# The S3 bucket to store a copy of nomconf.py for nommer instances.
CONFIG_S3_BUCKET = 'nommer_config'

# The SQS queue to use for storing encoding state info.
SQS_QUEUE_NAME = 'media_nommer'
SQS_JOB_STATE_CHANGE_QUEUE_NAME = 'media_nommer_jstate'

# The SimpleDB domain name for storing encoding job state in.
SIMPLEDB_DOMAIN_NAME = 'media_nommer'
# SimpleDB domain for storing EC2 instance nommer state in.
SIMPLEDB_EC2_NOMMER_STATE = 'media_nommer_ec2nommer_state'

"""
Intelligent scaling settings
"""
# The maximum number of jobs that should ever run on a single instance at
# the same time.
MAX_ENCODING_JOBS_PER_EC2_INSTANCE = 1
# The maximum number of EC2 instances to run at a time.
MAX_NUM_EC2_INSTANCES = 3
# If we our number of unfinished jobs exceeds our capacity by this number of
# jobs, look at starting new instances.
JOB_OVERFLOW_THRESH = 2

"""
EC2 instance settings
"""
# The user key with which to launch the instance.
EC2_KEY_NAME = 'your_key'
# The security groups to create EC2 instances under.
EC2_SECURITY_GROUPS = ['media_nommer']
# The AMI ID for the media-nommer EC2 instance.
EC2_AMI_ID = 'ami-847c8ded'
# The type of instance to run on. Must be at least m1.large. t1.micro and
# small instances are *NOT* supported by the default AMI.
EC2_INSTANCE_TYPE = 'm1.large'

"""
nommerd settings
"""
# When True, allow the termination of idle EC2 instances based on 
# the NOMMERD_MAX_INACTIVITY setting.
NOMMERD_TERMINATE_WHEN_IDLE = True
# How many seconds of inactivity (not working on any jobs) before an
# instance will terminate itself.
NOMMERD_MAX_INACTIVITY = 120
# How long to wait between sending a status update to SimpleDB from your
# EC2 encoder instances. Also check for inactivity greater than the configured
# value in NOMMERD_MAX_INACTIVITY, and terminate oneself if inactivity
# has exceeded that value, and NOMMERD_TERMINATE_WHEN_IDLE is True.
NOMMERD_HEARTBEAT_INTERVAL = 120
# An interval (in seconds) to wait between calls to AWS to check for new jobs.
NOMMERD_NEW_JOB_CHECK_INTERVAL = 60

"""
feederd settings
"""
# Number of seconds between checking the job state change queue for updates.
FEEDERD_JOB_STATE_CHANGE_CHECK_INTERVAL = 60
# How often to check for abandoned or expired jobs.
FEEDERD_PRUNE_JOBS_INTERVAL = 60
# When True, allow the launching of new EC2 instances.
FEEDERD_ALLOW_EC2_LAUNCHES = True
# If a job sticks in an un-finished state after this long (in seconds), it
# is considered abandoned, and is killed.
FEEDERD_ABANDON_INACTIVE_JOBS_THRESH = 3600 * 24
# Specifies how often feederd should see if it needs to spawn additional
# EC2 instances.
FEEDERD_AUTO_SCALE_INTERVAL = 60

"""
General settings
"""
# Storage backends. The protocol is the key, the value is the class used to
# access said protocol.
STORAGE_BACKENDS = {
    's3': 'media_nommer.core.storage_backends.s3.S3Backend',
}

# A dict of workflow presets.
PRESETS = ()
