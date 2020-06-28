"""Setup tools for tvnamer,
"""

import os
import sys


from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(args=['--tb=native'])
        sys.exit(errno)

# Ensure dir containing script is on PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tvnamer import __version__

needed_pkgs = []

needed_pkgs.append("tvdb_api>=2.0,<3")


from setuptools import setup
setup(
name = 'tvnamer',
version=".".join(str(x) for x in __version__),

author='dbr/Ben',
description='Automatic TV episode namer',
url='http://github.com/dbr/tvnamer',
license='unlicense',

long_description="""\
Automatically names downloaded/recorded TV-episodes, by parsing filenames and
retrieving show-names from www.thetvdb.com

Now deals with files containing multiple: show.name.s01e01e02.avi, anime
files: [SomeGroup] Show Name - 102 [A1B2C3].mkv and better handles files
containing unicode characters.
""",

packages = ['tvnamer'],

entry_points = {
    'console_scripts': [
        'tvnamer = tvnamer.main:main',
    ],
},

install_requires = needed_pkgs,
tests_require=['pytest'],
cmdclass = {'test': PyTest},

classifiers=[
    "Environment :: Console",
    "Intended Audience :: End Users/Desktop",
    # "License :: Unlicense",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Multimedia",
    "Topic :: Utilities",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
],
)
