.. _feederd:

.. include:: global.txt

=======
feederd
=======

Distributed encoding is a complex task, with lots of moving parts and
components. To create, monitor, and "motivate" our EC2_ encoding instances
during the process, we have ``feederd``.

What is feederd
---------------

``feederd`` is a Twisted_ plugin that runs as a daemon on the machine of your
choice. This can be on your own bare metal server, or on an EC2_ instance.
The daemon keeps track of encoding jobs through Amazon SimpleDB_, tells
your EC2_ encoder instances to get to work via Amazon SQS_, and exposes a 
lightweight JSON web API for your own custom applications to schedule and
manage jobs through.

Relationship with ec2nommerd
----------------------------

If ``feederd`` is the brains of the operation, :doc:`ec2nommerd` is the
brawn. ``feederd`` simply saves job state data to SimpleDB_ and creates
SQS_ queue entries to let your EC2_ instances know that there's work to 
be done. Each of your EC2_ instances run an :doc:`ec2nommerd` daemon, which
pulls jobs from the queue (or terminates the instance if there isn't any
work to be done).

Intelligent scaling
-------------------

Along with providing an entry point to start, manage, and track the encoding
process, ``feederd`` also handles scaling your encoding cloud up as needed.
Based on your configuration, ``feederd`` will look at the current list of
jobs that need to be encoded in comparison to the number of encoding instances
you currently have running on EC2_. It will then decide whether it should
spawn additional instances to handle the load.

EC2_ instances are spawned from a public AMI that we maintain as part of the
project. If you wish to create your own custom AMI, you may easily specify
your own or clone and modify ours.

Automated scaling is an optional feature, and can be configured and 
restricted in a number of different ways. For example, perhaps you don't want
any more than one or two EC2_ instances running at any given time.

Architectural notes
-------------------

One of the requirements for media-nommer was that at no time would ``feederd``
and one of its :doc:`ec2nommerd` instances communicate directly. As noted
earlier, job state information is saved and retrieved from SimpleDB_ by
both ``feederd`` and :doc:`ec2nommerd` instances. SQS_ is used to delegate
work to the :doc:`ec2nommerd` instances. This does a few things for us:

* We don't have to open a hole in our firewall in your data center or in your
  EC2 encoder nodes.
* If ``feederd`` or the server that hosts it goes down, your :doc:`ec2nommerd` 
  instances will continue encoding until the last job is popped off the queue.
  After that, they may be configured to terminate themselves after a period
  of inactivity (to save you money).
  
There is a lot of code that ``feederd`` and :doc:`ec2nommerd` shares, which can
all be found in the :py:mod:`media_nommer.core` module. This is best thought
of as a lower level API that these two components use to save and retrieve
job state information.

Source for ``feederd`` can be found in the :py:mod:`media_nommer.feederd`
module.