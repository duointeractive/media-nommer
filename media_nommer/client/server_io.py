"""
API request abstraction and helpers. This module and its contents should not be 
used directly.
"""
import urllib
import urllib2
import simplejson

class APIRequest(object):
    """
    A basic API request from which all will inherit. Does some basic error
    and authentication handling, and serializes/de-serializes request and
    responses.
    """
    def __init__(self, api_hostname, request_path, data):
        """
        Args:
            api_hostname: The protocol, hostname, and port of your feederd's
                REST API. There should be no trailing slash.
            request_path: The URL to query. No leading or trailing slash.
            data: A dict object of key/value pairs to JSON encode and send
                to feederd's REST API. Make sure anything you send is
                serializable by simplejson.
        """
        self.data = data
        self.api_hostname = api_hostname
        self.request_path = request_path
        
    def send(self):
        """
        Sends the query, returns an APIResponse object with the un-serialized
        response included.
        
        Returns:
            An APIResponse object.
        """
        encoded_data = urllib.urlencode(self.data)
        full_request_path = '%s/%s' % (self.api_hostname, self.request_path)
        request = urllib2.Request(full_request_path, encoded_data)
        response = urllib2.urlopen(request)
        return APIResponse(self, response.read())
    
class APIResponse(object):
    """
    A basic API response. Handles some simple error handling and provides some
    helpers to going figuring out what the server has to say.
    
    Your application will be interested in self.data, which is result of
    simplejson parsing feederd's response JSON.
    """
    def __init__(self, request, raw_response):
        """
        Args:
            request: The APIRequest object that created this response.
            raw_response: The raw response that urllib2 got from feederd.
        """
        self.request = request
        self.raw_response = raw_response
        # The response JSON parsed by simplejson. This is what you mostly
        # will want to look at from within your application.
        self.data = simplejson.loads(self.raw_response)
        
    def __str__(self):
        """
        When str()'d, just show the underlying response data.
        """
        return repr(self.data)
    
    def is_success(self):
        """
        Indicates whether the call completed without errors.
        
        Returns:
            If there were no errors, returns True, else False.
        """
        return True