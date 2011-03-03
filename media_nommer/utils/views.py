import simplejson

class BaseView(object):
    """
    The simplest base case for a view class. This is safe to use directly.
    See __new__() for the order of execution of the rendering methods.
    """

    def __new__(cls, request, *args, **kwargs):
        """
        The top-level factory function for views when called by urls.py.
        
        This method shows you the order that some of the class methods are
        called during the rendering sequence.
        """
        # Create a new instance of this class.
        view = cls.new(request, *args, **kwargs)

        # Run all of the view's generation code.
        view.view()
        return view.render()

    @classmethod
    def new(cls, *args, **kwargs):
        """
        The lower level factory method that constructs a new instance of
        the view sub-class (whatever it may be).
        """
        obj = object.__new__(cls)
        obj.__init__(*args, **kwargs)
        return obj

    def __init__(self, request, *args, **kwargs):
        """
        Re-set state variables, check to make sure that the user is
        authorized, and do some general preparation.
        """
        # Store the request object for the other methods to reach.
        self.request = request
        # Catch-all for kwargs.
        self.kwargs = kwargs
        # This is where the values to populate the RequestContext live.
        # You generally want to add keys to this dict rather than over-write
        # it with a new dict in your view.
        self.context = {
            'success': True
        }

    def set_error(self, message):
        """
        Sets an error state and HTTP code. 
        
        .. note:: You'll probably want to return your ``view()`` method 
            after calling this.
        
        :param str message: The error message to return in the response.
        """
        self.context = {
            'success': False,
            'message': message,
        }

    def render(self):
        """
        Handle construction of the response and return it.
        """
        return simplejson.dumps(self.context)

    def view(self, *args, **kwargs):
        """
        Override this with your view logic. You'll mostly want to manipulate
        self.context dictionary. If you want to check for certain conditions
        like authorization that would prevent access to this view, you'll
        want to do that in self.pre_view_checks(), which actually does something
        with return values (which view() doesn't).
        
        Does not return anything.
        """
        pass
