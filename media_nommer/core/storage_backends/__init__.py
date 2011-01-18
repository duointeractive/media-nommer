"""
Storage backends are used to handle download and uploading content to a number
of different protocols in an abstracted manner. 

media-nommer uses URI strings to represent media locations, whether it be
the file to download and encode, or where the output should be uploaded to.
A reference to the correct backend for a URI can be found using the
:py:func:`get_backend_for_uri` function.
"""
from media_nommer.conf import settings
from media_nommer.utils.mod_importing import import_class_from_module_string
from media_nommer.utils.uri_parsing import get_values_from_media_uri

def get_backend_for_protocol(protocol):
    """
    Given a protocol string, return the storage backend that has been tasked
    with serving said protocol.
    
    :param str protocol: A protocol string like 'http', 'ftp', or 's3'.
    :returns: A storage backend for the specified protocol.
    """
    backend_class_fqpn = settings.STORAGE_BACKENDS[protocol]
    return import_class_from_module_string(backend_class_fqpn)

def get_backend_for_uri(uri):
    """
    Given a URI string , return a reference to the storage backend class 
    capable of interacting with the protocol seen in the URI.
    
    :param str uri: The URI to find the appropriate storage backend for.
    :rtype: ``StorageBackend``
    :returns: A reference to the backend class to use with this URI.
    """
    values = get_values_from_media_uri(uri)
    return get_backend_for_protocol(values['protocol'])
