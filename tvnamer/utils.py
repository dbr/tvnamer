#!/usr/bin/env python

"""Utilities for tvnamer, including filename parsing
"""

import datetime
import os
import re
import sys
import logging

from tvdb_api import (tvdb_error, tvdb_shownotfound, tvdb_seasonnotfound,
tvdb_episodenotfound, tvdb_attributenotfound, tvdb_userabort)

from config import Config
from _titlecase import titlecase
from tvnamer_exceptions import (InvalidPath, InvalidFilename,
ShowNotFound, DataRetrievalError, SeasonNotFound, EpisodeNotFound,
EpisodeNameNotFound, ConfigValueError, UserAbort)

from formatting import makeValidFilename, formatEpisodeNames, formatEpisodeNumbers


def log():
    """Returns the logger for current file
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
    """Applies custom replacements.

    Argument cfile is string.

    Argument replacements is a list of dicts, with keys "match",
    "replacement", and (optional) "is_regex"
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
    """Applies custom input filename replacements, wraps _applyReplacements
    """
    return _applyReplacements(cfile, Config['input_filename_replacements'])


def applyCustomOutputReplacements(cfile):
    """Applies custom output filename replacements, wraps _applyReplacements
    """
    return _applyReplacements(cfile, Config['output_filename_replacements'])


def applyCustomFullpathReplacements(cfile):
    """Applies custom replacements to full path, wraps _applyReplacements
    """
    return _applyReplacements(cfile, Config['move_files_fullpath_replacements'])


