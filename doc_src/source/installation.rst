.. _installation:

.. include:: global.txt

Installation
============

Due to the early state of this project, there is a good chance that parts of
these instructions are out of date at any given time. If you run into any such
issue please let us know on our `issue tracker`_.

.. note:: 
    The following instructions are directed at what your eventual production
    environment will need. See :doc:`hacking` for details on setting up
    a development environment.

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

Installing
----------

For the sake of clarity, the media-nommer Python package on PyPi contains
the sources for :doc:`feederd` and :doc:`ec2nommerd`. You will want to install
this package on whatever machine you'd like to run :doc:`feederd` on. You do
not need to do any setup work for :doc:`ec2nommerd`, as those are ran on an
EC2_ instance that is based off of an AMI that we have created for you.

The easiest way is to install the package is through :command:`pip` or
:command:`easy_install`::

    pip install media-nommer
    
.. note::
    This will only work once we start distributing media-nommer on PyPi. For
    now, you'll need to download a tarball/zip, or check the source out from
    our `GitHub project`_ and install via the enclosed ``setup.py``. See the
    ``requirements.txt`` within the project for dependencies.
    
You will then need to visit `Amazon AWS`_ and sign up for the following
services:

* SimpleDB_
* SQS_
* EC2_

Fees are based on what you actually use, so signing up for these services will
incur no costs unless you use them.

You will then want to create a ``media_nommer`` *Security Group* through the 
AWS_ management console for your EC2_ instances to be part of. You will also
need to create an SSH key pair. Make sure to keep track of the name of your
key pair, as you will need that in the configuration stage.
    
.. _installing_configuring:
    
Configuring
-----------

Once media-nommer is installed, create a directory to store a few files in.
Within said directory, create a file called :file:`nomconf.py`. You will
want to add these settings values (at minimum):

.. code-block:: python
    
    # The AWS SSH key pair to use for creating instances. This is just the
    # name of it, as per your Account Security Credentials panel on AWS.
    EC2_KEY_NAME = 'xxxxxxxxx'
    # The AWS credentials used to access SimpleDB, SQS, and EC2.
    AWS_ACCESS_KEY_ID = 'YYYYYYYYYYYYYYYYYYYY'
    AWS_SECRET_ACCESS_KEY = 'ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ'
    
    PRESETS = {
        # A basic ffmpeg preset with no default options provided.
        'basic_ffmpeg': {
            'nommer': 'media_nommer.ec2nommerd.nommers.ffmpeg.FFmpegNommer',
            # This options dict will vary wildly depending on which
            # Nommer you are using. This example only holds true for 
            # the FFmpegNommer 
            'options': {
                # These are passed as infile options to ffmpeg
                'infile_options': {},
                # These are passed as outfile options to ffmpeg
                'outfile_options': {},
            }
        },
    }
    
See :py:mod:`media_nommer.conf.settings` for a full list of settings (and their
defaults) that you may override in your :file:`nomconf.py`.
    
Presets
-------

Presets are ways to shorten and simplify your job submission API calls. They
also make :ref:Nommers <nommers>` available via the :doc:`JSON API <jsonapi>`.

.. note:: For a :ref:`Nommer <nommers>` to be available via the 
    :doc:`JSON API <jsonapi>`, you must specify at least a 

At the very least, you'll need to add a basic preset to for each of the
:ref:Nommers <nommers>` you'd like to use. Specifying the ``options`` dict
is completely optional.

You'll want to look at the
:py:data:`PRESETS <media_nommer.conf.settings.PRESETS>` setting for more
details on how this works. The documentation for the :ref:`Nommer <nommers>`
used in each preset determines what kind of values you can pass in the
``options`` dict, so make sure you look them over as well.

.. note:: Values provided to the API at submission time always take priority
    over any directly conflicting default in a preset.

Starting feederd
----------------

You will now want to start :doc:`feederd` using whatever init script or
init daemon you use. We have had good results with Supervisor_, but you can
use whatever you're comfortable with. Make sure that the server running
:doc:`feederd` is reachable by the machines that will be sending API requests
to start encoding jobs.

Using
-----

From here, you'll want to select and start using a :ref:`client_api_libraries`.
These are what communicate with :doc:`feederd`'s RESTful web API, and ultimately
help get stuff done.