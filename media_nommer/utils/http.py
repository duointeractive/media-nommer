"""
Some assorted HTTP-related utilities, mainly for Twisted.
"""

from zope.interface import implements

from twisted.internet.defer import succeed
from twisted.web.iweb import IBodyProducer

class StringProducer(object):
    """
    This is useful for twisted.web.client.Agent, which must use a producer
    to spoon feed the request over a period of time, instead of one big chunk.

    Check the Twisted documentation for an example of how this fits together::

        http://twistedmatrix.com/documents/current/web/howto/client.html
    """
    implements(IBodyProducer)

    def __init__(self, body):
        """
        :param str body: The body to be sent to the remote server.
        """
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass