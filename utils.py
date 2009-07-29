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

from tvdb_api import (tvdb_error, tvdb_shownotfound, tvdb_seasonnotfound,
tvdb_episodenotfound, tvdb_episodenotfound, tvdb_attributenotfound,
tvdb_userabort)

from config import Config
from tvnamer_exceptions import (InvalidPath, InvalidFilename, UserAbort)


def warn(text):
    """Displays message to sys.stdout
    """
    sys.stderr.write("%s\n" % text)


def verbose(text):
    """Prints message if verbose option is specified
    """
    if Config['verbose']:
        print text


def getEpisodeName(tvdb_instance, episode):
    """Queries the tvdb_api.Tvdb instance for episode name and corrected
    series name.
    If series cannot be found, it will warn the user. If the episode is not
    found, it will use the corrected show name and not set an episode name.
    If the site is unreachable, it will warn the user. If the user aborts
    it will catch tvdb_api's user abort error and raise tvnamer's
    """
    try:
        show = tvdb_instance[episode.seriesname]
    except tvdb_error, errormsg:
        warn("! Warning: Error contacting www.thetvdb.com:\n%s\n" % errormsg)
        return
    except tvdb_shownotfound:
        # No such series found.
        warn("Show %s not found on www.thetvdb.com" % episode.seriesname)
        return
    else:
        # Series was found, use corrected series name
        episode.seriesname = show['seriesname']

    if not isinstance(episode.episodenumber, list):
        episode.episodenumber = [episode.episodenumber]

    epnames = []
    for cepno in episode.episodenumber:
        try:
            episodeinfo = show[episode.seasonnumber][cepno]
        except (tvdb_seasonnotfound, tvdb_episodenotfound, tvdb_attributenotfound):
            # The season, episode or name wasn't found, but the show was.
            # Use the corrected show-name, but no episode name.
            warn("Episode %02d of season %02d was not found" % (
                cepno, episode.seasonnumber))
        else:
            epnames.append(episodeinfo['episodename'])

    episode.episodename = epnames
    return episode


class FileFinder(object):
    """Given a file, it will verify it exists, given a folder it will descend
    one level into it and return a list of files, unless the recursive argument
    is True, in which case it finds all files contained within the path.
    """

    def __init__(self, path, recursive = False):
        self.path = path
        self.recursive = recursive

    def findFiles(self):
        """Returns list of files found at path
        """
        if os.path.isfile(self.path):
            return [os.path.abspath(self.path)]
        elif os.path.isdir(self.path):
            return self._findFilesInPath(self.path)
        else:
            raise InvalidPath("%s is not a valid file/directory" % self.path)

    def _findFilesInPath(self, startpath):
        """Finds files from startpath, could be called recursively
        """
        allfiles = []
        if os.path.isfile(startpath):
            allfiles.append(os.path.abspath(startpath))

        elif os.path.isdir(startpath):
            for subf in os.listdir(startpath):
                newpath = os.path.join(startpath, subf)
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
        """Takes episode_patterns from config, compiles them all
        into self.compiled_regexs
        """
        for cpattern in Config['episode_patterns']:
            try:
                cregex = re.compile(cpattern, re.VERBOSE)
            except re.error, errormsg:
                warn("WARNING: Invalid episode_pattern, %s. %s" % (
                    errormsg, cregex.pattern))
            else:
                self.compiled_regexs.append(cregex)

    def parse(self):
        """Runs path via configured regex, extracting data from groups.
        Returns an EpisodeInfo instance containing extracted data.
        """
        _, filename = os.path.split(self.path)

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

                seriesname = match.group('seriesname')

                #remove ._- characters from name (- removed only if next to
                # end of line)
                seriesname = re.sub("[\._]|\-(?=$)", " ", seriesname).strip()

                episode = EpisodeInfo(
                    seriesname = seriesname,
                    seasonnumber = seasonnumber,
                    episodenumber = episodenumber,
                    filename = self.path)
                return episode
        else:
            raise InvalidFilename(self.path)


def formatEpisodeName(names):
    """Takes a list of episode names, formats them into a string.
    If two names are supplied, such as "Pilot (1)" and "Pilot (2)", the
    returned string will be "Pilot (1-2)"

    If two different episode names are found, such as "The first", and
    "Something else" it will return "The first, Something else"
    """
    if len(names) == 1:
        return names[0]

    found_names = []
    numbers = []
    for cname in names:
        number = re.match("(.*) \(([0-9]+)\)$", cname)
        if number:
            epname, epno = number.group(1), number.group(2)
            if len(found_names) > 0 and epname not in found_names:
                return ", ".join(names)
            found_names.append(number.group(1))
            numbers.append(int(number.group(2)))
        else:
            # An episode didn't match
            return ", ".join(names)

    names = []
    start, end = min(numbers), max(numbers)
    names.append("%s (%d-%d)" % (found_names[0], start, end))
    return ", ".join(names)

class EpisodeInfo(object):
    """Stores information (season, episode number, episode name), and contains
    logic to generate new name
    """

    def __init__(self,
        seriesname = None,
        seasonnumber = None,
        episodenumber = None,
        episodename = None,
        filename = None):

        self.seriesname = seriesname
        self.seasonnumber = seasonnumber
        self.episodenumber = episodenumber
        self.episodename = episodename
        self.filename = filename

    def generateFilename(self):
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

        # Data made available to config'd output file format
        epdata = {
            'seriesname': self.seriesname,
            'seasonno': self.seasonnumber,
            'episode': epno,
            'episodename': self.episodename}

        if self.episodename is None:
            return Config['filename_without_episode'] % epdata
        else:
            if isinstance(self.episodename, list):
                epdata['episodename'] = formatEpisodeName(self.episodename)
            return Config['filename_with_episode'] % epdata

    def __repr__(self):
        return "<%s: %s>" % (
            self.__class__.__name__,
            self.generateFilename())


class Renamer(object):
    """Deals with renaming of files
    """

    def __init__(self, filename):
        self.filename = filename

    def newName(self, newName, keepExtension=True):
        """Renames a file, keeping the path the same.

        If keepExtension is True (default), the existing extension (if any) is
        retained. If False, the existing extension is removed, and the one in
        newName is used if it is supplied.

        If keepExtension is False, the extension in newName will be used
        """
        filepath, filename = os.path.split(self.filename)
        filename, fileext = os.path.splitext(filename)

        if keepExtension:
            newName = newName + fileext

        newpath = os.path.join(filepath, newName)
        os.rename(self.filename, newpath)
        self.filename = newpath
