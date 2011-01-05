"""
Helper methods for the backend system. Only broad, generic things should be
present in this module. Anything other than the utter basics should be here.
"""
from media_nommer.conf import settings
from media_nommer.utils.mod_importing import import_class_from_module_string

# Used to store the currently active job state backend. Do not try to access
# this directly, go through get_default_backend().
__BACKEND_INSTANCE = None

def get_default_backend():
    """
    Returns an instance of the default job state backend. Uses lazy loading
    to put off the import until needed.
    
    .. tip: 
        You should not import/instantiate backends directly. use this
        method instead.
    """
    global __BACKEND_INSTANCE

    if not __BACKEND_INSTANCE:
        __BACKEND_INSTANCE = import_class_from_module_string(settings.JOB_STATE_BACKEND)()

    return __BACKEND_INSTANCE

# You can import this for convenience.
EncodingJob = get_default_backend().get_job_class()
