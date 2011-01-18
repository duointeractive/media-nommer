.. _introduction:

.. include:: global.txt

An Introduction to media-nommer
===============================

media-nommer is a Python_-based, distributed media encoding system. It aims to
implement much of the same services offered by commercial encoding services.
The primary advantage afforded by media-nommer is that one only pays for what
they use on `Amazon AWS`_, with no additional price mark-up. It may also be
completely customized to meet your needs.

Some Background
---------------

There are any number of encoding services around the web, some of which are
cheap and very easy to use. We (`DUO Interactive`_) were searching 
for a suitable fit for two different projects that an extreme amount of
encoding scalability. However, the more we looked into it, the more we
struggled with picking a service that had a good balance of affordability and
permanence. We also were looking for a little more customizability in the
encoding process.

Many encoding services use software such as FFmpeg_, and encode media to codecs
that they have not paid licensing fees for. If the service has any
degree of success, it is only a matter of time before MPEG-LA and others come
knocking to get their licensing fees. This often spells end-of-game for the
smaller (often cheaper) services. On the other end of the spectrum, some
100% legal services have to raise their prices up to cover the large licensing
fees, putting it outside the realm of what we'd like to pay. A good read on
this subject can be found on the `FFmpeg legal`_ page.

For those of us who don't need to encode to royalty-encumbered formats, a
cheaper, more customizable, and more permanent solution was to just write our
own. The result of all of this was the creation of media-nommer, a 
Python_-based media encoding system with scalability and flexibility in mind.

.. _`FFmpeg legal`: http://ffmpeg.org/legal.html

A high level overview
---------------------

media-nommer is comprised of two primary componenets, :doc:`feederd` and
:doc:`ec2nommerd`.

feederd
^^^^^^^

Distributed encoding requires a director or orchestrator to keep
everything running as it should. This is where the :doc:`feederd` daemon 
comes into play. Here are some of the things it does:

* Manages your EC2_ instances (which have the :doc:`ec2nommerd` daemon
  running on them), and intelligently spins up more instances 
  according to your configuration and work load.
* Keeps track of the status of your encoding jobs, present and past.
* Exposes a simple JSON-based API that can be used to schedule jobs, and
  check on the status of those that are currently running or completed.
  
:doc:`feederd` may be ran on your current infrastructure, or on EC2_. Your
EC2_ nodes are never in direct contact with :doc:`feederd`, and instead
communicate through `Amazon AWS`_.

ec2nommerd
^^^^^^^^^^
  
Where :doc:`feederd` is the manager, :doc:`ec2nommerd` is the worker. Your
basic unit of work is an EC2_ instance that runs :doc:`ec2nommerd`. This
daemon simple checks a SQS_ queue for jobs that need to be encoded, and does
so until the queue is empty. After a period of inactivity, your EC2_ instances
will terminate themselves, saving you money.
