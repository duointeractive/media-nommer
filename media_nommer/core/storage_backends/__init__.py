"""
Helper methods for the backend system. Only broad, generic things should be
present in this module. Anything other than the utter basics should be here.
"""
from media_nommer.conf import settings
from media_nommer.utils.mod_importing import import_class_from_module_string
from media_nommer.utils.uri_parsing import get_values_from_media_uri

def get_storage_backend_for_protocol(protocol):
    """
    Given a protocol string, return the storage backend that has been tasked
    with serving said protocol.
    
    :param str protocol: A protocol string like 'http', 'ftp', or 's3'.
    :returns: A storage backend for the specified protocol.
    """
    backend_class_fqpn = settings.STORAGE_BACKENDS[protocol]
    return import_class_from_module_string(backend_class_fqpn)

def get_storage_backend_for_uri(uri):
    """
    Given a URI, return a storage backend capable of interacting with it.
    """
    values = get_values_from_media_uri(uri)
    return get_storage_backend_for_protocol(values['protocol'])
