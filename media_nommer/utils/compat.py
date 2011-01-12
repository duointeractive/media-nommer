"""
Python compatibility stuff and backports.
"""

def total_seconds(td):
    """
    Given a timedelta object, compute the total number of seconds elapsed
    for the entire delta. This is only available in the standard library for
    Python 2.7 and up.
    
    Source: http://docs.python.org/library/datetime.html#datetime.timedelta.total_seconds
    
    :param datetime.timedelta td: A timedelta instance.
    :rtype: float
    :returns: The seconds elapsed during the timedelta.
    """
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6) / 10 ** 6.0
