#!/usr/bin/env python

""" Utilities for tvnamer, including filename parsing
"""

import os
import re
import logging
import datetime

from tvdb_api import (tvdb_error, tvdb_shownotfound, tvdb_seasonnotfound,
                      tvdb_episodenotfound, tvdb_attributenotfound, tvdb_userabort)

from config import Config
from _titlecase import titlecase
from tvnamer_exceptions import (InvalidPath, InvalidFilename, ShowNotFound,
                                DataRetrievalError, SeasonNotFound, EpisodeNotFound,
                                EpisodeNameNotFound, ConfigValueError, UserAbort,
                                BaseTvnamerException)

from formatting import makeValidFilename, formatEpisodeNames, formatEpisodeNumbers
from unicode_helper import p


def log():
    """ Returns the logger for current file
    """
    return logging.getLogger(__name__)


def split_extension(filename):
    """ Splits the extension from the filename. Uses regular expression
        specified in config under 'extension_pattern' key.

        By default the dot is included in the extension, so other functions
        should use something like '
            full = basename + extension
        or
            full = u"%s%s" % (basename, extension)
        to get full filename again.
    """
    base = re.sub(Config["extension_pattern"], "", filename)
    ext = filename.replace(base, "")
    return base, ext


def _applyReplacements(cfile, replacements):
    """ Applies custom replacements.
        @param str  cfile
        @param list replacements - list of dicts with keys "match", "replacement", and (optional) "is_regex"
    """
    for rep in replacements:
        if not rep.get('with_extension', False):
            # By default, preserve extension
            cfile, cext = split_extension(cfile)
        else:
            cfile = cfile
            cext = ""

        if 'is_regex' in rep and rep['is_regex']:
            cfile = re.sub(rep['match'], rep['replacement'], cfile)
        else:
            cfile = cfile.replace(rep['match'], rep['replacement'])

        # Rejoin extension (cext might be empty-string)
        cfile = cfile + cext

    return cfile


def applyCustomInputReplacements(cfile):
    """ Applies custom input filename replacements, wraps _applyReplacements
    """
    return _applyReplacements(cfile, Config['input_filename_replacements'])


def applyCustomOutputReplacements(cfile):
    """ Applies custom output filename replacements, wraps _applyReplacements
    """
    return _applyReplacements(cfile, Config['output_filename_replacements'])


def applyCustomFullpathReplacements(cfile):
    """ Applies custom replacements to full path, wraps _applyReplacements
    """
    return _applyReplacements(cfile, Config['move_files_fullpath_replacements'])


def cleanRegexedSeriesName(seriesname):
    """ Cleans up series name by removing any . and _
        characters, along with any trailing hyphens.

        Is basically equivalent to replacing all _ and . with a
        space, but handles decimal numbers in string, for example:

        >>> cleanRegexedSeriesName("an.example.1.0.test")
        'an example 1.0 test'
        >>> cleanRegexedSeriesName("an_example_1.0_test")
        'an example 1.0 test'
    """

    # TODO: Could this be made to clean "Hawaii.Five-0.2010" into "Hawaii Five-0 2010"?
    seriesname = re.sub("(\D)[.](\D)", "\\1 \\2", seriesname)
    seriesname = re.sub("(\D)[.]", "\\1 ", seriesname)
    seriesname = re.sub("[.](\D)", " \\1", seriesname)
    seriesname = seriesname.replace("_", " ")
    seriesname = re.sub("-$", "", seriesname)
    return seriesname.strip()


def replaceInputSeriesName(seriesname):
    """ Allow specified replacements of series names in cases where default
        filenames match the wrong series, e.g. missing year gives wrong answer,
        or vice versa. This helps the TVDB query get the right match.
    """

    for pat, replacement in Config['input_series_replacements'].iteritems():
        if re.match(pat, seriesname, re.IGNORECASE | re.UNICODE):
            return replacement
    return seriesname


def replaceOutputSeriesName(seriesname):
    """ Transform TVDB series names after matching from TVDB, transform the
        series name for desired abbreviation, etc.

        This affects the output filename.
    """

    return Config['output_series_replacements'].get(seriesname, seriesname)


def handleYear(year):
    """ Handle two-digit years with heuristic guessing.

        Assumes 50-99 becomes 1950-1999, and 0-49 becomes 2000-2049

        ..might need to rewrite this function in 2050, but that seems like
        a reasonable limitation
    """

    year = int(year)

    # No need to guess with 4-digit years
    if year > 999:
        return year

    if year < 50:
        return 2000 + year
    else:
        return 1900 + year


