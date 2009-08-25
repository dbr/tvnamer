"""Setup tools for tvnamer,
"""

from setuptools import setup
setup(
name = 'tvnamer',
version='1.2',

author='dbr/Ben',
description='Automatic TV episode namer',
url='http://github.com/dbr/tvdb_api/tree/master',
license='GPLv2',

long_description="""\
Automatically names downloaded/recorded TV-episodes, by parsing filenames and
retrieving show-names from www.thetvdb.com

Now deals with files containing multiple: show.name.s01e01e02.avi, anime
files: [SomeGroup] Show Name - 102 [A1B2C3].mkv and better handles files
containing unicode characters.
""",

py_modules = ['tvnamer'],
entry_points = {
    'console_scripts': [
        'tvnamer = tvnamer.main:main',
    ],
},

install_requires = ['tvdb_api>=1.1'],

classifiers=[
    "Environment :: Console",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Multimedia",
    "Topic :: Utilities",
],
)
