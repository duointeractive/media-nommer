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

For the sake of clarity, the media-nommer Python package contains
the sources for :doc:`feederd` and :doc:`ec2nommerd`. You will want to install
this package on whatever machine you'd like to run :doc:`feederd` on. You do
not need to do any setup work for :doc:`ec2nommerd`, as those are ran on an
EC2_ instance that is based off of an AMI that we have created for you.

Since we are not yet distributing media-nommer on PyPi, the easiest way is to 
install the package is through :command:`pip`::

    pip install txrestapi twisted
    pip install --upgrade git+http://github.com/duointeractive/media-nommer.git#egg=media_nommer
    
.. note::
    If you don't have access to :command:`pip`, you may download a tarball/zip, 
    from our `GitHub project`_ and install via the enclosed ``setup.py``. See 
    the ``requirements.txt`` within the project for dependencies.

We have to install Twisted before media-nommer because of an odd behavior
with :command:`pip`. 

.. tip:: Any time that you upgrade or re-install Twisted, you must also 
    re-install media-nommer.

Signing up for AWS
------------------

After you have installed the media-nommer Python package on your machine(s),
you'll need to visit `Amazon AWS`_ and sign up for the following services:

* SimpleDB_
* SQS_
* EC2_

It is important to understand that even if you already have an Amazon account,
you need to sign up to each of these services specifically for your account to
have access to said services. This is a very quick process, and typically
involves looking over an agreement and accepting it.

.. tip:: Signing up for these services is outside the scope of this document. 
    Please contact AWS_ support with questions regarding this step. Their
    community forums are also a great resource.

Fees are based on what you actually use, so signing up for these services will
incur no costs unless you use them. 

You will need to create a ``media_nommer`` EC2 *Security Group* through the 
AWS_ management console for your EC2_ instances to be part of. 

.. warning:: Failure to create an EC2 security group will result in
    media-nommer not being able to spawn EC2 instances, which means
    no encoding for you.

You will also need to create an SSH key pair. Make sure to keep track of the 
name of your key pair, as you will need this in the configuration stage.
    
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
    # The S3 bucket to store a copy of ``nomconf.py`` for nommer instances.
    # NOTE: CREATE A BUCKET AND CHANGE THIS VALUE BEFORE YOU START!
    CONFIG_S3_BUCKET = 'change-this-value'
    # The AWS security groups to create EC2 instances under. They don't need
    # any rules set.
    EC2_SECURITY_GROUPS = ['media_nommer']
    # The name of the SQS queue for job notifications. This will be created
    # if needed, just pick a unique name.
    
See :py:mod:`media_nommer.conf.settings` for a full list of settings (and their
defaults) that you may override in your :file:`nomconf.py`.
    
Starting feederd
----------------

You will now want to start :doc:`feederd` using whatever init script or
init daemon you use. We have had good results with Supervisor_, but you can
use whatever you're comfortable with. Make sure that the server running
:doc:`feederd` is reachable by the machines that will be sending API requests
to start encoding jobs. Here is an example command string, assuming you're in
your top-level :file:`media-nommer` directory (not :file:`media_nommer`)::

    PYTHONPATH=media_nommer twistd -n --pidfile=feederd.pid feederd

Using
-----

From here, you'll want to select and start using a :ref:`client_api_libraries`.
These are what communicate with :doc:`feederd`'s RESTful web API, and ultimately
help get stuff done.