class FileFinder(object):
    """ Given a file, it will verify it exists. Given a folder it will descend
        one level into it and return a list of files, unless the recursive argument
        is True, in which case it finds all files contained within the path.

        The with_extension argument is a list of valid extensions, without leading
        spaces. If an empty list (or None) is supplied, no extension checking is
        performed.

        The filename_blacklist argument is a list of regexp strings to match against
        the filename (minus the extension). If a match is found, the file is skipped
        (e.g. for filtering out "sample" files). If [] or None is supplied, no
        filtering is done
    """

    def __init__(self, path, with_extension=None, filename_blacklist=None, recursive=False):
        self.path = path
        if with_extension is None:
            self.with_extension = []
        else:
            self.with_extension = with_extension
        if filename_blacklist is None:
            self.with_blacklist = []
        else:
            self.with_blacklist = filename_blacklist
        self.recursive = recursive

    def findFiles(self):
        """ Returns list of files found at path
        """
        if os.path.isfile(self.path):
            path = os.path.abspath(self.path)
            if self._checkExtension(path) and not self._blacklistedFilename(path):
                return [path]
            else:
                return []
        elif os.path.isdir(self.path):
            return self._findFilesInPath(self.path)
        else:
            raise InvalidPath("%s is not a valid file/directory" % self.path)

    def _checkExtension(self, fname):
        """ Checks if the file extension is blacklisted in valid_extensions
        """

        if len(self.with_extension) == 0:
            return True

        # don't use split_extension here (otherwise valid_extensions is useless)!
        _, extension = os.path.splitext(fname)
        if extension in [".%s" % ext for ext in self.with_extension]:
            return True
        return False

    def _blacklistedFilename(self, filepath):
        """ Checks if the filename (optionally excluding extension)
            matches filename_blacklist

            self.with_blacklist should be a list of strings and/or dicts:

            a string, specifying an exact filename to ignore
            "filename_blacklist": [".DS_Store", "Thumbs.db"],

            a dictionary, where each dict contains:

            Key 'match' - (if the filename matches the pattern, the filename
            is blacklisted)

            Key 'is_regex' - if True, the pattern is treated as a
            regex. If False, simple substring check is used (if
            cur['match'] in filename). Default is False

            Key 'full_path' - if True, full path is checked. If False, only
            filename is checked. Default is False.

            Key 'exclude_extension' - if True, the extension is removed
            from the file before checking. Default is False.
        """

        if len(self.with_blacklist) == 0:
            return False

        fdir, fullname = os.path.split(filepath)
        fname, fext = split_extension(fullname)

        for fblacklist in self.with_blacklist:
            if isinstance(fblacklist, basestring):
                if fullname == fblacklist:
                    return True
            else:
                if fblacklist.get("full_path"):
                    to_check = filepath
                elif fblacklist.get("exclude_extension"):
                    to_check = fname
                else:
                    to_check = fullname

                if fblacklist.get("is_regex"):
                    if re.match(fblacklist["match"], to_check):
                        return True
                elif fblacklist["match"] in to_check:
                    return True
        else:
            return False

    def _findFilesInPath(self, startpath):
        """ Finds files from startpath, could be called recursively
        """
        allfiles = []
        if not os.access(startpath, os.R_OK):
            log().info("Skipping inaccessible path %s" % startpath)
            return allfiles

        for subf in os.listdir(unicode(startpath)):
            newpath = os.path.join(startpath, subf)
            newpath = os.path.abspath(newpath)
            if os.path.isfile(newpath):
                if self._checkExtension(subf) and not self._blacklistedFilename(subf):
                    allfiles.append(newpath)
            elif self.recursive:
                allfiles.extend(self._findFilesInPath(newpath))
        return allfiles


