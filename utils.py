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
import sys
import re

import tvdb_api

from tvnamer_exceptions import InvalidPath, InvalidConfig, InvalidFilename


def warn(text):
    """Displays message to sys.stdout
    """
    sys.stderr.write("%s\n" % text)


class _ConfigManager(dict):
    """Stores configuration options, deals with optional parsing and saving
    of options to disc.
    """

    DEFAULT_CONFIG_FILE = os.path.expanduser("~/.tvnamer.conf")

    def __init__(self):
        super(_ConfigManager, self).__init__(self)
        if os.path.isfile(self.DEFAULT_CONFIG_FILE):
            try:
                self._loadConfig(self.DEFAULT_CONFIG_FILE)
            except InvalidConfig:
                warn("WARNING: Config file is invalid: %s\n" % (
                    self.DEFAULT_CONFIG_FILE))
                warn("Will use default configuration\n")
                self.useDefaultConfig()
        else:
            self.useDefaultConfig()

    def _clearConfig(self):
        """Clears all config options, usually before loading a new config file
        """
        self.clear()

    def _loadConfig(self, filename):
        """Loads a config from a file
        """
        pass

    def _setDefaults(self):
        """If no config file is found, these are used. If the config file
        skips any options, the missing settings are set to the defaults.
        """
        defaults = {
            'verbose': False,
            'recursive': False,
            'episode_patterns': [
                # [group] Show - 01-02 [Etc]
                '''^\[.+?\][ ]? # group name
                (?P<showname>.*?)[ ]?[-_][ ]? # show name, padding, spaces?
                (?P<episodenumberstart>\d+)   # first episode number
                ([-_]\d+)*                    # optional repeating episodes
                [-_](?P<episodenumberend>\d+) # last episode number
                [^\/]*$''',

                # [group] Show - 01 [Etc]
                '''^\[.+?\][ ]? # group name
                (?P<showname>.*) # show name
                [ ]?[-_][ ]?(?P<episodenumber>\d+)
                [^\/]*$''',

                # foo.s01e23e24*
                '''
                ^(?P<showname>.+?)[ \._\-]               # show name
                [Ss](?P<seasonnumber>[0-9]+)             # s01
                [\.\- ]?                                 # seperator
                [Ee](?P<episodenumberstart>[0-9]+)       # first e23
                ([\.\- ]?[Ee][0-9]+)*                    # e24e25 etc
                [\.\- ]?[Ee](?P<episodenumberend>[0-9]+) # final episode num
                [^\/]*$''',

                # foo.1x09-11*
                '''^(?P<showname>.+?)[ \._\-]       # show name and padding
                \[                                  # [
                    ?(?P<seasonnumber>[0-9]+)       # season
                x                                   # x
                    (?P<episodenumberstart>[0-9]+)  # episode
                -                                   # -
                    (?P<episodenumberend>[0-9]+)    # episode
                \]                                  # \]
                [^\\/]*$''',

                # foo_[s01]_[e01]
                '''^(?P<showname>.+?)[ \._\-]       # show name and padding
                \[                                  # [
                    [Ss](?P<seasonnumber>[0-9]+?)   # season
                \]                                  # ]
                _                                   # _
                \[                                  # [
                    [Ee](?P<episodenumber>[0-9]+?)  # episode
                \]?                                 # ]
                [^\\/]*$''',

                # foo.1x09*
                '''^(?P<showname>.+?)[ \._\-]       # show name and padding
                \[?                                 # [ optional
                (?P<seasonnumber>[0-9]+)            # season
                x                                   # x
                (?P<episodenumber>[0-9]+)           # episode
                \]?                                 # ] optional
                [^\\/]*$''',

                # foo.s01.e01, foo.s01_e01
                '''^(?P<showname>.+?)[ \._\-]
                [Ss](?P<seasonnumber>[0-9]+)[\.\- ]?
                [Ee](?P<episodenumber>[0-9]+)
                [^\\/]*$''',

                # foo.103*
                '''^(?P<showname>.+)[ \._\-]
                (?P<seasonnumber>[0-9]{1})
                (?P<episodenumber>[0-9]{2})
                [\._ -][^\\/]*$''',

                # foo.0103*
                '''^(?P<showname>.+)[ \._\-]
                (?P<seasonnumber>[0-9]{2})
                (?P<episodenumber>[0-9]{2,3})
                [\._ -][^\\/]*$''']}

        # Updates defaults dict with current settings
        for dkey, dvalue in defaults.items():
            self.setdefault(dkey, dvalue)

    def loadFile(self, filename):
        """Use Config.loadFile("something") to load a new config files, clears
        all existing options
        """
        self._clearConfig()
        self._loadConfig(filename)
        self._setDefaults() # Makes sure all config options are set

    def useDefaultConfig(self):
        """Uses only the default settings, works simialrly to Config.loadFile
        """
        self._clearConfig()
        self._setDefaults()

    def saveConfig(self, filename):
        """Stores config options into a file
        """
        pass


Config = _ConfigManager()


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
            return [os.path.abspath(self.path)]
        else:
            return self._findFilesInPath(self.path)

    def _findFilesInPath(self, startpath):
        """Finds files from startpath, could be called recursively
        """
        allfiles = []
        if os.path.isfile(startpath):
            allfiles.append(os.path.abspath(startpath))

        elif os.path.isdir(startpath):
            for sf in os.listdir(startpath):
                newpath = os.path.join(startpath, sf)
                newpath = os.path.abspath(newpath)
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

    def __init__(self, path):
        self.path = path
        self.regexs = []
        self._compileRegexs()

    def _compileRegexs(self):
        for cpattern in Config['episode_patterns']:
            try:
                cregex = re.compile(cpattern)
            except re.error:
                warn("WARNING: Invalid episode_patterns regex: %s" % (cregex))
            else:
                self.regexs.append(cregex)

    def parse(self):
        filepath, filename = os.path.split(self.path)

        for cmatcher in self.regexs:
            match = cmatcher.match(filename)
            if match:
                ep = EpisodeInfo(match.group(1), int(match.group(2)), int(match.group(3)))
                return ep
        else:
            raise InvalidFilename(self.path)


class EpisodeInfo(object):
    """Stores information (season, episode number, episode name), and contains
    logic to generate new name
    """

    def __init__(self,
        seasonname = None,
        seasonnumber = None,
        episodenumber = None,
        episodename = None):

        self.seasonname = seasonname
        self.seasonnumber = seasonnumber
        self.episodenumber = episodenumber
        self.episodename = episodename

    def __repr__(self):
        return "<%s: %s - [%02dx%02d] - %s>" % (
            self.__class__.__name__,
            self.seasonname,
            self.seasonnumber,
            self.episodenumber,
            self.episodename)


class Renamer(object):
    """Deals with renaming of files
    """
    pass
