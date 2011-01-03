"""
Import this client module from within your Python application or script to
use media-nommer. Note that this API requires feederd to be running and
reachable by the host that your Python application is on.
"""
from media_nommer.client.api import APIConnection

def connect(api_hostname):
    """
    Returns an APIConnection object, which is what you make API calls through.
    This is lazily loaded, so connect away without worry of overhead. You
    shouldn't take much of a performance hit until you actually perform
    some API calls.
    
    Args:
        api_hostname: A string URL (with port) to your feederd's REST API.
            By default, this is port 8001. For example: http://somehost:8001
    
    Returns:
        An APIConnection object, which has methods on it that map to feederd's
        RESTful API.
    """
    return APIConnection(api_hostname)