"""
Contains the :py:class:`NodeStateManager` class, which is an abstraction layer
for storing and communicating the status of EC2_ nodes.
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
    Tracks this node's state, reports it to :doc:`../feederd`, and terminates 
    itself if certain conditions of inactivity are met.
    """
    last_dtime_i_did_something = datetime.datetime.now()

    # Used for lazy-loading the SDB connection. Do not refer to directly.
    __aws_sdb_connection = None
    # Used for lazy-loading the SDB domain. Do not refer to directly.
    __aws_sdb_nommer_state_domain = None
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
    def _aws_sdb_nommer_state_domain(cls):
        """
        Lazy-loading of the SimpleDB boto domain. Refer to this instead of
        referencing cls.__aws_sdb_nommer_state_domain directly.

        :returns: A boto SimpleDB domain for this workflow.
        """
        if not cls.__aws_sdb_nommer_state_domain:
            cls.__aws_sdb_nommer_state_domain = cls._aws_sdb_connection().create_domain(
                                    settings.SIMPLEDB_EC2_NOMMER_STATE_DOMAIN)
        return cls.__aws_sdb_nommer_state_domain

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
    def send_instance_state_update(cls, state='ACTIVE'):
        """
        Sends a status update to feederd through SimpleDB. Lets the daemon
        know how many jobs this instance is crunching right now. Also updates
        a timestamp field to let feederd know how long it has been since the
        instance's last check-in.
        
        :keyword str state: If this EC2_ instance is anything but ``ACTIVE``,
            pass the state here. This is useful during node termination.
        """
        if cls.is_ec2_instance():
            instance_id = cls.get_instance_id()
            item = cls._aws_sdb_nommer_state_domain().new_item(instance_id)
            item['id'] = instance_id
            item['active_jobs'] = cls.get_num_active_threads() - 1
            item['last_report_dtime'] = datetime.datetime.now()
            item['state'] = state
            item.save()

    @classmethod
    def contemplate_termination(cls, thread_count_mod=0):
        """
        Looks at how long it's been since this worker has done something, and
        decides whether to self-terminate.
        
        :param int thread_count_mod: Add this to the amount returned by the call
            to :py:meth:`get_num_active_threads`. This is useful when calling
            this method from a non-encoder thread.
        :rtype: bool
        :returns: ``True`` if this instance terminated itself, ``False``
            if not.
        """
        if not cls.is_ec2_instance():
            # Developing locally, don't go here.
            return False

        # This is -1 since this is also a thread doing the contemplation.
        # This would always be 1, even if we had no jobs encoding, if we
        # didn't take into account this thread.
        num_active_threads = cls.get_num_active_threads() + thread_count_mod

        if num_active_threads > 0:
            # Encoding right now, don't terminate.
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
                    cls.send_instance_state_update(state='TERMINATED')
                    instance.terminate()
            # Seeya later!
            return True
        # Continue existence, no termination.
        return False

    @classmethod
    def get_num_active_threads(cls):
        """
        Checks the reactor's threadpool to see how many threads are currently
        working. This can be used to determine how busy this node is.
        
        :rtype: int
        :returns: The number of active threads.
        """
        return len(reactor.getThreadPool().working)

    @classmethod
    def i_did_something(cls):
        """
        Pat ourselves on the back each time we do something.
        
        Used for determining whether this node's continued existence is
        necessary anymore in :py:meth:`contemplate_termination`.
        """
        cls.last_dtime_i_did_something = datetime.datetime.now()
