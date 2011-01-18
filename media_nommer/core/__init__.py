"""
The core module is home to code that is important to both the
:py:mod:`media_nommer.ec2nommerd` and :py:mod:`media_nommer.feederd` top-level
modules. This is best thought of as a lower level API that all of the pieces
of the encoding system use to communicate and interact with one another.

.. note:: 
    There should be nothing that is specific to just :doc:`../ec2nommerd`
    or just :doc:`../feederd` here if at all possible.
"""