class FileParser(object):
    """ Deals with parsing of filenames
    """

    def __init__(self, path):
        self.path = path
        self.compiled_regexs = []
        self._compileRegexs()

    def _compileRegexs(self):
        """ Compiles items from 'filename_patterns' list in config into re.RegexObject,
            appends into self.compiled_regexs. Checks validity of each regex (must contain
            certain matching groups).
        """
        for cpattern in Config['filename_patterns']:
            try:
                cregex = re.compile(cpattern, re.VERBOSE)
                groups = set(cregex.groupindex.keys())

                # check regex validity
                if 'seriesname' not in groups:
                    raise ConfigValueError(
                        "Regex must contain group 'seriesname'."
                        "Pattern was:\n" + cpattern)

                dateset = set(['year', 'month', 'day'])
                intersection = groups.intersection(dateset)
                if len(intersection) > 0 and intersection != dateset:
                    raise ConfigValueError(
                        "Date-based regex must contain groups 'year', 'month' and 'day'."
                        "Pattern was:\n" + cpattern)

                # check for episodenumber only in non-dated regex
                elif len(intersection) == 0:
                    epnoset = set(['episodenumberstart', 'episodenumberend'])
                    intersection = groups.intersection(epnoset)
                    if len(intersection) > 0 and intersection != epnoset:
                        raise ConfigValueError(
                            "Regex must contain both (or none of) following groups:"
                            "'episodenumberstart', 'episodenumberend'"
                            "Pattern was:\n" + cpattern)

                    epnoset.update(set(['episodenumber'] + ['episodenumber%s' % x for x in xrange(1, 10)]))
                    intersection = groups.intersection(epnoset)
                    if len(intersection) == 0:
                        raise ConfigValueError(
                            "Regex does not contain episode number group, should"
                            "contain episodenumber, episodenumber1-9, or"
                            "episodenumberstart and episodenumberend."
                            "Pattern was:\n" + cpattern)

            except re.error, errormsg:
                log().warning("Invalid episode_pattern (error: %s)\nPattern:\n%s" % (errormsg, cpattern))
            else:
                self.compiled_regexs.append(cregex)

    def parse(self):
        """ Runs path via configured regex, extracting data from groups.
            Returns an EpisodeInfo instance containing extracted data.
        """

        _, filename = os.path.split(self.path)
        filename = applyCustomInputReplacements(filename)

        for cmatcher in self.compiled_regexs:
            match = cmatcher.match(filename)
            if not match:
                continue

            parsed = match.groupdict()

            episode_type = self.getEpType(parsed)
            episode_numbers = self.getEpNumbers(parsed, episode_type, filename)

            if parsed.get('seriesname'):
                parsed['seriesname'] = cleanRegexedSeriesName(parsed['seriesname'])
                parsed['seriesname'] = replaceInputSeriesName(parsed['seriesname'])

            return EpisodeInfo(filename=self.path, eptype=episode_type, episodenumbers=episode_numbers, extra=parsed)

        # body of for loop didn't return, which means no regex matches the filename
        else:
            emsg = "Cannot parse %r" % self.path
            if len(Config['input_filename_replacements']) > 0:
                emsg += " with replacements: %r" % filename
            raise InvalidFilename(emsg)

    def getEpType(self, parsed):
        """ Determines correct episode type from parsed values
        """

        if parsed.get('group'):
            if parsed.get('crc'):
                return 'anime_crc'
            return 'anime'
        if 'year' in parsed.keys():
            return 'dated'
        if not parsed.get('seasonnumber'):
            return 'noseason'
        return 'default'

    def getEpNumbers(self, parsed, eptype, filename):
        """ Returns parsed episode numbers, updates 'parsed' dict (removes auxiliary items,
            adds 'year', 'month', 'day' items for dated episodes.
        """

        if eptype == 'dated':
            episodenumbers = [datetime.date(handleYear(parsed.get('year')),
                                            int(parsed.get('month')),
                                            int(parsed.get('day')))]
            parsed["year"] = episodenumbers[0].year
            parsed["month"] = episodenumbers[0].month
            parsed["day"] = episodenumbers[0].day

        elif 'episodenumberstart' in parsed.keys():
            # Multiple episodes, regex specifies start and end number
            start = int(parsed.get('episodenumberstart'))
            end = int(parsed.get('episodenumberend'))
            if start > end:
                # Swap start and end
                start, end = end, start
            episodenumbers = range(start, end + 1)
            if end - start > 5:
                log().warning("WARNING: %s episodes detected in file: %s, confused by numeric episode name, using first match: %s" % (end - start, filename, start))
                episodenumbers = [start]
            del parsed["episodenumberstart"]   # delete auxiliary key from parsed
            del parsed["episodenumberend"]   # delete auxiliary key from parsed

        elif 'episodenumber' in parsed.keys():
            episodenumbers = [int(parsed.get('episodenumber')), ]
            del parsed["episodenumber"]   # delete auxiliary key from parsed

        elif 'episodenumber1' in parsed.keys():
            # TODO: isn't episodenumber[1-9] useless???
            # Multiple episodes, have episodenumber1 or 2 etc
            epnos = []
            for cur in parsed.keys():
                epnomatch = re.match('episodenumber(\d+)', cur)
                if epnomatch:
                    epnos.append(int(parsed.get(cur)))
                    del parsed[cur]   # delete auxiliary key from parsed
            epnos.sort()
            episodenumbers = epnos

        else:
            # should never happen
            raise BaseTvnamerException("Unable to parse episodenumbers")

        return episodenumbers


