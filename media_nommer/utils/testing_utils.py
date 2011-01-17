"""
This module contains some helpful utilities used in the testing process.
"""
import os

try:
    AWS_ACCESS_KEY_ID = os.environ['MNOM_TEST_AWS_ACCESS_KEY_ID']
except KeyError:
    raise Exception("No MNOM_TEST_AWS_ACCESS_KEY_ID environment variable found. Please set it and try again.")

try:
    AWS_SECRET_ACCESS_KEY = os.environ['MNOM_TEST_AWS_SECRET_ACCESS_KEY']
except KeyError:
    raise Exception("No MNOM_TEST_AWS_SECRET_ACCESS_KEY environment variable found. Please set it and try again.")
