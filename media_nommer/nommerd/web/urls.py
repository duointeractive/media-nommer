# -*- coding: utf-8 -*-
"""
This module assembles the various API sub-modules into URL paths. These become
the JSON API that external software can POST to for various things.
"""
import cgi
from twisted.web.resource import Resource

"""
URL assembly.
"""
URL_ROOT = Resource()


