"""
Import this client module from within your Python application or script to
use media-nommer. Note that this API requires :doc:`../feederd` to be running 
and reachable by the host that your Python application is on.
"""
from media_nommer.client.api import APIConnection

def connect(api_hostname):
    """
    Returns an :py:class:`APIConnection <media_nommer.client.api.APIConnection>` 
    object, which is what you make API calls through. This is lazily loaded, so 
    connect away without worry of overhead from instantiation alone. You 
    shouldn't take much of a performance hit until you actually perform some 
    API calls.
    
    :param api_hostname: A URL with protocol, hostname, and port. No trailing slash.
    :type api_hostname: str
    :returns: An :py:class:`APIConnection <media_nommer.client.api.APIConnection>` 
        object, which has methods on it that map to feederd's RESTful API.
    """
    return APIConnection(api_hostname)
