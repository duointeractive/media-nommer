"""
This file contains the global default configuration for feederd. When the
daemon starts, these are loaded as initial values, then the user's settings
override anything here.
"""
# These AWS credentials are used for job state management via SimpleDB, and
# queueing with SQS.
AWS_ACCESS_KEY_ID = None
AWS_SECRET_ACCESS_KEY = None

# The SQS queue to use for storing encoding state info.
SQS_QUEUE_NAME = None

# The SimpleDB domain name for storing encoding job state in.
SIMPLEDB_DOMAIN_NAME = None

# A tuple of nommer config dicts.
NOMMERS = ()

# Storage backends. The protocol is the key, the value is the class used to
# access said protocol.
STORAGE_BACKENDS = {
    's3': 'media_nommer.core.storage_backends.s3.S3Backend',
}

# Job state backends track job queues and the state of the entries.
JOB_STATE_BACKEND = 'media_nommer.core.job_state_backends.aws.AWSJobStateBackend'
