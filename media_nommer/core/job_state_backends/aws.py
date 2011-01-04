"""
Contains an AWS job state backend that uses services such as SimpleDB and
SQS for storage.
"""
import boto
from media_nommer.conf import settings
from media_nommer.core.job_state_backends.base_backend import JobStateBackend

class AWSJobStateBackend(JobStateBackend):
    def __init__(self):
        #super(AWSJobStateBackend, self).__init__(self, args*, kwargs**)
        # Start as a None value so we can lazy load.
        self._aws_s3_connection = None
        # Start as a None value so we can lazy load.
        self._aws_sdb_connection = None
        # Ditto.
        self._aws_sdb_domain = None

    @property
    def aws_s3_connection(self):
        """
        Lazy-loading of the S3 boto connection. Refer to this instead of
        referencing self._aws_s3_connection directly.
        
        Returns:
            A boto connection to Amazon's S3 interface.
        """
        if not self._aws_s3_connection:
            self._aws_s3_connection = boto.connect_s3(
                settings.AWS_ACCESS_KEY_ID,
                settings.AWS_SECRET_ACCESS_KEY)
        return self._aws_s3_connection

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

    def wipe_all_job_data(self):
        """
        Deletes the SimpleDB domain that stores job state data. 
        
        .. warning:: This will mean that everything in the incoming bucket will 
        be scheduled for rendering again, so be careful!
        
        Returns:
            True if successful. False if not.
        """
        try:
            retval = self.aws_sdb_connection.delete_domain(settings.SIMPLEDB_DOMAIN_NAME)
        except boto.exception.SDBResponseError:
            # Tried to delete a domain that doesn't exist. We probably haven't
            # ran feederd before, or are doing testing.
            retval = True
        # Reset our local cache of the boto domain object.
        self._aws_sdb_domain = None
        # True if successful.
        return retval

    def get_unfinished_jobs(self):
        """
        Queries SimpleDB for a list of pending jobs that have not yet been
        finished. This is useful in determining which files in the incoming
        S3 bucket need to be added to the DB.
        
        Returns:
            A list of filenames residing in the incoming bucket that are 
            still being worked on.
        """
        domain = self.aws_sdb_domain
        db_jobs = domain.select("SELECT * FROM %s" % settings.SIMPLEDB_DOMAIN_NAME)
        return [job['key_name'] for job in db_jobs]

    def create_new_job_in_db(self, job_key_name):
        """
        Given the filename of any of a key in the workflow's incoming bucket,
        create a new encoding job in SimpleDB.
        """
        new_job = self.aws_sdb_domain.new_item(job_key_name)
        new_job['job_key_name'] = job_key_name
        new_job['status'] = defines.JOB_STATE_PENDING
        new_job['creation_dtime'] = datetime.datetime.now()
        new_job['last_modified_dtime'] = datetime.datetime.now()
        new_job.save()
