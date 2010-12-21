# -*- coding: utf-8 -*-
"""
This module assembles the various API sub-modules into URL paths. These become
the JSON API that external software can POST to for various things.
"""
import cgi
from twisted.web.resource import Resource

class FormPage(Resource):
    """
    This is just an example, we'll move Resource objects into their own
    sub-modules later.
    """
    def render_GET(self, request):
        return '<html><body><form method="POST"><input name="the-field" type="text" /></form></body></html>'

    def render_POST(self, request):
        return '<html><body>You submitted: %s</body></html>' % (cgi.escape(request.args["the-field"][0]),)

class SubUrlPage(Resource):
    """
    This is a page beneath FormPage in the URL structure.
    """
    def render_GET(self, request):
        return '<html><body>Hooray</body></html>'

"""
URL assembly.
"""
URL_ROOT = Resource()

fpage = FormPage()
fpage.putChild("test", SubUrlPage())

URL_ROOT.putChild("form", fpage)
