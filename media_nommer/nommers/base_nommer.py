"""
Classes in this module serve as a basis for Nommers. This should be thought
of as a protocol or a foundation to assist in maintaining a consistent API
between Nommers.
"""
import boto
from media_nommer.nommers.exceptions import NommerConfigException

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

    def get_sdb_domain_name(self):
        """
        Returns:
            The AWS SimpleDB domain name for this workflow. Based off of 
            the NAME setting.
        """
        name = self.CONFIG['NAME']
        return 'nommer_%s' % name

    def get_sdb_domain(self):
        """
        Returns:
            The SimpleDB domain for this workflow.
        """
        return self.aws_sdb_connection.create_domain(self.get_sdb_domain_name())
