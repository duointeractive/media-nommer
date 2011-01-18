"""
Some methods for tracking and reporting the state of the ec2nommerd.
"""
import urllib2
import datetime
import boto
from twisted.internet import reactor
from media_nommer.conf import settings
from media_nommer.utils import logger
from media_nommer.utils.compat import total_seconds

class NodeStateManager(object):
    """
    Tracks this node's state, reports it to feederd, and terminates itself
    if certain conditions of inactivity are met.
    
    TODO: Make these method names consistent with the JobStateBackend.
    """
    last_dtime_i_did_something = datetime.datetime.now()

    # Used for lazy-loading the SDB connection. Do not refer to directly.
    __aws_sdb_connection = None
    # Used for lazy-loading the SDB domain. Do not refer to directly.
    __aws_sdb_domain = None
    # Used for lazy-loading the EC2 connection. Do not refer to directly.
    __aws_ec2_connection = None
    # Store the instance ID for this EC2 node (if not local).
    __instance_id = None

    @classmethod
    def _aws_ec2_connection(cls):
        """
        Lazy-loading of the EC2 boto connection. Refer to this instead of
        referencing cls.__aws_ec2_connection directly.
        
        :returns: A boto connection to Amazon's EC2 interface.
        """
        if not cls.__aws_ec2_connection:
            cls.__aws_ec2_connection = boto.connect_ec2(
                settings.AWS_ACCESS_KEY_ID,
                settings.AWS_SECRET_ACCESS_KEY)
        return cls.__aws_ec2_connection

    @classmethod
    def _aws_sdb_connection(cls):
        """
        Lazy-loading of the SimpleDB boto connection. Refer to this instead of
        referencing cls.__aws_sdb_connection directly.
        
        :returns: A boto connection to Amazon's SimpleDB interface.
        """
        if not cls.__aws_sdb_connection:
            cls.__aws_sdb_connection = boto.connect_sdb(
                settings.AWS_ACCESS_KEY_ID,
                settings.AWS_SECRET_ACCESS_KEY)
        return cls.__aws_sdb_connection

    @classmethod
    def _aws_sdb_domain(cls):
        """
        Lazy-loading of the SimpleDB boto domain. Refer to this instead of
        referencing cls.__aws_sdb_domain directly.

        :returns: A boto SimpleDB domain for this workflow.
        """
        if not cls.__aws_sdb_domain:
            cls.__aws_sdb_domain = cls._aws_sdb_connection().create_domain(
                                    settings.SIMPLEDB_EC2_NOMMER_STATE_DOMAIN)
        return cls.__aws_sdb_domain

    @classmethod
    def get_instance_id(cls, is_local=False):
        """
        Determine this EC2 instance's unique instance ID. Lazy load this, and
        avoid further re-queries after the first one.
               
        :param bool is_local: When True, don't try to hit EC2's meta data server,
            When False, just make up a unique ID.
            
        :rtype: str
        :returns: The EC2 instance's ID.
        """
        if not cls.__instance_id:
            if is_local:
                cls.__instance_id = 'local-dev'
            else:
                aws_meta_url = 'http://169.254.169.254/latest/meta-data/instance-id'
                response = urllib2.urlopen(aws_meta_url)
                cls.__instance_id = response.read()

        return cls.__instance_id

    @classmethod
    def is_ec2_instance(cls):
        """
        Determine whether this is an EC2 instance or not.
        
        :rtype: bool
        :returns: ``True`` if this is an EC2 instance, ``False`` if otherwise.
        """
        return cls.get_instance_id() != 'local-dev'

    @classmethod
    def send_instance_state_update(cls):
        """
        Sends a status update to feederd through SimpleDB. Lets the daemon
        know how many jobs this instance is crunching right now. Also updates
        a timestamp field to let feederd know how long it has been since the
        instance's last check-in.
        """
        if cls.is_ec2_instance():
            instance_id = cls.get_instance_id()
            item = cls._aws_sdb_domain().new_item(instance_id)
            item['id'] = instance_id
            item['active_jobs'] = len(reactor.getThreadPool().working) - 1
            item['last_report_dtime'] = datetime.datetime.now()
            item.save()

    @classmethod
    def contemplate_termination(cls):
        """
        Looks at how long it's been since this worker has done something, and
        decides whether to self-terminate.
        
        TODO: State update on termination?
        
        :rtype: bool
        :returns: ``True`` if this instance terminated itself, ``False``
            if not.
        """
        if not cls.is_ec2_instance():
            # Developing locally, don't go here.
            return False

        tdelt = datetime.datetime.now() - cls.last_dtime_i_did_something
        # Total seconds of inactivity.
        inactive_secs = total_seconds(tdelt)

        # If we're over the inactivity threshold...
        if inactive_secs > settings.NOMMERD_MAX_INACTIVITY:
            instance_id = cls.get_instance_id()
            conn = cls._aws_ec2_connection()
            # Find this particular EC2 instance via boto.
            reservations = conn.get_all_instances(instance_ids=[instance_id])
            # This should only be one match, but in the interest of
            # playing along...
            for reservation in reservations:
                for instance in reservation.instances:
                    # Here's the instance, terminate it.
                    logger.info("Goodbye, cruel world.")
                    instance.terminate()
            # Seeya later!
            return True
        # Continue existence, no termination.
        return False

    @classmethod
    def i_did_something(cls):
        """
        Pat ourselves on the back each time we do something.
        
        Used for determining whether this node's continued existence is
        necessary anymore in :py:meth:`contemplate_termination`.
        """
        cls.last_dtime_i_did_something = datetime.datetime.now()
