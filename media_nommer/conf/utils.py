"""
Various configuration-related utility methods.
"""
import boto
from media_nommer.conf import settings
from media_nommer.core.storage_backends.s3 import S3Backend

def upload_settings(nomconf_module):
    """
    Given a user-defined nomconf module (already imported), push said file
    to the S3 conf bucket, as defined by settings.CONFIG_S3_BUCKET. 
    This is used by the nommers that require access to the config, like 
    EC2FFmpegNommer.
    """
    nomconf_py_path = nomconf_module.__file__[:-1]
    conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID,
                           settings.AWS_SECRET_ACCESS_KEY)
    bucket = conn.create_bucket(settings.CONFIG_S3_BUCKET)
    key = bucket.new_key('nomconf.py')
    key.set_contents_from_filename(nomconf_py_path)

def download_settings(nomconf_uri):
    """
    Given the URI to a S3 location with a valid nomconf.py, download it.
    This is used on the media-nommer EC2 AMIs.
    """
    fobj = open('nomconf.py', 'w')
    S3Backend.download_file(nomconf_uri, fobj)
