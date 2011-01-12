"""
Some misc. utilities for interacting with the EC2 node that the daemon
is running on.
"""
import urllib2
import boto
from media_nommer.conf import settings

# Do not directly access this.
__INSTANCE_ID = None

def get_instance_id(is_local=False):
    """
    Determine this EC2 instance's unique instance ID. Lazy load this, and
    avoid further re-queries after the first one.
    
    :param bool is_local: When True, don't try to hit EC2's meta data server,
        When False, just make up a unique ID.
        
    :rtype: str
    :returns: The EC2 instance's ID.
    """
    global __INSTANCE_ID

    if not __INSTANCE_ID:
        if is_local:
            __INSTANCE_ID = 'local-dev'
        else:
            response = urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id')
            __INSTANCE_ID = response.read()

    return __INSTANCE_ID
