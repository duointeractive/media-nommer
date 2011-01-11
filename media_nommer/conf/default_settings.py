"""
This file contains the global default configuration. When the
daemons start, these are loaded as initial values, then the user's settings
override anything here.
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

# If a job sticks in an un-finished state after this long (in seconds), it
# is considered abandoned, and is killed.
ABANDON_INACTIVE_JOBS_THRESH = 3600 * 24

# The maximum number of jobs that should ever run on a single instance at
# the same time.
MAX_ENCODING_JOBS_PER_EC2_INSTANCE = 1

# The maximum number of EC2 instances to run at a time.
MAX_NUM_EC2_INSTANCES = 1

# A dict of workflow presets.
PRESETS = ()

# Storage backends. The protocol is the key, the value is the class used to
# access said protocol.
STORAGE_BACKENDS = {
    's3': 'media_nommer.core.storage_backends.s3.S3Backend',
}

# Job state backends track job queues and the state of the entries.
JOB_STATE_BACKEND = 'media_nommer.core.job_state_backends.aws.AWSJobStateBackend'
