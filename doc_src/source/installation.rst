.. _installation:

.. include:: global.txt

Installation
============

Due to the early state of this project, there is a good chance that parts of
these instructions are out of date at any given time. If you run into any such
issue please let us know on our `issue tracker`_.

.. note:: 
    The following instructions are directed at what your eventual production
    environment will need. Developers setting up a dev environment can omit
    anything that they don't need (like daemonizing and process monitoring).

Assumptions
-----------
For the sake of sanity, good deployment practices, and uniformity, we're
going to make some assumptions. It is perfectly fine if you'd like to deviate,
but it will be *much* more difficult for us to help you:

* You are deploying or developing media-nommer in a virtualenv_. We highly
  recommend that and virtualenvwrapper_.
* You are running a flavor of Linux, BSD, Mac OS, or something POSIX compatible.
  While Windows support is achievable, it's not something we currently have
  the resources to maintain (any takers?).
* You have Python_ 2.5 or later. Python_ 2.6 or 2.7 is preferred. Python_ 3.x is 
  not currently supported.
* You have an `Amazon AWS`_ account, and can create or destroy S3_ buckets.

Requirements
------------

* Some flavor of Linux, Unix, BSD, Mac OS, or POSIX compliant OS.
* Python_ 2.5 or higher, Python_ 2.6 or 2.7 recommended. Python_ 3.x is not 
  supported (yet).
* Twisted_ 10.x. We develop on 10.2.
* Boto_ 2.0 or higher.

The easiest way to satisfy these is to create your virtualenv_, switch to
it, and run the following::

    pip install twisted boto