"""Setup tools for tvnamer,
"""

needed_pkgs = []

try:
    import json
except ImportError:
    needed_pkgs.append('simplejson')

needed_pkgs.append("tvdb_api>=1.5")


from setuptools import setup
setup(
name = 'tvnamer',
version='2.2',

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

classifiers=[
    "Environment :: Console",
    "Intended Audience :: End Users/Desktop",
    # "License :: Unlicense",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Multimedia",
    "Topic :: Utilities",
],
)
