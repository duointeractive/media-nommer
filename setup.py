import os
from distutils.core import setup
from distutils.sysconfig import get_python_lib
import media_nommer

long_description = open('README.rst').read()

TWISTED_PLUGIN_PATH = os.path.join(get_python_lib(), 'twisted', 'plugins')
TMP_BUILD_PATH = os.path.realpath(os.path.dirname(__file__))
NOMMER_PLUGIN_PATH = os.path.join(TMP_BUILD_PATH,
                                  'media_nommer', 'twisted', 'plugins')
data_files = [
    (
        TWISTED_PLUGIN_PATH,
        [os.path.join(NOMMER_PLUGIN_PATH, 'feederd.py')]
    ),
    (
        TWISTED_PLUGIN_PATH,
        [os.path.join(NOMMER_PLUGIN_PATH, 'ec2nommerd.py')]
    ),
]

setup(
    name='media-nommer',
    version=media_nommer.VERSION,
    description='A Python-based media encoding system, using Amazon AWS as its backbone.',
    long_description=long_description,
    author='DUO Interactive, LLC',
    author_email='gtaylor@duointeractive.com',
    license='BSD License',
    url='http://duointeractive.github.com/media-nommer/',
    platforms=["any"],
    # Can't use this until pip install --upgrade behavior is corrected.
    #install_requires=['boto==2.0b4', 'twisted', 'txrestapi', 'simplejson'],
    install_requires=['boto==2.0b4', 'simplejson'],
    provides=['media_nommer'],
    packages=[
        'media_nommer',
        'media_nommer.conf',
        'media_nommer.core',
        'media_nommer.ec2nommerd',
        'media_nommer.ec2nommerd.nommers',
        'media_nommer.ec2nommerd.web',
        'media_nommer.core.storage_backends',
        'media_nommer.feederd',
        'media_nommer.feederd.web',
        'media_nommer.utils'
    ],
    data_files=data_files,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Topic :: Multimedia :: Video :: Conversion',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

try:
    # This is needed to re-generate the Twisted plugin dropin.cache after install.
    from twisted.plugin import IPlugin, getPlugins
    list(getPlugins(IPlugin))
except ImportError:
    # Probably haven't installed yet. Fail silently.
    pass
