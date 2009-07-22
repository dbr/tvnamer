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
import re
import sys
import xml
import elementtree.ElementTree as ET

import tvdb_api

from tvnamer_exceptions import (InvalidPath, InvalidConfigFile,
InvalidFilename, WrongConfigVersion, InvalidConfigFile)


def warn(text):
    """Displays message to sys.stdout
    """
    sys.stderr.write("%s\n" % text)


def _serialiseElement(root, name, elem, type='option'):
    """Used for config XML saving, currently supports strings, integers
    and lists contains the any of these
    """
    celem = ET.SubElement(root, type)
    if name is not None:
        celem.set('name', name)

    if isinstance(elem, bool):
        celem.set('type', 'bool')
        celem.text = str(elem)
        return
    elif isinstance(elem, int):
        celem.set('type', 'int')
        celem.text = str(elem)
        return
    elif isinstance(elem, basestring):
        celem.set('type', 'string')
        celem.text = elem
        return
    elif isinstance(elem, list):
        celem.set('type', 'list')
        for subelem in elem:
            _serialiseElement(celem, None, subelem, 'value')
        return


def _deserialiseItem(ctype, citem):
    """Used for config XML loading, currently supports strings, integers
    and lists contains the any of these
    """
    if ctype == 'int':
        return int(citem.text)
    elif ctype == 'string':
        return citem.text
    elif ctype == 'bool':
        if citem.text == 'True':
            return True
        elif citem.text == 'False':
            return False
        else:
            raise InvalidConfigFile(
                "Boolean value for %s was not 'True' or ', was %r" % (
                    citem.text))
    elif ctype == 'list':
        ret = []
        for subitem in citem:
            ret.append(_deserialiseItem(subitem.attrib['type'], subitem))
        return ret


def _indentTree(elem, level=0):
    i = "\n" + "  " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            _indentTree(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


class _ConfigManager(dict):
    """Stores configuration options, deals with optional parsing and saving
    of options to disc.
    """

    VERSION = 1
    DEFAULT_CONFIG_FILE = os.path.expanduser("~/.tvnamer.xml")

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
                [\._ -][^\\/]*$'''],

            'filename_with_episode': '%(showname)s - [%(seasonno)02dx%(episode)s] - %(episodename)s',
            'filename_without_episode': '%(showname)s - [%(seasonno)02dx%(episode)s]',
            'episode_single': '%02d',
            'episode_seperator': '-',
            }

        # Updates defaults dict with current settings
        for dkey, dvalue in defaults.items():
            self.setdefault(dkey, dvalue)

    def _clearConfig(self):
        """Clears all config options, usually before loading a new config file
        """
        self.clear()

    def _loadConfig(self, xml):
        """Loads a config from a file
        """
        try:
            root = ET.fromstring(xml)
        except xml.parsers.expat.ExpatError, errormsg:
            raise InvalidConfigFile(errormsg)

        version = int(root.attrib['version'])
        if version != 1:
            raise WrongConfigVersion(
                'Expected version %d, got version %d' % (
                    self.VERSION, version))

        conf = {}
        for citem in root:
            value = _deserialiseItem(citem.attrib['type'], citem)
            conf[citem.attrib['name']] = value

        return conf

    def _saveConfig(self, config):
        root = ET.Element('tvnamer')
        root.set('version', str(self.VERSION))

        for ckey, cvalue in config.items():
            _serialiseElement(root, ckey, cvalue)

        _indentTree(root)
        return ET.tostring(root).strip()

    def loadConfig(self, filename):
        """Use Config.loadFile("something") to load a new config files, clears
        all existing options
        """
        self._clearConfig()
        try:
            xml = open(filename).read()
        except IOError, errormsg:
            raise InvalidConfigFile(errormsg)
        else:
            loaded_conf = self._loadConfig(xml)
            self._setDefaults() # Makes sure all config options are set
            self.update(loaded_conf)

    def saveConfig(self, filename):
        """Stores config options into a file
        """
        xml = self._saveConfig(self)
        try:
            f = open(filename, 'w')
        except IOError, errormsg:
            raise InvalidConfigFile(errormsg)
        else:
            f.write(xml)
            f.close()

    def useDefaultConfig(self):
        """Uses only the default settings, works similarly to Config.loadFile
        """
        self._clearConfig()
        self._setDefaults()


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
        self.compiled_regexs = []
        self._compileRegexs()

    def _compileRegexs(self):
        for cpattern in Config['episode_patterns']:
            try:
                cregex = re.compile(cpattern, re.VERBOSE)
            except re.error, errormsg:
                warn("WARNING: Invalid episode_pattern, %s. %s" % (
                    errormsg, cregex.pattern))
            else:
                self.compiled_regexs.append(cregex)

    def parse(self):
        filepath, filename = os.path.split(self.path)

        for cmatcher in self.compiled_regexs:
            match = cmatcher.match(filename)
            if match:
                namedgroups = match.groupdict().keys()

                if 'episodenumber1' in namedgroups:
                    # Multiple episodes, have episodenumber1 or 2 etc
                    epnos = []
                    for cur in namedgroups:
                        epnomatch = re.match('episodenumber(\d+)', cur)
                        if epnomatch:
                            epnos.append(int(match.group(cur)))
                    epnos.sort()
                    episodenumber = epnos

                elif 'episodenumberstart' in namedgroups:
                    # Multiple episodes, regex specifies start and end number
                    start = int(match.group('episodenumberstart'))
                    end = int(match.group('episodenumberend'))
                    episodenumber = range(start, end + 1)

                else:
                    episodenumber = int(match.group('episodenumber'))

                if 'seasonnumber' in namedgroups:
                    seasonnumber = int(match.group('seasonnumber'))
                else:
                    # No season number specified, usually for Anime
                    seasonnumber = None

                episode = EpisodeInfo(
                    showname = match.group('showname'),
                    seasonnumber = seasonnumber,
                    episodenumber = episodenumber)
                return episode
        else:
            raise InvalidFilename(self.path)


class EpisodeInfo(object):
    """Stores information (season, episode number, episode name), and contains
    logic to generate new name
    """

    def __init__(self,
        showname = None,
        seasonnumber = None,
        episodenumber = None,
        episodename = None):

        self.showname = showname
        self.seasonnumber = seasonnumber
        self.episodenumber = episodenumber
        self.episodename = episodename

    def _generateFilename(self):
        """
        Uses the following config options:
        filename_with_episode # Filename when episode name is found
        filename_without_episode # Filename when no episode can be found
        episode_single # formatting for a single episode number
        episode_seperator # used to join multiple episode numbers
        """
        # Format episode number into string, or a list
        if isinstance(self.episodenumber, list):
            epno = Config['episode_seperator'].join(
                Config['episode_single'] % x for x in self.episodenumber)
        else:
            epno = Config['episode_single'] % self.episodenumber

        epdata = {
            'showname': self.showname,
            'seasonno': self.seasonnumber,
            'episode': epno,
            'episodename': self.episodename
        }

        if self.episodename is None:
            return Config['filename_with_episode'] % epdata
        else:
            return Config['filename_without_episode'] % epdata

    def __repr__(self):
        return "<%s: %s>" % (
            self.__class__.__name__,
            self._generateFilename())


class Renamer(object):
    """Deals with renaming of files
    """
    pass
