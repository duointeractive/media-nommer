"""
This is the top-level API module. You should generally instantiate the
APIConnection object in here by using media_nommer.client.connect() instead
of direct initialization of APIConnection.

The APIConnection class is your link to feederd, which runs a RESTful JSON API.
"""
import simplejson
from media_nommer.client.server_io import APIRequest

class APIConnection(object):
    """
    Your application's means of communicating with feederd's RESTful JSON API.
    The public methods on this class correspond to API calls.
    
    API calls return media_nommer.client.server_io.APIResponse objects with
    the results of your queries. Check the APIResponse.data attrib for your
    un-serialized results.
    """
    def __init__(self, api_hostname):
        """
        This should generally only be called by media_nommer.client.connect().
        
        Do any setup work to prepare this object for communication with
        feederd's API. This method constructor should be as lazy as possible.
        
        Args:
            A URL string with protocol, hostname, and port. No trailing slash.
        """
        self.api_hostname = api_hostname
        
    def _send_request(self, request_path, job_data):
        """
        Helper method for sending an API request. Pulls some values off of
        this APIConnection object to avoid repetition.
        
        Returns:
            A media_nommer.client.server_io.APIResponse object with the result
            of sending the APIRequest object this method forms. Your application
            will be interested in the APIResponse.data attribute, which is the
            un-serialized response from the server. 
        """
        return APIRequest(self.api_hostname, request_path, job_data).send()
    
    ##############################
    ### Begin API call methods ###
    ##############################
        
    def job_submit(self, source_path, dest_path, job_options, notify_url=None):
        """
        Submits an encoding job to feederd. This is an async call, so you may
        want to specify a notify_url for job state notifications to be sent to.
        
        source_path: The path string to the master file to encode.
        dest_path: The path string to where you'd like the encoded files to
            be saved to.
        job_options: A dictionary with additional job options like bitrates,
            target encoding formats, etc. These options can vary widely based
            on the Nommer and the formats you're asking for.
        notify_url: A URL to send job state updates to.
        
        Returns:
            A media_nommer.client.server_io.APIResponse object.
        """
        job_data = {
            'source_path': source_path,
            'dest_path': dest_path,
            'notify_url': notify_url,
            # Note that the many/varied encoding job options appear under
            # their own key, separate from the args/kwargs that job_submit()
            # has for common, important stuff.
            'job_options': job_options,
        }
        
        return self._send_request('job/submit', job_data)