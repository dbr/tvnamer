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
        if os.path.isfile(self.path) or os.path.isdir(self.path):
            return True
        else:
            raise InvalidPath(self.path)

    def findFiles(self):
        """Returns list of files found at path
        """
        if os.path.isfile(self.path):
            return [self.path]
        else:
            return self._findFilesInPath(self.path)

    def _findFilesInPath(self, startpath):
        """Finds files from startpath, could be called recursively
        """
        allfiles = []
        if os.path.isfile(startpath):
            allfiles.append(startpath)

        elif os.path.isdir(startpath):
            for sf in os.listdir(startpath):
                newpath = os.path.join(startpath, sf)
                if os.path.isfile(newpath):
                    allfiles.append(newpath)
                else:
                    if self.recursive:
                        allfiles.extend(self._findFilesInPath(newpath))
                    #end if recursive
                #end if isfile
            #end for sf
        #end if isdir
        return allfiles


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
        seasonnumber = None,
        episodenumber = None,
        episodename = None):

        self.seriesname = seriesname
        self.seasonnumber = seasonnumber
        self.episodenumber = episodenumber
        self.episodename = episodename

    def __repr__(self):
        return "<%s: %s - [%02dx%02d] - %s>" % (
            self.__class__.__name__,
            self.seriesname,
            self.seasonnumber,
            self.episodenumber,
            self.episodename)


class Renamer(object):
    """Deals with renaming of files
    """
    pass
