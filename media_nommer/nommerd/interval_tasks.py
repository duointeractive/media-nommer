"""
This module contains tasks that are executed at intervals, and is imported at
the time the server is started.
"""
from twisted.internet import task
from twisted.internet import reactor

def run_every_second():
    """
    Just an example task.
    """
    #print "a second has passed"
    pass
task.LoopingCall(run_every_second).start(1.0, now=False)
