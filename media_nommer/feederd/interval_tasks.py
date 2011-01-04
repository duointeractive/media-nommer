"""
This module contains tasks that are executed at intervals, and is imported at
the time the server is started.
"""
from twisted.internet import task, threads, reactor
from twisted.python import log
from media_nommer.conf import settings

def run_every_second():
    """
    Just an example task.
    """
    print "a second has passed"
#task.LoopingCall(run_every_second).start(1.0, now=False)
