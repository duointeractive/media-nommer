.. _index:

.. include:: global.txt

=================================================
media-nommer: A Python-based media encoder system
=================================================

media-nommer is a distributed media encoding system that gets its horsepower
from `Amazon AWS`_. This leaves you with a cheaper, more reliable alternative
to some commercial paid encoding systems, since you are only paying for your
`Amazon AWS`_ usage. The software is powered by a combination of Python_, 
Twisted_, and Boto_, and is licensed under the flexible `BSD License`_.

This may be useful to you if...
-------------------------------

media-nommer is of interest to you if you need a way to encode media in a 
cheap, fast, and scalable manner. By using `Amazon AWS`_'s excellent EC2_
service, you can automatically scale your number of encoder instances up to
meet your demands. Of course, the entire process may be configured, limited,
and adapted to meet your needs.

Learning more
-------------

To learn more about media-nommer, see the :doc:`introduction`.

**Project Status:** Early development

**License:** media-nommer is licensed under the `BSD License`_.

Useful Links
------------

* Source repository: https://github.com/duointeractive/media-nommer
* Issue tracker: https://github.com/duointeractive/media-nommer/issues

Documentation
-------------

.. toctree::
   :maxdepth: 2
   
   introduction
   installation
   feederd
   ec2nommerd
   hacking
   apiref/index
   
   
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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

