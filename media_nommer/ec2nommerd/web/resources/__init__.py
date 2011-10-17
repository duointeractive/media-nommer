"""
This JSON API is primarily used for executing server commands from
a remote TCP connection. The :class:`APIResource` class is the top-level
entry in here where everything gets started from.
"""
from twisted.web.resource import NoResource, Resource

class APIResource(Resource):
    """
    Top level

    Path: /
    """

    def getChild(self, path, request):
        # We don't have anything to see here just yet.
        return NoResource()