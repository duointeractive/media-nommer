"""
ec2nommerd may eventually grow a really simple JSON API for feederd to
optionally check up on instances individually.

This JSON API is primarily used for executing server commands from
a remote TCP connection. The :class:`APIResource` class is the top-level
entry in here where everything gets started from.
"""
from twisted.web.resource import NoResource, Resource
import job

class APIResource(Resource):
    """
    Top level

    Path: /
    """

    def getChild(self, path, request):
        if path == 'job':
            return job.JobResource()
        else:
            return NoResource()