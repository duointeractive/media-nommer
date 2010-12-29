"""
Classes in this module serve as a basis for Nommers. This should be thought
of as a protocol or a foundation to assist in maintaining a consistent API
between Nommers.
"""
import datetime
import boto
from media_nommer.nommers.exceptions import NommerConfigException
from media_nommer.nommers import defines

class BaseNommer(object):
    """
    This is a base class that can be sub-classed by each Nommer to serve
    as a foundation. Required methods raise a NotImplemented exception
    by default, unless overridden by child classes.
    """
    def __init__(self, config):
        """
        Do some basic setup and validation. 
        """
        # These correspond to keys that should be found in each and every
        # member of the settings.WORKFLOWS tuple. Members are usually a dict,
        # and are used to instantiate Nommer objects.
        self.REQUIRED_SETTINGS = [
            'NAME',
            'AWS_ACCESS_KEY_ID',
            'AWS_SECRET_ACCESS_KEY',
            'S3_IN_BUCKET',
            'S3_OUT_BUCKET',
        ]
        # Store the values from this Nommer's settings.WORKFLOWS entry.
        self.CONFIG = config
        # Make sure that all required settings are present.
        self.check_for_required_settings()
        # Start as a None value so we can lazy load.
        self._aws_s3_connection = None
        # Start as a None value so we can lazy load.
        self._aws_sdb_connection = None
        # Ditto.
        self._aws_sdb_domain = None

    def check_for_required_settings(self):
        """
        Checks to make sure that all required settings are specified in the
        config dictionary.
        
        Raises:
            NommerConfigException when a required config value is missing
            from the config dict (self.CONFIG).
        """
        for setting in self.REQUIRED_SETTINGS:
            if not self.CONFIG.has_key(setting):
                msg = "Your nommer with name '%s' is missing a required setting: %s" % (
                    self.CONFIG['NAME'], setting,
                )
                raise NommerConfigException(msg)

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
                                    self.CONFIG['AWS_ACCESS_KEY_ID'],
                                    self.CONFIG['AWS_SECRET_ACCESS_KEY'])
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
                                    self.CONFIG['AWS_ACCESS_KEY_ID'],
                                    self.CONFIG['AWS_SECRET_ACCESS_KEY'])
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
            self._aws_sdb_domain = self.aws_sdb_connection.create_domain(self.get_sdb_domain_name())
        return self._aws_sdb_domain

    def get_sdb_domain_name(self):
        """
        Returns:
            The AWS SimpleDB domain name for this workflow. Based off of 
            the NAME setting.
        """
        name = self.CONFIG['NAME']
        return 'nommer_job_state_%s' % name

    def get_s3_in_bucket_keys(self):
        """
        Get all of the keys contained within a bucket.
        
        Returns:
            A boto.s3.bucketlistresultset.BucketListResultSet object, which is
            an iterable object that will let you gracefully iterate over large
            numbers of keys.
        """
        bucket = self.aws_s3_connection.create_bucket(self.CONFIG['S3_IN_BUCKET'])
        return bucket.list()

    def wipe_job_db(self):
        """
        Deletes the SimpleDB domain that stores job state data. 
        
        .. warning:: This will mean that everything in the incoming bucket will 
        be scheduled for rendering again, so be careful!
        
        Returns:
            True if successful. False if not.
        """
        try:
            retval = self.aws_sdb_connection.delete_domain(self.get_sdb_domain_name())
        except boto.exception.SDBResponseError:
            # Tried to delete a domain that doesn't exist. We probably haven't
            # ran feederd before, or are doing testing.
            retval = True
        # Reset our local cache of the boto domain object.
        self._aws_sdb_domain = None
        # True if successful.
        return retval

    def get_unfinished_jobs_from_db(self):
        """
        Queries SimpleDB for a list of pending jobs that have not yet been
        finished. This is useful in determining which files in the incoming
        S3 bucket need to be added to the DB.
        
        Returns:
            A list of filenames residing in the incoming bucket that are 
            still being worked on.
        """
        domain = self.aws_sdb_domain
        db_jobs = domain.select("SELECT * FROM %s" % self.get_sdb_domain_name())
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

    def sync_queue_with_db(self):
        """
        Looks at the workflow's incoming S3 bucket and syncs the contents with 
        the workflow's job state SimpleDB domain.
        
        Returns:
            A list of any newly created boto SimpleDB items.
        """
        # Un-comment for testing purposes.
        self.wipe_job_db()

        self.get_unfinished_jobs_from_db()
        incoming_keys = [key.name for key in self.get_s3_in_bucket_keys()]
        print "INCOMING KEYS", incoming_keys
        unfinished_jobs = self.get_unfinished_jobs_from_db()
        print "UNFINISHED", unfinished_jobs

        # Stores any newly created jobs for later returning.
        new_job_sdb_key_names = []
        for job_key_name in incoming_keys:
            # Only add files that have not yet been detected and stored in
            # the workflow's SimpleDB domain.
            if job_key_name not in unfinished_jobs:
                print "New file found in incoming bucket: %s" % job_key_name
                # New file found, create a job to encode it.
                self.create_new_job_in_db(job_key_name)
                new_job_sdb_key_names.append(job_key_name)

        # Un-comment for testing purposes.
        self.wipe_job_db()
        return new_job_sdb_key_names
