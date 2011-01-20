.. _ec2nommerd:

.. include:: global.txt

==========
ec2nommerd
==========

If :doc:`feederd` is the manager, ``ec2nommerd`` is the worker. You can also
think of the relationship in that :doc:`feederd` feeds your nommers.

What is ec2nommerd
------------------

``ec2nommerd`` is a Twisted_ plugin that runs as a daemon on EC2_ instances
in the cloud. These instances are automatically created by :doc:`feederd`.
If an ``ec2nommerd`` finds itself with available encoding capacity, it will
hit an Amazon SQS_ queue to see if there is any work available. If it finds
anything, it pulls the job details from SimpleDB_ and hands the job off to
the appropriate :ref:`nommer <nommers>` for encoding.

If, after a period of time, the daemon receives no work to be done, it can
be configured to terminate itself to save money.

.. _nommers:

Nommers
-------

Nommers are classes that contain all of the logic specific to different kinds
of encoding workflows. For example, the 
:py:mod:`FFmpegNommer <media_nommer.ec2nommerd.nommers.ffmpeg.FFmpegNommer>`
nommer wraps the FFmpeg_ command for encoding. Each nommer sub-classes
the
:py:mod:`BaseNommer <media_nommer.ec2nommerd.nommers.base_nommer.BaseNommer>`
class, which provides some foundational methods. View the source for these
two classes for examples on how they work. You may sub-class or create your
own nommer, adding it to at least one preset in your 
:py:data:`PRESETS <media_nommer.conf.settings.PRESETS>` setting.

The following Nommer classes are currently included with media-nommer. See
each for details on how the ``job_options`` key should look like in your
:py:data:`PRESETS <media_nommer.conf.settings.PRESETS>` setting in 
your ``nomconf.py``:

* :py:mod:`media_nommer.ec2nommerd.nommers.ffmpeg.FFmpegNommer`