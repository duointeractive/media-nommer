"""
The feederd module contains Twisted daemon that monitors queues, creates
EC2 instances, schedules encoding jobs, handles response pings from
external encoding services, and notifies your external applications when
encoding has completed.

.. note:: 
    Only more general management logic should live in this module. Anything
    specific like encoding commands or EC2 management should live elsewhere.
    feederd is just the orchestrator.
"""
