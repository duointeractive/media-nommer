"""
Utilities for parsing URI and URL strings.
"""
from media_nommer.utils.exceptions import BaseException

class InvalidUri(BaseException):
    """
    Raised when an invalid URI is passed to a function that consumes URIs.
    Make sure to instantiate with a helpful error message.
    """
    pass

def get_values_from_media_uri(uri_str):
    """
    Given a valid URI string, break it up into its component pieces like
    protocol, hostname, and path, along with some optional elements like 
    username, password, and port. All of these values are returned in a dict.
    
    The following keys should always be in the dict:
    * protocol
    * host
    * path
    
    The following are set when present, but absent when not:
    * port
    * username
    * password
    
    :param str uri_str: A valid URI string.
    :returns: A dict of strings.
    """
    # The dict that will be later returned.
    values = {}

    dslash_split = uri_str.split('://', 1)
    values['protocol'] = dslash_split[0]
    try:
        url_str = dslash_split[1]
    except IndexError:
        # If this split fails, we've definitely forgotten the protocol.
        msg = 'No protocol specified. Pre-pend "proto://" to your current ' \
              'value of "%s", where "proto" is your choice of protocol.' % uri_str
        raise InvalidUri(msg)

    # An '@' symbol indicates the presence of a username and/or username+pass.
    has_auth_details = '@' in url_str
    if has_auth_details:
        auth_host_split = url_str.split('@', 1)
        # Should be just the username or username@pass.
        auth_details = auth_host_split[0]

        # A colon is used to separate username from passwords.
        has_password = ':' in auth_details
        if has_password:
            user_pass_split = auth_details.split(':', 1)
            values['username'] = user_pass_split[0]
            values['password'] = user_pass_split[1]
        else:
            values['username'] = auth_details

        # Seperated the host/path from auth details. 
        host_and_path = auth_host_split[1]
    else:
        host_and_path = url_str

    # Split the host and path up.
    host_path_split = host_and_path.split('/', 1)
    values['host'] = host_path_split[0]

    try:
        values['path'] = host_path_split[1]
    except IndexError:
        # This means that no trailing slash was present in the URI str after
        # the host was specified. Assume they mean the root path.
        values['path'] = '/'

    if ':' in values['host']:
        # Looks like they specified a port.
        host_port_split = values['host'].split(':')
        values['host'] = host_port_split[0]
        values['port'] = host_port_split[1]

    return values
