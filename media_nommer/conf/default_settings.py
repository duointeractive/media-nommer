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
# SimpleDB domain for storing EC2 instance nommer state in.
SIMPLEDB_EC2_NOMMER_STATE = 'media_nommer_ec2nommer_state'

# If a job sticks in an un-finished state after this long (in seconds), it
# is considered abandoned, and is killed.
ABANDON_INACTIVE_JOBS_THRESH = 3600 * 24
# The user key with which to launch the instance.
EC2_KEY_NAME = 'your_key'
# The security groups to create EC2 instances under.
EC2_SECURITY_GROUPS = ['media_nommer']
# The AMI ID for the media-nommer EC2 instance.
EC2_AMI_ID = 'ami-f27d8c9b'
# The type of instance to run on. Must be at least m1.large. t1.micro and
# small instances are *NOT* supported by the default AMI.
EC2_INSTANCE_TYPE = 'm1.large'
# The maximum number of jobs that should ever run on a single instance at
# the same time.
MAX_ENCODING_JOBS_PER_EC2_INSTANCE = 1
# When True, allow the launching of new EC2 instances.
ALLOW_EC2_LAUNCHES = True
# When True, allow the termination of idle EC2 instances.
ALLOW_EC2_TERMINATION = True
# The maximum number of EC2 instances to run at a time.
MAX_NUM_EC2_INSTANCES = 3
# If we our number of unfinished jobs exceeds our capacity by this number of
# jobs, look at starting new instances.
EC2_JOB_OVERFLOW_THRESH = 2

# Storage backends. The protocol is the key, the value is the class used to
# access said protocol.
STORAGE_BACKENDS = {
    's3': 'media_nommer.core.storage_backends.s3.S3Backend',
}

# Job state backends track job queues and the state of the entries.
JOB_STATE_BACKEND = 'media_nommer.core.job_state_backends.aws.AWSJobStateBackend'

# A dict of workflow presets.
PRESETS = ()
