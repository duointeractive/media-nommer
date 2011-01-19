.. _jsonapi:

.. include:: global.txt

Using feederd's JSON API
========================

One of :doc:`feederd`'s roles is hosting a web-based JSON API for your
custom applications to communicate through. With this API, you may do such
things as:

* Schedule encoding jobs
* Check the state of existing encoding jobs (To be implemented)

By using a simple web-based API, you are free to either use one of the existing
client API libraries, or write your own.

.. _client_api_libraries: 

Client API Libraries
--------------------

The following API client libraries are for forming and sending JSON queries
to media-nommer's RESTful API. This is important for sending and checking on
encoding jobs. Your applications will use the API to make media-nommer do
something (other than stare at you blankly).

If you create a library of your own, let us know via the issue tracker and 
we'll add yours to the list.

* `media-nommer-api`_ (Python_)

.. _`media-nommer-api`: https://github.com/duointeractive/media-nommer-api-python

API Call Reference
------------------

We will go on to document the various API calls and their arguments here.