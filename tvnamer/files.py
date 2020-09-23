import os
import re
import errno
import shutil
import logging
import datetime
from typing import List, Pattern, Optional

from .config import Config
from .utils import _apply_replacements, warn, split_extension
from .data import BaseInfo, EpisodeInfo, DatedEpisodeInfo, AnimeEpisodeInfo, NoSeasonEpisodeInfo
from .tvnamer_exceptions import ConfigValueError, InvalidFilename, InvalidPath


LOG = logging.getLogger(__name__)


def _apply_replacements_input(cfile):
    # type: (str) -> str
    """Applies custom input filename replacements, wraps _apply_replacements
    """
    return _apply_replacements(cfile, Config['input_filename_replacements'])


def _apply_replacements_fullpath(cfile):
    # type: (str) -> str
    """Applies custom replacements to full path, wraps _apply_replacements
    """
    return _apply_replacements(cfile, Config['move_files_fullpath_replacements'])


def _replace_input_series_name(seriesname):
    # type: (str) -> str
    """allow specified replacements of series names

    in cases where default filenames match the wrong series,
    e.g. missing year gives wrong answer, or vice versa

    This helps the TVDB query get the right match.
    """
    for pat, replacement in Config['input_series_replacements'].items():
        if re.match(pat, seriesname, re.IGNORECASE | re.UNICODE):
            return replacement
    return seriesname


def intepret_year(value):
    # type: (str) -> int
    """Handle two-digit years with heuristic-ish guessing

    Assumes 50-99 becomes 1950-1999, and 0-49 becomes 2000-2049

    ..might need to rewrite this function in 2050, but that seems like
    a reasonable limitation
    """

    year = int(value)

    # No need to guess with 4-digit years
    if year > 999:
        return year

    if year < 50:
        return 2000 + year
    else:
        return 1900 + year


def _clean_extracted_series_name(seriesname):
    # type: (str) -> str
    """Cleans up series name by removing any . and _
    characters, along with any trailing hyphens.

    Is basically equivalent to replacing all _ and . with a
    space, but handles decimal numbers in string, for example:

    >>> _clean_extracted_series_name("an.example.1.0.test")
    'an example 1.0 test'
    >>> _clean_extracted_series_name("an_example_1.0_test")
    'an example 1.0 test'
    """
    # TODO: Could this be made to clean "Hawaii.Five-0.2010" into "Hawaii Five-0 2010"?
    seriesname = re.sub(r"(\D)[.](\D)", "\\1 \\2", seriesname)
    seriesname = re.sub(r"(\D)[.]", "\\1 ", seriesname)
    seriesname = re.sub(r"[.](\D)", " \\1", seriesname)
    seriesname = seriesname.replace("_", " ")
    seriesname = re.sub("-$", "", seriesname)
    return seriesname.strip()


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

    def __init__(
        self, path, with_extension=None, filename_blacklist=None, recursive=False
    ):
        # type: (str, Optional[List[str]], Optional[List[str]], bool) -> None
        self.path = path
        if with_extension is None:
            self.with_extension = [] # type: List[str]
        else:
            self.with_extension = with_extension
        if filename_blacklist is None:
            self.with_blacklist = []
        else:
            self.with_blacklist = filename_blacklist
        self.recursive = recursive

    def find_files(self):
        # type: () -> List[str]
        """Returns list of files found at path
        """
        if os.path.isfile(self.path):
            path = os.path.abspath(self.path)
            if self._check_extension(path) and not self._blacklisted_filename(path):
                return [path]
            else:
                return []
        elif os.path.isdir(self.path):
            return self._find_files_in_path(self.path)
        else:
            raise InvalidPath("%s is not a valid file/directory" % self.path)

    def _check_extension(self, fname):
        # type: (str) -> bool
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

    def _blacklisted_filename(self, filepath):
        # type: (str) -> bool
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
            if isinstance(fblacklist, str):
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

    def _find_files_in_path(self, startpath):
        # type: (str) -> List[str]
        """Finds files from startpath, could be called recursively
        """
        allfiles = [] # type: List[str]
        if not os.access(startpath, os.R_OK):
            LOG.info("Skipping inaccessible path %s" % startpath)
            return allfiles

        for subf in os.listdir(startpath):
            newpath = os.path.join(startpath, subf)
            newpath = os.path.abspath(newpath)
            if os.path.isfile(newpath):
                if not self._check_extension(subf):
                    continue
                elif self._blacklisted_filename(subf):
                    continue
                else:
                    allfiles.append(newpath)
            else:
                if self.recursive:
                    allfiles.extend(self._find_files_in_path(newpath))
                # end if recursive
            # end if isfile
        # end for sf
        return allfiles


