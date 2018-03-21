#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine
import io
import os
import re
import sys
from codecs import open
from glob import glob
from os.path import basename
from os.path import splitext
from shutil import rmtree

from setuptools import find_packages, setup, Command


# Package meta-data.
NAME = 'em-keyboard-py3'
DESCRIPTION = 'The CLI Emoji Keyboard'
REPO_USERNAME = 'c17r'
EMAIL = 'sauerc@gmail.com'
AUTHOR = 'Christian Sauer'
URL = 'https://github.com/{0}/{1}'.format(REPO_USERNAME, NAME)

# What packages are required for this module to be executed?
REQUIRED = [
    'xerox'
]

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!
def read(f):
    return open(f, encoding='utf-8').read()

PKG_NAME = NAME.replace('-', '_')

here = os.path.abspath(os.path.dirname(__file__))

# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, 'em', '__version__.py')) as f:
    exec(f.read(), about)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    repo = None
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        self.repo = '--repository {}'.format(self.repo) if self.repo else ''
        cmd = 'twine upload {} dist/*'.format(self.repo)
        os.system(cmd)

        sys.exit()


class TestUploadCommand(UploadCommand):
    repo = 'testpypi'


# Where the magic happens:
if __name__ == '__main__':
    setup(
        name=NAME,
        version=about['__version__'],
        description=DESCRIPTION,
        long_description=read('README.rst'),
        author=AUTHOR,
        author_email=EMAIL,
        url=URL,
        packages=['em'],
        package_data={'': ['LICENSE', 'NOTICE'], 'em': ['emojis.json',]},
        entry_points = {
            'console_scripts': ['em=em:cli'],
        },
        install_requires=REQUIRED,
        include_package_data=True,
        license='ISC',
        zip_save=False,
        classifiers=[
            # Trove classifiers
            # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
            'License :: OSI Approved :: ISC License (ISCL)',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy'
        ],
        # $ setup.py publish support.
        cmdclass={
            'upload': UploadCommand,
            'test_upload': TestUploadCommand,
        },
    )
