"""
This module contains code that handles notifying external services of state
changes in EncodingJobs. For example, when the state changes from
PENDING to DOWNLOADING, or ENCODING to FINISHED.
"""
import json
from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

from media_nommer.utils.http import StringProducer
from media_nommer.utils import logger

def cb_response_received(ignored, unique_id):
    """
    This is a callback function that is hit when a response comes back from
    the remote server given in EncodingJob.notify_url. We'll just log it here
    for troubleshooting purposes.
    """
    logger.info('Job state change notification HTTP Response received for job: %s' % unique_id)

def send_notification(job):
    """
    Given an EncodingJob, see if it has a ``notify_url`` set, and dispatch
    a notification to said URL (if set). Don't do any processing of the response.

    :param EncodingJob job: The job whose state has changed.
    """
    if not job.notify_url:
        # No URL to notify, hang it up here.
        return

    # This will be JSON-serialized and POSTed to the notify_url.
    data = {
        'unique_jd': job.unique_id,
        'job_state': job.job_state,
        'job_state_details': job.job_state_details,
    }

    agent = Agent(reactor)
    headers = Headers({'User-Agent': ['Twisted Web Client Example']})
    body = StringProducer(json.dumps(data))
    
    request_deferred = agent.request(
        'POST',
        # TODO: See if Twisted can be made to accept unicode..
        str(job.notify_url),
        headers,
        body)

    # This callback will handle the success only.
    request_deferred.addCallback(cb_response_received, job.unique_id)