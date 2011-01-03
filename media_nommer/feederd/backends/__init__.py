from media_nommer.feederd.conf import settings

def get_storage_backend_from_conn_str(conn_str):
    print "CONN STR", conn_str
    print "BACKENDS", settings.STORAGE_BACKENDS
    protocol = conn_str.split(':')[0]
    backend = settings.STORAGE_BACKENDS[protocol]
    print "BACKEND", backend, __import__(backend)