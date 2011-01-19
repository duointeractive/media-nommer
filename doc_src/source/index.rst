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

This may be useful if...
------------------------

media-nommer is of interest to you if you need a way to encode media in a 
cheap, fast, and scalable manner. By using `Amazon AWS`_'s excellent EC2_
service, you can automatically scale your number of encoder instances up to
meet your demands. Of course, the entire process may be configured, limited,
and adapted to meet your needs. Some example usage cases where media-nommer
might be a good fit:

* Encoding user-uploaded media for serving from your site
* Bulk encoding large collections of videos

Learning more
-------------

To learn more about media-nommer, see the :doc:`introduction`.

**Project Status:** Early development

**License:** media-nommer is licensed under the `BSD License`_.

These links may also be useful to you.

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
   jsonapi

Development docs
----------------

The following topics will be useful to you if you would like to help improve
media-nommer.

.. toctree::
   :maxdepth: 2

   hacking
   apiref/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