class FileParser(object):
    """Deals with parsing of filenames
    """

    def __init__(self, path):
        # type: (str) -> None
        self.path = path
        self.compiled_regexs = [] # type: List[Pattern]
        self._compile_regexs()

    def _compile_regexs(self):
        # type: () -> None
        """Takes episode_patterns from config, compiles them all
        into self.compiled_regexs
        """
        for cpattern in Config['filename_patterns']:
            try:
                cregex = re.compile(cpattern, re.VERBOSE)
            except re.error as errormsg:
                warn(
                    "WARNING: Invalid episode_pattern (error: %s)\nPattern:\n%s"
                    % (errormsg, cpattern)
                )
            else:
                self.compiled_regexs.append(cregex)

    def parse(self):
        # type: () -> BaseInfo
        """Runs path via configured regex, extracting data from groups.
        Returns an EpisodeInfo instance containing extracted data.
        """
        _, filename = os.path.split(self.path)

        filename = _apply_replacements_input(filename)

        for cmatcher in self.compiled_regexs:
            match = cmatcher.match(filename)
            if match:
                namedgroups = match.groupdict().keys()

                if 'episodenumber1' in namedgroups:
                    # Multiple episodes, have episodenumber1 or 2 etc
                    epnos = []
                    for cur in namedgroups:
                        epnomatch = re.match(r'episodenumber(\d+)', cur)
                        if epnomatch:
                            epnos.append(int(match.group(cur)))
                    epnos.sort()
                    episodenumbers = epnos # type: List[int]

                elif 'episodenumberstart' in namedgroups:
                    # Multiple episodes, regex specifies start and end number
                    start = int(match.group('episodenumberstart'))
                    end = int(match.group('episodenumberend'))
                    if end - start > 5:
                        warn(
                            "WARNING: %s episodes detected in file: %s, confused by numeric episode name, using first match: %s"
                            % (end - start, filename, start)
                        )
                        episodenumbers = [start]
                    elif start > end:
                        # Swap start and end
                        start, end = end, start
                        episodenumbers = list(range(start, end + 1))
                    else:
                        episodenumbers = list(range(start, end + 1))

                elif 'episodenumber' in namedgroups:
                    episodenumbers = [
                        int(match.group('episodenumber')),
                    ]

                elif (
                    'year' in namedgroups
                    or 'month' in namedgroups
                    or 'day' in namedgroups
                ):
                    if not all(
                        [
                            'year' in namedgroups,
                            'month' in namedgroups,
                            'day' in namedgroups,
                        ]
                    ):
                        raise ConfigValueError(
                            "Date-based regex must contain groups 'year', 'month' and 'day'"
                        )
                    match.group('year')

                    year = intepret_year(match.group('year'))

                    episodedates = [
                        datetime.date(
                            year, int(match.group('month')), int(match.group('day'))
                        )
                    ]

                else:
                    raise ConfigValueError(
                        "Regex does not contain episode number group, should"
                        "contain episodenumber, episodenumber1-9, or"
                        "episodenumberstart and episodenumberend\n\nPattern"
                        "was:\n" + cmatcher.pattern
                    )

                if 'seriesname' in namedgroups:
                    seriesname = match.group('seriesname')
                else:
                    raise ConfigValueError(
                        "Regex must contain seriesname. Pattern was:\n"
                        + cmatcher.pattern
                    )

                if seriesname is not None:
                    seriesname = _clean_extracted_series_name(seriesname)
                    seriesname = _replace_input_series_name(seriesname)

                extra_values = match.groupdict()

                if 'seasonnumber' in namedgroups:
                    seasonnumber = int(match.group('seasonnumber'))

                    episode = EpisodeInfo(
                        seriesname=seriesname,
                        seasonnumber=seasonnumber,
                        episodenumbers=episodenumbers,
                        filename=self.path,
                        extra=extra_values,
                    ) # type: BaseInfo
                elif (
                    'year' in namedgroups
                    and 'month' in namedgroups
                    and 'day' in namedgroups
                ):
                    episode = DatedEpisodeInfo(
                        seriesname=seriesname,
                        episodenumbers=episodedates, # FIXME: Refactor so this is defined closer to here, prone to name not defined error
                        filename=self.path,
                        extra=extra_values,
                    )
                elif 'group' in namedgroups:
                    episode = AnimeEpisodeInfo(
                        seriesname=seriesname,
                        episodenumbers=episodenumbers,
                        filename=self.path,
                        extra=extra_values,
                    )
                else:
                    # No season number specified, usually for Anime
                    episode = NoSeasonEpisodeInfo(
                        seriesname=seriesname,
                        episodenumbers=episodenumbers,
                        filename=self.path,
                        extra=extra_values,
                    )

                return episode
        else:
            emsg = "Cannot parse %r" % self.path
            if len(Config['input_filename_replacements']) > 0:
                emsg += " with replacements: %r" % filename
            raise InvalidFilename(emsg)


