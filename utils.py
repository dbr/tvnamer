#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Utilities for tvnamer, including filename parsing
"""

import os

import tvdb_api

from tvnamer_exceptions import InvalidPath


class ConfigManager(dict):
    """Stores configuration options, deals with optional parsing and saving
    of options to disc.
    """

    def __init__(self):
        super(ConfigManager, self).__init__(self)
        # Default options
        self['verbose'] = False
        self['recursive'] = False


class FileFinder(object):
    """Given a file, it will verify it exists, given a folder it will descend
    one level into it and return a list of files, unless the recursive argument
    is True, in which case it finds all files contained within the path.
    """

    def __init__(self, path, recursive = False):
        self.path = path
        self.recursive = recursive

    def checkPath(self):
        """Checks if path is valid file or folder, raises InvalidPath if not
        """
        if not os.path.isfile(self.path) and not os.path.isdir(self.path):
            raise InvalidPath(self.path)

    def findFiles(self):
        """Returns list of files
        """
        pass


class FileParser(object):
    """Deals with parsing of filenames
    """
    pass


class EpisodeInfo(object):
    """Stores information (series, episode number, episode name), and contains
    logic to generate new name
    """

    def __init__(self,
        seriesname = None,
        episodenumber = None,
        seasonnumber = None,
        episodename = None):

        self.seriesname = seriesname
        self.episodenumber = episodenumber
        self.seasonnumber = seasonnumber
        self.episodename = episodename


class Renamer(object):
    """Deals with renaming of files
    """
    pass
