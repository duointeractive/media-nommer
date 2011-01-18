.. _index:

.. include:: global.txt

=================================================
media-nommer: A Python-based media encoder system
=================================================

media-nommer is an encoding system that is able to utilize a number of
different encoding methods and services via the aptly named Nommer system.
The software is powered by a combination of Python_, Twisted_, and Boto_.

For example, if you wanted to do all of your encoding on your own with EC2_
and FFmpeg_, you'd use the EC2FFmpegNommer to encode your media files. Or perhaps
you want to encode your smaller media with FFmpeg_, but ship some of your
larger files off to encoding.com, you could use the up-coming 
EncodingDotComNommer in addition to the aforementioned EC2FFmpegNommer to
create a mixed workflow.

Regardless of how you nom your media, this Python_ module will abstract away
the boring stuff, leaving you to create your media for the masses to consume
(nom?).

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
   
Reference
---------

.. toctree::
   :maxdepth: 1

   apiref/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

