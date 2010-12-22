"""
This twistd plugin is where the nommerd is started. In addition to starting
the TCPServer process, a few other things are tied in like scheduling checks
of the S3 incoming buckets and determining whether more EC2 nodes are needed.
"""
from zope.interface import implements
from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import internet
from twisted.web.server import Site

from media_nommer.nommerd.conf import settings
from media_nommer.nommerd import interval_tasks
from media_nommer.nommerd.exceptions import NoConfigFileException
from media_nommer.nommerd.web.urls import URL_ROOT

class Options(usage.Options):
    """
    Some assorted configuration options for the twistd nommerd plugin.
    
    http://twistedmatrix.com/documents/current/api/twisted.python.usage.Options.html
    """
    # Set up the parameters we're looking for.
    optParameters = [
         ["port", "p", 8001, "The port number to listen on."],
         ["config", "c", "nomconf", "Config file"]
    ]


class WebApiServiceMaker(object):
    """
    Used by twisted's plugin architecture to spawn the web server service.
    """
    implements(IServiceMaker, IPlugin)
    tapname = "nommerd"
    description = "Starts the media-nommer nommerd."
    options = Options

    def makeService(self, options):
        """
        Construct a TCPServer from a Site factory, along with our URL
        structure module.
        """
        self.load_settings(options)
        return internet.TCPServer(int(options['port']), Site(URL_ROOT))

    def load_settings(self, options):
        cfg_file = options['config']

        try:
            user_settings = __import__(cfg_file)
        except ImportError:
            message = "The config module '%s' could not be found in your" \
                      "sys.path. Correct your path or specify another config " \
                      "module with the --config parameter when running the " \
                      "nommerd Twisted plugin." % cfg_file
            raise NoConfigFileException(message)

        settings.update_from_user_settings(user_settings)

# Now construct an object which *provides* the relevant interfaces
# The name of this variable is irrelevant, as long as there is *some*
# name bound to a provider of IPlugin and IServiceMaker.
service_maker = WebApiServiceMaker()