def cleanRegexedSeriesName(seriesname):
    """Cleans up series name by removing any . and _
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
    """allow specified replacements of series names

    in cases where default filenames match the wrong series,
    e.g. missing year gives wrong answer, or vice versa

    This helps the TVDB query get the right match.
    """
    for pat, replacement in Config['input_series_replacements'].iteritems():
        if re.match(pat, seriesname, re.IGNORECASE|re.UNICODE):
            return replacement
    return seriesname


def replaceOutputSeriesName(seriesname):
    """transform TVDB series names

    after matching from TVDB, transform the series name for desired abbreviation, etc.

    This affects the output filename.
    """
    return Config['output_series_replacements'].get(seriesname, seriesname)


def handleYear(year):
    """Handle two-digit years with heuristic-ish guessing

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
    """Given a file, it will verify it exists. Given a folder it will descend
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

    def __init__(self, path, with_extension = None, filename_blacklist = None, recursive = False):
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
        """Returns list of files found at path
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
        """Checks if the file extension is blacklisted in valid_extensions
        """
        if len(self.with_extension) == 0:
            return True

        # don't use split_extension here (otherwise valid_extensions is useless)!
        _, extension = os.path.splitext(fname)
        for cext in self.with_extension:
            cext = ".%s" % cext
            if extension == cext:
                return True
        else:
            return False

    def _blacklistedFilename(self, filepath):
        """Checks if the filename (optionally excluding extension)
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
                    continue

            if "full_path" in fblacklist and fblacklist["full_path"]:
                to_check = filepath
            else:
                if fblacklist.get("exclude_extension", False):
                    to_check = fname
                else:
                    to_check = fullname

            if fblacklist.get("is_regex", False):
                m = re.match(fblacklist["match"], to_check)
                if m is not None:
                    return True
            else:
                m = fblacklist["match"] in to_check
                if m:
                    return True
        else:
            return False

    def _findFilesInPath(self, startpath):
        """Finds files from startpath, could be called recursively
        """
        allfiles = []
        if not os.access(startpath, os.R_OK):
            log().info("Skipping inaccessible path %s" % startpath)
            return allfiles

        for subf in os.listdir(unicode(startpath)):
            newpath = os.path.join(startpath, subf)
            newpath = os.path.abspath(newpath)
            if os.path.isfile(newpath):
                if not self._checkExtension(subf):
                    continue
                elif self._blacklistedFilename(subf):
                    continue
                else:
                    allfiles.append(newpath)
            else:
                if self.recursive:
                    allfiles.extend(self._findFilesInPath(newpath))
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
        for cpattern in Config['filename_patterns']:
            try:
                cregex = re.compile(cpattern, re.VERBOSE)
            except re.error, errormsg:
                log().warn("Invalid episode_pattern (error: %s)\nPattern:\n%s" % (
                    errormsg, cpattern))
            else:
                self.compiled_regexs.append(cregex)

    def parse(self):
        """Runs path via configured regex, extracting data from groups.
        Returns an EpisodeInfo instance containing extracted data.
        """
        _, filename = os.path.split(self.path)

        filename = applyCustomInputReplacements(filename)

        for cmatcher in self.compiled_regexs:
            match = cmatcher.match(filename)
            if not match:
                continue

            namedgroups = match.groupdict().keys()

            # create copy of match.groupdict for changed values
            extra_values = match.groupdict().copy()

            fmt_keys = {"epname": "filename_with_episode_no_season", "noepname": "filename_without_episode_no_season"}

            if 'episodenumber1' in namedgroups:
                # Multiple episodes, have episodenumber1 or 2 etc
                epnos = []
                for cur in namedgroups:
                    epnomatch = re.match('episodenumber(\d+)', cur)
                    if epnomatch:
                        epnos.append(int(match.group(cur)))
                        del extra_values[cur]   # delete auxiliary key from extra_values
                epnos.sort()
                episodenumbers = epnos

            elif 'episodenumberstart' in namedgroups:
                # Multiple episodes, regex specifies start and end number
                start = int(match.group('episodenumberstart'))
                end = int(match.group('episodenumberend'))
                if start > end:
                    # Swap start and end
                    start, end = end, start
                episodenumbers = range(start, end + 1)
                if end - start > 5:
                    warn("WARNING: %s episodes detected in file: %s, confused by numeric episode name, using first match: %s" %(end - start, filename, start))
                    episodenumbers = [start]
                del extra_values["episodenumberstart"]   # delete auxiliary key from extra_values
                del extra_values["episodenumberend"]   # delete auxiliary key from extra_values

            elif 'episodenumber' in namedgroups:
                episodenumbers = [int(match.group('episodenumber')), ]
                del extra_values["episodenumber"]   # delete auxiliary key from extra_values

            elif any(['year' in namedgroups, 'month' in namedgroups, 'day' in namedgroups]):
                if not all(['year' in namedgroups, 'month' in namedgroups, 'day' in namedgroups]):
                    raise ConfigValueError(
                        "Date-based regex must contain groups 'year', 'month' and 'day'")

                episodenumbers = [datetime.date(handleYear(match.group('year')),
                                                int(match.group('month')),
                                                int(match.group('day')))]
                extra_values["year"] = episodenumbers[0].year
                extra_values["month"] = episodenumbers[0].month
                extra_values["day"] = episodenumbers[0].day

                fmt_keys = {"epname": "filename_with_date_and_episode", "noepname": "filename_with_date_without_episode"}

            else:
                raise ConfigValueError(
                    "Regex does not contain episode number group, should"
                    "contain episodenumber, episodenumber1-9, or"
                    "episodenumberstart and episodenumberend\n\nPattern"
                    "was:\n" + cmatcher.pattern)

            extra_values['episode'] = formatEpisodeNumbers(episodenumbers)

            if not 'seriesname' in namedgroups:
                raise ConfigValueError(
                    "Regex must contain seriesname. Pattern was:\n" + cmatcher.pattern)

            seriesname = match.group('seriesname')
            if seriesname:
                seriesname = cleanRegexedSeriesName(seriesname)
                seriesname = replaceInputSeriesName(seriesname)

            if extra_values.get('seasonnumber'):
                extra_values['seasonnumber'] = int(extra_values.get('seasonnumber'))
                # overwrite default *_no_season key
                fmt_keys = {"epname": "filename_with_episode", "noepname": "filename_without_episode"}

            if 'group' in namedgroups:
                if extra_values.get('crc'):
                    fmt_keys = {"epname": "filename_anime_with_episode", "noepname": "filename_anime_without_episode"}
                else:
                    fmt_keys = {"epname": "filename_anime_with_episode_without_crc", "noepname": "filename_anime_without_episode_without_crc"}

            return EpisodeInfo(
                    seriesname = seriesname,
                    episodenumbers = episodenumbers,
                    filename = self.path,
                    fmt_keys = fmt_keys,
                    extra = extra_values)

        # body of for loop didn't return, which means no regex matches the filename
        else:
            emsg = "Cannot parse %r" % self.path
            if len(Config['input_filename_replacements']) > 0:
                emsg += " with replacements: %r" % filename
            raise InvalidFilename(emsg)


class EpisodeInfo(object):
    """Stores information (season, episode number, episode name), and contains
    logic to generate new name
    """

    _fullpath = str
    filename = str
    extension = str

    def __init__(self, filename, episodenumbers, fmt_keys, extra=None, **kwargs):
        self.fullpath = filename
        self.episodenumbers = episodenumbers
        self.fmt_keys = fmt_keys

        if extra is None:
            self.extra = {}
        else:
            self.extra = extra
        self.extra.update(kwargs)

    @property
    def seasonnumber(self):
        return self.extra.get('seasonnumber')

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

    @property
    def seriesname(self):
        return self.extra.get('seriesname')
    @property
    def episodename(self):
        return self.extra.get('episodename')

    def sortable_info(self):
        """Returns a list of sortable information
        """
        info = []
        info.append(self.extra['seriesname'])
        if self.extra.get('seasonnumber'):
            info.append(self.extra['seasonnumber'])
        info.append(self.episodenumbers)
        return info

    def number_string(self):
        """Used in UI
        """
        string = ""
        if self.extra.get('seasonnumber'):
            string += "season: %s, " % self.extra['seasonnumber']
        string += "episode: %s" % ", ".join([str(x) for x in self.episodenumbers])
        return string

    def is_dated_episode(self):
        return self.fmt_keys["epname"].startswith("filename_with_date_")

    def populateFromTvdb(self, tvdb_instance, force_name=None, series_id=None):
        """Queries the tvdb_api.Tvdb instance for episode name and corrected
        series name.
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

        if self.is_dated_episode():
            # Date-based episode
            epnames = []
            for cepno in self.episodenumbers:
                try:
                    sr = show.airedOn(cepno)
                    if len(sr) > 1:
                        raise EpisodeNotFound(
                            "Ambigious air date %s, there were %s episodes on that day" % (
                            cepno, len(sr)))
                    epnames.append(sr[0]['episodename'])
                except tvdb_episodenotfound:
                    raise EpisodeNotFound(
                        "Episode that aired on %s could not be found" % cepno)
            self.extra['episodename'] = epnames
            return

        # Default to 1, series without concept of seasons have all episodes in season 1
        seasonnumber = self.extra.get('seasonnumber') or 1

        epnames = []
        for cepno in self.episodenumbers:
            try:
                episodeinfo = show[seasonnumber][cepno]

            except tvdb_seasonnotfound:
                raise SeasonNotFound(
                    "Season %s of show %s could not be found" % (
                    seasonnumber,
                    self.extra['seriesname']))

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
                        raise EpisodeNotFound(
                            "No episode actually matches %s, found %s results instead" % (cepno, len(sr)))
                elif len(sr) == 1:
                    epnames.append(sr[0]['episodename'])
                else:
                    raise EpisodeNotFound(
                        "Episode %s of show %s, season %s could not be found (also tried searching by absolute episode number)" % (
                            cepno,
                            self.extra['seriesname'],
                            seasonnumber))

            except tvdb_attributenotfound:
                raise EpisodeNameNotFound(
                    "Could not find episode name for %s" % cepno)
            else:
                epnames.append(episodeinfo['episodename'])

        self.extra['episodename'] = epnames

    def getepdata(self):
        """ Made data available to config'd output file format
        """

        epdata = self.extra.copy()
        epdata.update({
            'originalfilename': self.fullfilename,
            'ext': self.extension,
            'episode': formatEpisodeNumbers(self.episodenumbers),    # test_name_generation.py relies on calling this from getepdata(), normally 'episode' is already formatted
            })

        # format dynamic parts according to config
        # TODO: move this to populateFromTvdb and fix test_name_generation.py
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

        return epdata

    def generateFilename(self):
        epdata = self.getepdata()
        if self.extra.get('episodename'):
            return Config[self.fmt_keys["epname"]] % epdata
        else:
            return Config[self.fmt_keys["noepname"]] % epdata

    def __repr__(self):
        return u"<%s: %r>" % (self.__class__.__name__, self.fullfilename)
