.. _introduction:

.. include:: global.txt

An Introduction to media-nommer
===============================

media-nommer is a Python project that aims to provide media encoding that
scales to your needs in the cloud (`Amazon AWS`_, to be specific). This is not
altogether special, and is a problem that has been solved by a good number of
other efforts. However, we take a unique stance in that we provide a number
of different encoding backends for different services and providers, without
your having to deal with their respective APIs directly.

Some Background
---------------

As mentioned earlier, there are any number of various projects out there that
handle encoding media on various services. We (`DUO Interactive`_) were searching 
for a suitable fit for two different projects that needed near-infinite media
encoding scalability. However, the two projects were completely different in 
the way that the media files would be delivered and tracked, as well as the
formats to be encoded to. Furthermore, there were/are certain formats that some 
services like Encoding.com handle much better/cheaper than our ideal of
EC2_ + FFmpeg_.

We needed a package that would let us send media directly to our encoding
software, or grab it from S3 for encoding. Encoded output would need to be 
stored on S3 for distribution via CloudFront_. We also wanted to go the
cheapest route, which sometimes meant using a more specialized third party
service. We wanted to be able to selectively pipe certain media out to said
third parties, and send the rest to our default EC2_ + FFmpeg_ encoding
plugin. And most importantly of all, we wanted the bulk of the setup work
for a deployment of the software to be done in the config file, with the
nasty stuff humming along out of sight.

The result of all of this was the creation of media-nommer, a Python_-based
media encoding system with a penchant for scalability and flexibility.

A high level overview
---------------------

Intelligent distributed encoding requires a director or orchestrator to keep
everything running as it should. Since we've targeted near-infinite scalability
as a goal, we need to be able to hand out media to external services, as well
as scale our own EC2_ + FFmpeg_ instances up and down to meet demand. This is
where the :py:obj:`nommerd <media_nommer.nommerd>` daemon comes in.

The nommerd manages the various *Nommers*, which are classes that manage the
encoding service they abstract. For example, we have an EC2FFmpegNommer,
as well as an EncodingDotComNommer. Each of these has methods that lets nommerd
submit encoding jobs, receive notification of their success/failure, and
deal with the output.

nommerd also implements a simple JSON-based API for your custom software to
query for pending or current encoding job states. 

And finally, upon completion of an encoding job, you may optionally have
nommerd ping you back at a specified URL.

That's a lot of nommerd
-----------------------

You'll notice that we mention nommerd pretty frequently. We could have done
without this guy if we went with a de-centralized EC2_ + FFmpeg_ setup, but
then we lose a lot of ability to blend Amazon AWS-based encoding with
external encoding.
  