def rename_file(old, new):
    # type: (str, str) -> None
    print("rename %s to %s" % (old, new))
    stat = os.stat(old)
    shutil.move(old, new)
    try:
        os.utime(new, (stat.st_atime, stat.st_mtime))
    except OSError as ex:
        if ex.errno == errno.EPERM:
            warn(
                "WARNING: Could not preserve times for %s "
                "(owner UID mismatch?)" % new
            )
        else:
            raise


def copy_file(old, new):
    # type: (str, str) -> None
    print("copy %s to %s" % (old, new))
    shutil.copyfile(old, new)
    shutil.copystat(old, new)


def symlink_file(target, name):
    # type: (str, str) -> None
    print("symlink %s to %s" % (name, target))
    os.symlink(target, name)


class Renamer(object):
    """Deals with renaming of files
    """

    def __init__(self, filename):
        # type: (str) -> None
        self.filename = os.path.abspath(filename)

    def new_path(
        self,
        new_path=None, # type: Optional[str]
        new_fullpath=None, # type: Optional[str]
        force=False, # type: bool
        always_copy=False, # type: bool
        always_move=False, # type: bool
        leave_symlink=False, # type: bool
        get_path_preview=False, # type: bool
    ):
        # type: (...) -> Optional[str]
        """Moves the file to a new path.

        If it is on the same partition, it will be moved (unless always_copy is True)
        If it is on a different partition, it will be copied, and the original
        only deleted if always_move is True.
        If the target file already exists, it will raise OSError unless force is True.
        If it was moved, a symlink will be left behind with the original name
        pointing to the file's new destination if leave_symlink is True.
        """

        if always_copy and always_move:
            raise ValueError("Both always_copy and always_move cannot be specified")

        if (new_path is None and new_fullpath is None) or (
            new_path is not None and new_fullpath is not None
        ):
            raise ValueError("Specify only new_dir or new_fullpath")

        old_dir, old_filename = os.path.split(self.filename)
        if new_path is not None:
            # Join new filepath to old one (to handle realtive dirs)
            new_dir = os.path.abspath(os.path.join(old_dir, new_path))

            # Join new filename onto new filepath
            new_fullpath = os.path.join(new_dir, old_filename)

        else:
            # Join new filepath to old one (to handle realtive dirs)
            new_fullpath = os.path.abspath(os.path.join(old_dir, new_fullpath))

            new_dir = os.path.dirname(new_fullpath)

        if len(Config['move_files_fullpath_replacements']) > 0:
            print("Before custom full path replacements: %s" % (new_fullpath))
            new_fullpath = _apply_replacements_fullpath(new_fullpath)
            new_dir = os.path.dirname(new_fullpath)

        print("New path: %s" % new_fullpath)

        if get_path_preview:
            return new_fullpath

        if not os.path.exists(new_dir):
            os.makedirs(new_dir, exist_ok=True)
            print("Created directory %s" % new_dir)

        if os.path.isfile(new_fullpath):
            # If the destination exists, raise exception unless force is True
            if not force:
                raise OSError(
                    "File %s already exists, not forcefully moving %s"
                    % (new_fullpath, self.filename)
                )

        if always_copy:
            # Same partition, but forced to copy
            copy_file(self.filename, new_fullpath)
        else:
            # Same partition, just rename the file to move it
            rename_file(self.filename, new_fullpath)

            # Leave a symlink behind if configured to do so
            if leave_symlink:
                symlink_file(new_fullpath, self.filename)

        self.filename = new_fullpath

        return None # TODO: Remove get_path_preview argument