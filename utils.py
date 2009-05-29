#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Utilities for tvnamer, including filename parsing
"""


class ConfigManager(dict):
    """Stores configuration options, deals with optional parsing and saving
    of options to disc.
    """

    def __init__(self):
        super(ConfigManager, self).__init__(self)
        # Default options
        #TODO: Read from file
        self['verbose'] = False
        self['recursive'] = False


class FileFinder(object):
    """Given a file, it will verify it exists, given a folder it will descend
    one level into it and return a list of files, unless the recusive argument
    is True, in which case it finds all files contained within the path.
    """

    def __init__(self, path, recusive = False):
        self.path = path
        self.recusive = recusive

    def findFiles(self):
        """Starts file-finder
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
    pass


class Renamer(object):
    """Deals with renaming of files
    """
    pass
