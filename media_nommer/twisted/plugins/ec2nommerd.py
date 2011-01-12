"""
This twistd plugin is where the feederd is started. In addition to starting
the TCPServer process, a few other things are tied in like scheduling checks
of the S3 incoming buckets and determining whether more EC2 nodes are needed.

More documentation about the Twisted plugin system can be found here:
http://twistedmatrix.com/documents/current/core/howto/plugin.html
"""
import os
from zope.interface import implements
from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import internet
from twisted.web.server import Site

from media_nommer.conf import settings
from media_nommer.conf.utils import download_settings
from media_nommer.utils.conf import NoConfigFileException
from media_nommer.ec2nommerd.web.urls import API

class Options(usage.Options):
    """
    Some assorted configuration options for the twistd ec2nommerd plugin.
    
    http://twistedmatrix.com/documents/current/api/twisted.python.usage.Options.html
    """
    # Set up the parameters we're looking for.
    optParameters = [
        ["port", "p", 8002, "The port number to listen on."],
        ["config", "c", "nomconf", "Config file."],
    ]

    optFlags = [
        ["local", "o", "Use when developing locally."],
    ]

class WebApiServiceMaker(object):
    """
    Used by twisted's plugin architecture to spawn the web server service.
    """
    implements(IServiceMaker, IPlugin)
    tapname = "ec2nommerd"
    description = "Starts the media-nommer ec2nommerd."
    options = Options

    def makeService(self, options):
        """
        Construct a TCPServer from a Site factory, along with our URL
        structure module.
        """
        self.download_settings()
        self.load_settings(options)
        self.start_tasks(options)
        return internet.TCPServer(int(options['port']), Site(API))

    def download_settings(self):
        """
        Downloads nomconf.py from the bucket specified in 
        settings.CONFIG_S3_BUCKET. feederd uploads its nomconf.py to that
        location at start time.
        
        Only do this if a ~/.nommerd_s3.cfg file exists with a valid URI.
        """
        s3_uri_path = os.path.expanduser('~/.nommerd_s3.cfg')

        s3_uri_present = os.path.exists(s3_uri_path)
        if s3_uri_present:
            print "nommerd nomconf S3 URI present, using that to " \
                  "download nomconf.py"
            s3_uri = open(s3_uri_path, 'r').read().strip()
            download_settings(s3_uri)

    def load_settings(self, options):
        """
        Loads user settings into the global store at media_nommer.conf.settings.
        """
        # This is the value given with --config, and should be a python module
        # on their sys.path, minus the .py extension. A FQPN.
        cfg_file = options['config']

        try:
            user_settings = __import__(cfg_file)
        except ImportError:
            message = "The config module '%s' could not be found in your" \
                      "sys.path. Correct your path or specify another config " \
                      "module with the --config parameter when running the " \
                      "feederd Twisted plugin." % cfg_file
            raise NoConfigFileException(message)

        # Now that the user's settings have been imported, populate the
        # global settings object and override defaults with the user's values.
        settings.update_settings_from_module(user_settings)

    def start_tasks(self, options):
        """
        Tasks are started by importing the interval_tasks module. Only do this
        once the settings have been loaded by self.load_settings().
        """
        from media_nommer.ec2nommerd.ec2_utils import get_instance_id

        is_local = options.get('local', 0) == 1
        # if we're developing local, don't try to get an instance ID from AWS.
        get_instance_id(is_local=is_local)

        from media_nommer.ec2nommerd import interval_tasks

# Now construct an object which *provides* the relevant interfaces
# The name of this variable is irrelevant, as long as there is *some*
# name bound to a provider of IPlugin and IServiceMaker.
service_maker = WebApiServiceMaker()
