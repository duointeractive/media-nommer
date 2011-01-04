"""
This module contains tasks that are executed at intervals, and is imported at
the time the server is started.
"""
from twisted.internet import task, threads, reactor
from twisted.python import log
from media_nommer.scavengerd.conf import settings

# Holds instances of BaseNommer sub-classes. These are best thought of as the
# interfaces to getting stuff done.
NOMMER_INSTANCES = []

# Instantiate Nommers for each workflow. Store them in NOMMER_INSTANCES.
log.msg('Instantiating nommers')
for workflow in settings.WORKFLOWS:
    # Split the NOMMER FQPN into a list.
    components = workflow['NOMMER'].split('.')
    # Generate a FQPN with everything but the Nommer's class name.
    nom_module_str = '.'.join(components[:-1])
    # The class name of the Nommer.
    class_name = components[-1]
    # Import the Nommer's module and the class itself.
    nommer = __import__(nom_module_str, globals(), locals(), [class_name])
    # Get the Nommer class for instantiation.
    NommerClass = getattr(nommer, class_name)
    # Instantiate the Nommer and stick it in the list of workflows to track.
    NOMMER_INSTANCES.append(NommerClass(workflow))

def run_every_second():
    """
    Just an example task.
    """
    print "a second has passed"
#task.LoopingCall(run_every_second).start(1.0, now=False)

def threaded_check_s3_in_buckets():
    """
    Checks all S3 In Buckets for incoming files to encode.
    """
    global NOMMER_INSTANCES
    for nommer in NOMMER_INSTANCES:
        print "Nommer", nommer
        nommer.sync_queue_with_db()

def callback_check_s3_in_buckets(x):
    log.msg("Incoming queue checking cycle complete.")

def task_check_s3_in_buckets():
    """
    Calls the incoming bucket checking functions in a separate thread to prevent
    this long call from blocking us.
    
    TODO: Figure out how to not spawn a new thread with each loop of this.
    That is expensive. Earlier attempts failed, please be my guest.
    """
    #reactor.callInThread(threaded_check_s3_in_buckets)
    d = threads.deferToThread(threaded_check_s3_in_buckets)
    d.addCallback(callback_check_s3_in_buckets)
task.LoopingCall(task_check_s3_in_buckets).start(30, now=True)
