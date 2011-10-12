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
to media-nommer's web API. This is important for sending and checking on
encoding jobs. Your applications will use the API to make media-nommer do
something (other than stare at you blankly).

If you create a library of your own, let us know via the issue tracker and 
we'll add yours to the list.

* `media-nommer-api`_ (Python_)

.. _`media-nommer-api`: http://media-nommer-api-python.readthedocs.org/en/latest/

API Call Reference
------------------

All API calls are sent via **POST** with the body being JSON. Responses are
also JSON-formatted.

.. note:: You should send these calls to the host/port that your :doc:`feederd` 
    is running on. This defaults to 8001, but may specify when you call
    the :command:`twistd` command to start the daemon.

/job/submit/
^^^^^^^^^^^^

This call submits a job for encoding. Here is an example call with POST
body::


    {
        "source_path": "s3://AWS_ID:AWS_SECRET_KEY@BUCKET/KEYNAME.mp4",
        "dest_path": "s3://AWS_ID:AWS_SECRET_KEY@OTHER_BUCKET/KEYNAME.mp4",
        "notify_url": "http://myapp.somewhere.com/encoding/job_done/",
        "job_options": {
            "nommer": "media_nommer.ec2nommerd.nommers.ffmpeg.FFmpegNommer",
            "options": [
                {
                    'outfile_options': [
                        ('vcodec', 'libx264'),
                        ('preset', 'medium'),
                        ('vprofile', 'baseline'),
                        ('b', '400k'),
                        ('vf', "yadif,scale='640:trunc(ow/a/2)*2'"),
                        ('pass', '1'),
                        ('f', 'mp4'),
                        ('an', None),
                    ],
                },
                {
                    'outfile_options': [
                        ('vcodec', 'libx264'),
                        ('preset', 'medium'),
                        ('vprofile', 'baseline'),
                        ('b', '400k'),
                        ('vf', "yadif,scale='640:trunc(ow/a/2)*2'"),
                        ('pass', '2'),
                        ('acodec', 'libfaac'),
                        ('ab', '128k'),
                        ('ar', '48000'),
                        ('async', '480'),
                        ('ac', '2'),
                        ('f', 'mp4'),
                    ],
                    'move_atom_to_front': True,
                },
            ],
        },
    }
    
To further elaborate:

* ``source_path`` is a URI to the media file you'd like to encode. In this 
  example, we use an S3 URI. 
* ``dest_path`` is the full URI to where the output will end up.
* ``job_options`` is where you provide specifics as to what you'd like
  media-nommer to do. The ``nommer`` key is used to select which :ref:`nommer <nommers>`
  to use, and the ``options`` key within ``job_options`` is used to
  configure said :ref:`nommer <nommers>` (the values depend on the nommer). In
  the example above, we've selected the
  :py:class:`FFmpegNommer <media_nommer.ec2nommerd.nommers.ffmpeg.FFmpegNommer>`
  nommer, which wraps the excellent FFmpeg_. See the documentation for the
  various  :ref:`nommers` to see what ``job_options`` is used for.
* ``notify_url`` is optional, and may be omitted entirely. If specified, this
  URL is hit with a GET request when the encoding job completes.
  
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