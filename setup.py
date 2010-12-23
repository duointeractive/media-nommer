from distutils.core import setup
import media_nommer

long_description = open('README.rst').read()

setup(
    name='media-nommer',
    version=media_nommer.VERSION,
    packages=['media_nommer'],
    description='A Python-based media encoding system, using Amazon AWS as its backbone.',
    long_description=long_description,
    author='DUO Interactive, LLC',
    author_email='gtaylor@duointeractive.com',
    license='BSD License',
    url='http://duointeractive.github.com/media-nommer/',
    platforms=["any"],
    requires=['boto', 'twisted'],
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
