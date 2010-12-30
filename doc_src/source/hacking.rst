.. _hacking:

.. include:: global.txt

Hacking on media-nommer
=======================

For those that are particularly ambitious, or generous enough to want to
contribute to the project, the barrier to entry is reasonably low. We will go
over a few topics at a high level to get you started.

Obtaining the source
--------------------

The best way to obtain the source is through our git_ repository on GitHub_.
If you are going to do anything aside from poke at the code, I would *highly*
recommend visiting our `GitHub project`_ and forking the project via the
**Fork** button. 

For those not familiar with GitHub_, this will create a copy
of the repository under your username which you have commit access to. From
your repository, you can make modifications and send *Pull Requests* to the
upstream project asking for your changes to be merged in. Meanwhile, you can
keep your fork up to date with changes from upstream. This is a whole lot
faster, easier, and more fun than the traditional patch juggling method.

If you'd like to skip the whole *forking* ordeal and just get a copy of our
upstream repository on your machine, you'll probably want to do something like::

    git clone https://github.com/duointeractive/media-nommer.git
    
This will leave you with a `media-nommer` directory in your current directory.

.. tip::
    For those that aren't familiar with git_ and/or GitHub_, see the
    excellent `GitHub help`_ with lots of helpful how-tos.
    
.. _GitHub help: http://help.github.com/

Installing additional dependencies
----------------------------------

There are a few additional dependencies to install when doing development
work. Since everyone is being good little programmers and working under
virtualenv_, it's just a matter of switching to said virtual environment and
doing::

    pip install nose sphinx
    
Now you're set to run unit tests and build our documentation.

Running and writing unit tests
------------------------------

Running unit tests is trivial with nose_. `cd` to your media-nommer directory
and just run::

    nose
    
The cool thing about nose_ is that it will find anything that looks like a
unit test throughout the entire codebase, without us having to tell it where
to look.

As far as writing unit tests, we'd like to shoot for full coverage, so please
do write tests for your changes. If you are working on something new,
find the `tests.py` module neighboring the one you're working on (or create
one if it doesn't already exist) and write your unit tests using the standard
Python unittest_ module. If you need any examples of how our unit tests look,
run this to find all of our `tests.py` modules from your root `media-nommer`
directory::

    find . -name tests.py
    
Look through these for a good idea of what we're looking for.

.. _unittest: http://docs.python.org/library/unittest.html

.. warning::
    We are very unlikely to accept code contributions without unit tests. It
    is understood that writing unit tests is boring, tedious, and un-fun, but
    it is a necessary evil for complex software.
    
Code style
----------

We mostly adhere to PEP8_, and expect contributors to do the same. A few quick
hi-lights:

* 80 columns width max, unless absolutely necessary.
* Indents are 4 spaces, and not tabs. **No tabs allowed**.
* Avoid wildcard * imports unless absolutely necessary.
* No camelCase method names, use underscores and lowercase letters. 
* Classes use CapWords.
* Global variables are ALL_UPPER_CASE.
* Comments and docstrings for just about everything. Even if you think it's 
  obvious. It probably won't be a few weeks/months/years later.

.. _PEP8: http://www.python.org/dev/peps/pep-0008/

Contributing code
-----------------

After you have made modifications in your GitHub_ fork, you need only send
a *Pull Request* to us via the aptly named **Pull Request** on your fork's
project page. See `GitHub's guide to forking`_. It's quick and easy, we
promise.

"I'm stumped, help!"
--------------------

The best way to get help right now is to submit an issue on the `issue tracker`_.
This is useful for questions, suggestions, and bugs.

Contributions are BSD-licensed
------------------------------

Important to note is the fact that all contributions to the media-nommer
project are, like the project itself, BSD-licensed. Please make sure you or
your employer are OK with this before contributing.

.. _GitHub's guide to forking: http://help.github.com/forking/