class EpisodeInfo(object):
    """ Stores information (season, episode number, episode name), and contains
        logic to generate new name
    """

    _fullpath = str
    filename = str
    extension = str

    def __init__(self, filename, episodenumbers, eptype='default', extra=None, **kwargs):
        self.fullpath = filename
        self.eptype = eptype
        self.episodenumbers = episodenumbers

        if extra is None:
            self.extra = {}
        else:
            self.extra = extra
        self.extra.update(kwargs)

    def __getattr__(self, key):
        """ Expose values of self.extra as attributes of EpisodeInfo.
            First check if self already has attribute 'key', otherwise look into self.extra.
        """

        if key in self.__dict__:
            return self.__dict__[key]
        elif key in self.extra:
            return self.extra[key]
        raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, key))

    def __hasattr__(self, key):
        return key in self.__dict__ or key in self.extra

    # TODO: this might not be necessary as self.fullpath is not updated after rename
    def fullpath():
        def fget(self):
            return self._fullpath

        def fset(self, value):
            self._fullpath = value
            self.filename = os.path.split(value)[1]
            self.filename, self.extension = split_extension(self.filename)
        return locals()

    fullpath = property(**fullpath())

    @property
    def fullfilename(self):
        return u"%s%s" % (self.filename, self.extension)

    def sortable_info(self):
        """ Returns a list of sortable information
        """
        info = []
        info.append(self.extra['seriesname'])
        if hasattr(self, 'seasonnumber'):
            info.append(int(self.seasonnumber))
        info.append(self.episodenumbers)
        return info

    def number_string(self):
        """ Used in UI
        """
        string = ""
        if hasattr(self, 'seasonnumber'):
            string += "season: %s, " % self.seasonnumber
        string += "episode: %s" % ", ".join([str(x) for x in self.episodenumbers])
        return string

    def getFormatString(self):
        """ Returns format string from Config for current episode type.
        """

        epname = self.extra.get('episodename')
        if self.eptype == 'anime':
            return Config['filename_anime_with_episode_without_crc'] if epname else Config['filename_anime_without_episode_without_crc']
        elif self.eptype == 'anime_crc':
            return Config['filename_anime_with_episode'] if epname else Config['filename_anime_without_episode']
        elif self.eptype == 'dated':
            return Config['filename_with_date_and_episode'] if epname else Config['filename_with_date_without_episode']
        elif self.eptype == 'noseason':
            return Config['filename_with_episode_no_season'] if epname else Config['filename_without_episode_no_season']
        else:
            return Config['filename_with_episode'] if epname else Config['filename_without_episode']

    def populateFromTvdb(self, tvdb_instance, force_name=None, series_id=None):
        """ Queries the tvdb_api.Tvdb instance for episode name and corrected series name.

            If series cannot be found, it will warn the user. If the episode is not
            found, it will use the corrected show name and not set an episode name.

            If the site is unreachable, it will warn the user. If the user aborts
            it will catch tvdb_api's user abort error and raise tvnamer's
        """

        try:
            if series_id is None:
                show = tvdb_instance[force_name or self.extra['seriesname']]
            else:
                series_id = int(series_id)
                tvdb_instance._getShowData(series_id, Config['language'])
                show = tvdb_instance[series_id]
        except tvdb_error, errormsg:
            raise DataRetrievalError("Error with www.thetvdb.com: %s" % errormsg)
        except tvdb_shownotfound:
            # No such series found.
            raise ShowNotFound("Show %s not found on www.thetvdb.com" % self.extra['seriesname'])
        except tvdb_userabort, error:
            raise UserAbort(unicode(error))
        else:
            # Series was found, use corrected series name
            self.extra['seriesname'] = replaceOutputSeriesName(show['seriesname'])

        if self.eptype == 'dated':
            # Date-based episode
            epnames = []
            for cepno in self.episodenumbers:
                try:
                    sr = show.airedOn(cepno)
                    if len(sr) > 1:
                        raise EpisodeNotFound("Ambigious air date %s, there were %s episodes on that day" % (cepno, len(sr)))
                    epnames.append(sr[0]['episodename'])
                except tvdb_episodenotfound:
                    raise EpisodeNotFound("Episode that aired on %s could not be found" % cepno)
            self.extra['episodename'] = epnames
            return

        # Default to 1, series without concept of seasons have all episodes in season 1
        seasonnumber = int(self.extra.get('seasonnumber') or 1)

        epnames = []
        for cepno in self.episodenumbers:
            try:
                episodeinfo = show[seasonnumber][cepno]

            except tvdb_seasonnotfound:
                raise SeasonNotFound("Season %s of show %s could not be found" % (seasonnumber, self.extra['seriesname']))

            except tvdb_episodenotfound:
                # Try to search by absolute_number
                sr = show.search(cepno, "absolute_number")
                if len(sr) > 1:
                    # For multiple results try and make sure there is a direct match
                    unsure = True
                    for e in sr:
                        if int(e['absolute_number']) == cepno:
                            epnames.append(e['episodename'])
                            unsure = False
                    # If unsure error out
                    if unsure:
                        raise EpisodeNotFound("No episode actually matches %s, found %s results instead" % (cepno, len(sr)))
                elif len(sr) == 1:
                    epnames.append(sr[0]['episodename'])
                else:
                    raise EpisodeNotFound(
                        "Episode %s of show %s, season %s could not be found (also tried searching by absolute episode number)" % (
                            cepno, self.extra['seriesname'], seasonnumber))

            except tvdb_attributenotfound:
                raise EpisodeNameNotFound("Could not find episode name for %s" % cepno)
            else:
                epnames.append(episodeinfo['episodename'])

        self.extra['episodename'] = epnames

    def getepdata(self):
        """ Return dict of formatted data available to config'd output file format
        """

        epdata = self.extra.copy()
        epdata.update({
            'originalfilename': self.fullfilename,
            'ext': self.extension,
            'episode': formatEpisodeNumbers(self.episodenumbers),
        })

        # format dynamic parts according to config
        for key in epdata.keys():
            if key == 'originalfilename':
                continue
            if key == 'episodename':
                epdata[key] = formatEpisodeNames(epdata[key])
            if key in ('seriesname', 'episodename'):
                if Config['lowercase_dynamic_parts']:
                    epdata[key] = epdata[key].lower()
                elif Config['titlecase_dynamic_parts']:
                    epdata[key] = titlecase(epdata[key])
                epdata[key] = makeValidFilename(epdata[key])

            # TODO: would be better to expose only strings? (%s can accept int, but %d cannot accept str,
            # so using %s in format strings is less error-prone)
            if key == 'seasonnumber':
                epdata[key] = int(epdata[key])

        return epdata

    def getNewFullPath(self):
        """ Generates final fullPath, with all replacements, formatting etc.
            It's ready to pass it to Renamer.rename().
        """

        epdata = self.getepdata()
        newName = self.getFormatString() % epdata

        if len(Config['output_filename_replacements']) > 0:
            p("Before custom output replacements: '%s'" % newName)
            newName = applyCustomOutputReplacements(newName)
            p("After custom output replacements:  '%s'" % newName)

        if self.eptype == 'dated':
            newPath = Config['move_files_destination_date'] % epdata
        else:
            newPath = Config['move_files_destination'] % epdata
        if Config['move_files_destination_is_filepath']:
            newPath, newName = os.path.split(newPath)

        # make newName lowercase if specified in config
        if Config['lowercase_filename']:
            newName = newName.lower()

        # make sure the filename is valid
        newName = makeValidFilename(newName)

        # Join new filepath to old one (to handle realtive dirs)
        oldPath = os.path.dirname(self.fullpath)
        newFullPath = os.path.abspath(os.path.join(oldPath, newPath, newName))

        # apply full-path replacements
        if len(Config['move_files_fullpath_replacements']) > 0:
            p("Before custom full path replacements: '%s'" % (newFullPath))
            newFullPath = applyCustomFullpathReplacements(newFullPath)

        return newFullPath

    def generateFilename(self):
        """ Wraps getNewFullPath
            DEPRECATED: useful only for tests, getNewFullPath should be used instead
        """
        return os.path.split(self.getNewFullPath())[1]

    def __repr__(self):
        return u"<%s: %r>" % (self.__class__.__name__, self.fullfilename)
