.. _jsonapi:

.. include:: global.txt

Using feederd's JSON API
========================

One of :doc:`feederd`'s roles is hosting a web-based JSON API for your
custom applications to communicate through. With this API, you may do such
things as:

* Schedule encoding jobs
* Check the state of existing encoding jobs (To be implemented)

By using a simple web-based API, you are free to either use one of the existing
client API libraries, or write your own.

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

.. _`media-nommer-api`: http://duointeractive.github.com/media-nommer-api-python/

API Call Reference
------------------

All API calls are sent via **POST**, and have keys that may either be straight
string values or JSON. Responses are also JSON-formatted.

.. note:: You should send these calls to the host/port that your :doc:`feederd` 
    is running on. This defaults to 8001, but may specify when you call the
    :command:`twistd` command to start the daemon.

/job/submit/
^^^^^^^^^^^^

This call submits a job for encoding. Here is an example call with POST
keys and their values::

    source_path = s3://AWS_ID:AWS_SECRET_KEY@BUCKET/KEYNAME.mp4
    dest_path = s3://AWS_ID:AWS_SECRET_KEY@OTHER_BUCKET/KEYNAME.mp4
    preset = movie_high_q
    notify_url = http://myapp.somewhere.com/encoding/job_done/
    job_options = {
        "infile_options": {"r": 24},
        "outfile_options": {"sameq": null, "target": "vcd"}
    }
    
To further elaborate:

* ``source_path`` is a URI to the media file you'd like to encode. In this 
  example, we use an S3 URI. 
* ``dest_path`` is the full URI to where the output will end up.
* ``preset`` corresponds to a preset specified in your ``nomconf.py``
  configuration file. See the 
  :py:data:`PRESETS <media_nommer.conf.settings.PRESETS>` setting for more
  details. These are mandatory, and can optionally be used to specify default
  encoding settings for a certain kind of encoding job. You also specify
  which :ref:`nommer <nommers>` to use here.
* ``notify_url`` is optional, and may be omitted entirely. If specified, this
  URL is hit with a GET request when the encoding job completes.
* ``job_options`` is an optional key that contains a JSON-serialized dict, and 
  may be omitted as well. The contents of this depends on the 
  :ref:`nommer <nommers2>` selected in your ``preset``.
  See your ``nomconf.py`` if you need a refresher as to which preset uses which
  nommer. For this example, we show 
  :py:class:`FFmpegNommer <media_nommer.ec2nommerd.nommers.ffmpeg.FFmpegNommer>`,
  which wraps the excellent FFmpeg_. See the documentation for the various 
  :ref:`nommers` to see what ``job_options`` is used for. In cases where values 
  specified in your API request's ``job_options`` conflict with the ``options``
  in your preset, the value from the API request is used.
  
The response to your request is also JSON-formatted, and looks like this::

    {
        "success": true, 
        "job_id": "1f40fc92da241694750979ee6cf582f2d5d7d28e1833"
    }
    
If an error is encountered, ``success`` will be ``false``, additional
``message`` and ``error_code`` keys will be set::

    {
        "false": true, 
        "error_code": "BADINPUT", 
        "message": "Bad input file. Unable to encode."
    }