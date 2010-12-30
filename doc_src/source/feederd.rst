.. _feederd:

.. include:: global.txt

=======
feederd
=======

`feederd` is a Twisted_ daemon that orchestrates encoding workflows that involve
monitoring a filesystem, FTP, S3, or other protocols for new files needing
encoding. It does no encoding itself, but watches for incoming media, and uses
our underlying nommer API to launch the encoding jobs.

.. tip::
    Usage of `feederd` is entirely optional. It is an easy way to get
    drag-and-drop encoding going, but you may also use the underlying APIs
    directly in your own applications.

Installation
============

If you followed the :doc:`installation` instructions for media-nommer, you
already have all of the needed dependencies installed. You now need to get
your `feederd` daemon up and running.

nomconf.py
----------

The biggest trouble spot in setup and installation follows, so pay special
attention to this part. `feederd` looks for a configuration file for its
settings. **This file must be in your Python path**. Please take a moment
to consider how this will fit into your choice of init system.

We'll go into more detail in the next section about how the startup process
works, but for now, you need to know that you should do something like this
to create a Python module with a  :file:`nomconf.py` file in it::

    cd <LOCATION OF YOUR CHOICE>
    mkdir media_nom
    cd media_nom
    touch __init__.py nomconf.py
    
.. tip:: 
    You don't want to create a directory called :file:`media_nommer`, as this 
    would clash with media-nommer package name (media_nommer). We suggest 
    using the :file:`media_nom` example above.
    
This should leave you with a valid Python package beneath the directory of
your choice. Make sure to note the full path of this package using the
:command:`pwd` command. It will be important for starting the daemon.

Next, open up :file:`nomconf.py` in the editor of your choice, and copy/paste
the following:

.. code-block:: python

    # The following AWS credentials are used for accessing SQS and SimpleDB.
    # For media source and destinations, other S3 accounts may be used.
    AWS_ACCESS_KEY_ID = 'XXXXXXXXXXXXXXXXXXXX'
    AWS_SECRET_ACCESS_KEY = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'

    # The SQS queue to use for storing encoding state info.
    SQS_QUEUE_NAME = 'media_nommer'
    
    # The SimpleDB domain name for storing encoding job state in.
    SIMPLEDB_DOMAIN_NAME = 'media_nommer'

    # Example configuration for a basic EC2+FFmpeg workflow.
    BASIC_S3_WORKFLOW = {
        # FQPN for the Nommer class.
        'NOMMER': 'media_nommer.nommers.ec2_ffmpeg.EC2FFmpegNommer',
        # Unique identifier for this workflow.
        'NAME': 'basic_s3_workflow',
        # A description for some UI elements and commands.
        'DESCRIPTION': 'An example workflow',
        # The S3 bucket to monitor for incoming media files to encode.
        'MEDIA_SOURCE': 's3://YOUR_AWS_KEY_ID:YOUR_AWS_SECRET_KEY@nommer_in',
        # The bucket to place encoded files in.
        'MEDIA_DESTINATION': 's3://YOUR_AWS_KEY_ID:YOUR_AWS_SECRET_KEY@nommer_out',
    }

    # A tuple with all of your workflow dicts in it. One feederd process can
    # manage multiple workflows at the same time.
    WORKFLOWS = (
        BASIC_S3_WORKFLOW,
    )

See the :ref:`feederd-settings` section for a full run-down of all possible 
settings.

.. tip:: 
    This :file:`nomcomf.py` file can be imported and used if you're going
    to write anything that uses any of the APIs in media-nommer directly.

Starting the daemon
-------------------

Since `feederd` is just a Twisted_ plugin, we run it via the :command:`twistd`
command. Before you begin, take a moment to review some of the possible
options::

    twistd --help
    
You'll see that there are a number of options that allow you to set logging,
uid/gid, and daemonization settings. Everything shown in this help display is
part of Twisted_, no media-nommer.

The next step is to review the options presented by our `feederd` Twisted_
plugin::

    twistd feederd --help
    
Notice that we have a `--config` option. This defaults to the `nomconf` module
we created earlier, but can be anything you'd like. Note that this is in
Python module name format, so don't include the '`.py`' extension if you're
going to over-ride the default.

Now for the fun part, let's start up `feederd`::

    twistd -n feederd

The `-n` flag starts `feederd` in 'nodaemon' mode, which means you can stop
it using :kbd:`Control-c` or :kbd:`Control-d` instead of having to
:command:`kill` it. This is useful for testing, and some init systems like
Supervisor_.

If you weren't greeted with a successful startup, you are most likely running
into the Python path issues we hinted at earlier. If you start the daemon
from within the directory that :file:`nomconf.py` resides in, you should see
a successful startup. If you need to be able to start the daemon from another
directory that puts our our previously created :file:`media_nom` module outside
of our Python path, we can add it explicitly:: 
    
    PYTHONPATH=/home/youruser/media_nom twistd -n feederd
    
Some init systems, such as Supervisor_, have facilities that allow you to change
current working directories, which will have the same affect.

.. _feederd-settings:

Settings
========

The following directives may be included in your :file:`nomconf.py` (or
whatever custom name you chose).

AWS_ACCESS_KEY_ID
-----------------

The AWS id for the account that will queue encoding jobs in SimpleDB_, and
track job state in SimpleDB_.

AWS_SECRET_ACCESS_KEY
---------------------

The AWS key for the account that will queue encoding jobs in SimpleDB_, and
track job state in SimpleDB_.

SQS_QUEUE_NAME
--------------

The SQS_ queue used to schedule encoding jobs with.

SIMPLEDB_DOMAIN_NAME
--------------------

The SimpleDB_ domain name for storing encoding job state in.

WORKFLOWS
---------

Default: ``()`` (Empty tuple)

A tuple of workflow dictionaries. Each dict represents one media encoding
workflow. A single `feederd` daemon can service multiple workflows, at the
cost of potentially longer delays in some operations.

.. code-block:: python
    
    WORKFLOWS = (
        {
            'NOMMER': 'media_nommer.nommers.ec2_ffmpeg.EC2FFmpegNommer',
            'NAME': 'basic_s3_workflow',
            'MEDIA_SOURCE': 's3://YOUR_AWS_KEY_ID:YOUR_AWS_SECRET_KEY@nommer_in',
            'MEDIA_DESTINATION': 's3://YOUR_AWS_KEY_ID:YOUR_AWS_SECRET_KEY@nommer_out',
        },
    )

All of the workflow settings are documented below.

NOMMER
~~~~~~

FQPN of the Nommer class. The current choices are:

* ``'media_nommer.nommers.ec2_ffmpeg.EC2FFmpegNommer'``

Each of these handles encoding differently, sometimes drastically so.

NAME
~~~~

Unique identifier for this workflow. This is used for identification in
log files, and querying of jobs in SimpleDB_ and SQS_.

.. _feederd-settings-media_source:

MEDIA_SOURCE
~~~~~~~~~~~~

For workflows that monitor a location somewhere for files to encode, this is
the URI of said location to monitor. Here are some example values:

* ``'s3://AWS_KEY_ID:AWS_SECRET_KEY@nommer_in'``
* ``'ftp://someuser@somehost:/some/loc'`` *(Not implemented yet)*
* ``'file://path/to/some/dir'`` *(Not implemented yet)*

MEDIA_DESTINATION
~~~~~~~~~~~~~~~~~

The final location for encoded media (along with the master file from which
the encodings were made) should end up. This follows the same format as
:ref:`feederd-settings-media_source`.