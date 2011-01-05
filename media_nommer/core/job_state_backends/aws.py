"""
Contains an AWS job state backend that uses services such as SimpleDB and
SQS for storage.
"""
import datetime
import random
import hashlib
import boto
from boto.sqs.message import Message
from media_nommer.conf import settings
from media_nommer.core.job_state_backends.base_backend import BaseJobStateBackend, BaseEncodingJob

class AWSEncodingJob(BaseEncodingJob):
    def _generate_unique_job_id(self):
        random_salt = random.random()
        combo_str = "%s%s%s%s" % (self.source_path,
                                  self.dest_path,
                                  str(self.job_options),
                                  random_salt)
        return hashlib.sha512(combo_str).hexdigest()[:50]

    def save(self):
        """
        Given an EncodingJob, save it to SimpleDB and SQS. 
        """
        self.backend.wipe_all_job_data()
        # Is this a new job that needs creation?
        is_new_job = not self.unique_id
        # Generate this once so our microseconds stay the same from
        # creation time to updated time.
        now_dtime = datetime.datetime.now()

        if is_new_job:
            # This serves as the "FK" equivalent.
            unique_id = self._generate_unique_job_id()
            # Create the item in the domain.
            job = self.backend.aws_sdb_domain.new_item(unique_id)
            # Start populating values.
            job['unique_id'] = unique_id
            job['creation_dtime'] = now_dtime
            job['status'] = self.backend.JOB_STATES['PENDING']
        else:
            # Retrieve the existing item for the job.
            job = self.backend.aws_sdb_domain.get_item(encoding_job.unique_id)

        job['preset'] = self.preset
        job['options'] = self.job_options
        job['status'] = self.job_state
        job['last_modified_dtime'] = now_dtime
        job.save()

        if is_new_job:
            sqs_message = Message()
            sqs_message.set_body(job['unique_id'])
            self.backend.aws_sqs_queue.write(sqs_message)

class AWSJobStateBackend(BaseJobStateBackend):
    def __init__(self, *args, **kwargs):
        super(AWSJobStateBackend, self).__init__(self, *args , **kwargs)
        # Start as a None value so we can lazy load.
        self._aws_sdb_connection = None
        # Ditto.
        self._aws_sdb_domain = None
        # Another ditto.
        self._aws_sqs_connection = None
        # Triple ditto.
        self._aws_sqs_queue = None

    @property
    def aws_sdb_connection(self):
        """
        Lazy-loading of the SimpleDB boto connection. Refer to this instead of
        referencing self._aws_sdb_connection directly.
        
        Returns:
            A boto connection to Amazon's SimpleDB interface.
        """
        if not self._aws_sdb_connection:
            self._aws_sdb_connection = boto.connect_sdb(
                settings.AWS_ACCESS_KEY_ID,
                settings.AWS_SECRET_ACCESS_KEY)
        return self._aws_sdb_connection

    @property
    def aws_sdb_domain(self):
        """
        Lazy-loading of the SimpleDB boto domain. Refer to this instead of
        referencing self._aws_sdb_domain directly.

        Returns:
           A boto SimpleDB domain for this workflow.
        """
        if not self._aws_sdb_domain:
            self._aws_sdb_domain = self.aws_sdb_connection.create_domain(settings.SIMPLEDB_DOMAIN_NAME)
        return self._aws_sdb_domain

    @property
    def aws_sqs_connection(self):
        """
        Lazy-loading of the SQS boto connection. Refer to this instead of
        referencing self._aws_sqs_connection directly.
        
        Returns:
            A boto connection to Amazon's SimpleDB interface.
        """
        if not self._aws_sqs_connection:
            self._aws_sqs_connection = boto.connect_sqs(
                settings.AWS_ACCESS_KEY_ID,
                settings.AWS_SECRET_ACCESS_KEY)
        return self._aws_sqs_connection

    @property
    def aws_sqs_queue(self):
        """
        Lazy-loading of the SQS boto queue. Refer to this instead of
        referencing self._aws_sqs_queue directly.

        Returns:
           A boto SQS queue.
        """
        if not self._aws_sqs_queue:
            self._aws_sqs_queue = self.aws_sqs_connection.create_queue(
                settings.SQS_QUEUE_NAME)
        return self._aws_sqs_queue

    def get_job_class(self):
        """
        Returns a reference to this backend's EncodingJob sub-class.
        """
        return AWSEncodingJob

    def wipe_all_job_data(self):
        """
        Deletes the SimpleDB domain that stores job state data. 
        
        .. warning:: This will mean that everything in the incoming bucket will 
        be scheduled for rendering again, so be careful!
        
        Returns:
            True if successful. False if not.
        """
        try:
            self.aws_sdb_connection.delete_domain(settings.SIMPLEDB_DOMAIN_NAME)
            self.aws_sqs_queue.clear()
        except boto.exception.SDBResponseError:
            # Tried to delete a domain that doesn't exist. We probably haven't
            # ran feederd before, or are doing testing.
            pass

        # Reset our local cache of the boto SDB domain object.
        self._aws_sdb_domain = None
        # Reset our local cache of the boto SQS queue object.
        self._aws_sqs_queue = None

    def get_unfinished_jobs(self):
        """
        Queries SimpleDB for a list of pending jobs that have not yet been
        finished. 
        
        Returns:
            A SimpleDB resultset.
        """
        return self.aws_sdb_domain.select("SELECT * FROM %s" % settings.SIMPLEDB_DOMAIN_NAME)
