"""
This module contains tasks that are executed at intervals, and is imported at
the time the server is started.
"""
from twisted.internet import task, threads, reactor
from media_nommer.nommerd.conf import settings

def run_every_second():
    """
    Just an example task.
    """
    print "a second has passed"
task.LoopingCall(run_every_second).start(1.0, now=False)

TEST = 0

def check_s3_in_buckets():
    import time
    print "Sleepytime"
    time.sleep(5)
    print "Done"
    return 50

def printResult(x):
    global TEST
    TEST += 1
    print "YAY", x, TEST

def task_check_s3_in_buckets():
    """
    Checks all S3 In Buckets for incoming files to encode.
    """
    reactor.callInThread(check_s3_in_buckets)
    d = threads.deferToThread(check_s3_in_buckets)
    d.addCallback(printResult)
task.LoopingCall(task_check_s3_in_buckets).start(5.0, now=True)
