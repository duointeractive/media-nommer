import json
from twisted.web.resource import Resource, NoResource

class RoutingResource(Resource):
    """
    Provides simple routing of resources based on the key values in the
    :attr:`PATHS` dict. The ``path`` arg to getChild is used to perform a
    lookup on the :attr:`PATHS` dict, instantiating and returning the value
    (as Resource sub-class).
    """
    PATHS = {
        #'urlname': ResourceClassRef,
    }

    def getChild(self, path, request):
        """
        Handles matching a URL path to an API method.

        :param str path: The component of the URL path being routed against.
        :rtype: Resource
        :returns: The Resource for the requested API method.
        """
        # Check the PATHS dict for which resource should be returned for
        # any given path.
        resource = self.PATHS.get(path)
        if resource:
            # Instantiate the matching Resource child and return it.
            return resource()
        else:
            # No dict key matching the path was found. 404 it.
            return NoResource()

class BasicJSONResource(Resource):
    """
    Mixin for JSON Resource objects. No particular execution order is
    enforced here, just return the value of :method:`get_context_json` to
    the user.
    """
    #noinspection PyUnusedLocal
    def __init__(self, *args, **kwargs):
        """
        Important part to note here is that self.context is the dict that
        we serialize and return to the user. Add any key/values in here that
        the user needs to see.
        """
        Resource.__init__(self)

        # This holds the user's parsed JSON input, if applicable.
        self.user_input = None
        # The payload we return to the user.
        self.context = {
            'success': True
        }

    def set_error(self, message):
        """
        Sets an error state and HTTP code.

        :param str message: The error message to return in the response.
        """
        self.context = {
            'success': False,
            'message': message,
            }

    def parse_user_input(self, request):
        """
        Parses the user's JSON input.

        :returns: The user's input dict, or None if there was no input.
        """
        request.content.seek(0)
        raw_input = request.content.read()

        if raw_input:
            return json.loads(raw_input)
        else:
            return None

    def set_context(self, request):
        """
        Adjusts the :attr:`context` attribute to contain whatever data will
        be returned by :meth:`render_POST`.
        """
        pass

    def get_context_json(self):
        """
        Handle construction of the response and return it.

        :rtype: str
        :returns: A serialized JSON string to return to the user.
        """
        return json.dumps(self.context)

    def render_POST(self, request):
        """
        Finishes up the rendering by returning the JSON dump of the context.

        :rtype: str
        :returns: The JSON-serialized context dict.
        """
        self.user_input = self.parse_user_input(request)
        self.set_context(request)
        return self.get_context_json()
