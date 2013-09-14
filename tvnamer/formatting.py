#!/usr/bin/env python

import os
import re
import logging
import platform
import datetime

from unicode_helper import p
from config import Config


__all__ = ['makeValidFilename', 'formatEpisodeNames', 'formatEpisodeNumbers']


def log():
    """Returns the logger for current file
    """
    return logging.getLogger(__name__)


def _makeValidFilename(value, normalize_unicode=False, windows_safe=False, custom_blacklist=None, replace_with="_"):
    """
    Takes a string and makes it into a valid filename.

    normalize_unicode replaces accented characters with ASCII equivalent, and
    removes characters that cannot be converted sensibly to ASCII.

    windows_safe forces Windows-safe filenames, regardless of current platform

    custom_blacklist specifies additional characters that will removed. This
    will not touch the extension separator:

        >>> makeValidFilename("T.est.avi", custom_blacklist=".")
        'T_est.avi'
    """

    if windows_safe:
        # Allow user to make Windows-safe filenames, if they so choose
        sysname = "Windows"
    else:
        sysname = platform.system()

    # If the filename starts with a . prepend it with an underscore, so it
    # doesn't become hidden.

    # This is done before calling splitext to handle filename of ".", as
    # splitext acts differently in python 2.5 and 2.6 - 2.5 returns ('', '.')
    # and 2.6 returns ('.', ''), so rather than special case '.', this
    # special-cases all files starting with "." equally (since dotfiles have
    # no extension)
    if value.startswith("."):
        value = "_" + value

    # Treat extension seperatly
    value, extension = os.path.splitext(value)

    # Remove any null bytes
    value = value.replace("\0", "")

    # Blacklist of characters
    if sysname == 'Darwin':
        # : is technically allowed, but Finder will treat it as / and will
        # generally cause weird behaviour, so treat it as invalid.
        blacklist = r"/:"
    elif sysname in ['Linux', 'FreeBSD']:
        blacklist = r"/"
    else:
        # platform.system docs say it could also return "Windows" or "Java".
        # Failsafe and use Windows sanitisation for Java, as it could be any
        # operating system.
        blacklist = r"\/:*?\"<>|"

    # Append custom blacklisted characters
    if custom_blacklist is not None:
        blacklist += custom_blacklist

    # Replace every blacklisted character with a underscore
    value = re.sub("[%s]" % re.escape(blacklist), replace_with, value)

    # Remove any trailing whitespace
    value = value.strip()

    # There are a bunch of filenames that are not allowed on Windows.
    # As with character blacklist, treat non Darwin/Linux platforms as Windows
    if sysname not in ['Darwin', 'Linux']:
        invalid_filenames = [
            "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5",
            "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4",
            "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]
        if value in invalid_filenames:
            value = "_" + value

    # Replace accented characters with ASCII equivalent
    if normalize_unicode:
        import unicodedata
        value = unicode(value)  # cast data to unicode
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')

    # Truncate filenames to valid/sane length.
    # NTFS is limited to 255 characters, HFS+ and EXT3 don't seem to have
    # limits, FAT32 is 254. I doubt anyone will take issue with losing that
    # one possible character, and files over 254 are pointlessly unweidly
    max_len = 254

    if len(value + extension) > max_len:
        if len(extension) > len(value):
            # Truncate extension instead of filename, no extension should be
            # this long..
            new_length = max_len - len(value)
            extension = extension[:new_length]
        else:
            # File name is longer than extension, truncate filename.
            new_length = max_len - len(extension)
            value = value[:new_length]

    return value + extension


def makeValidFilename(fname):
    """ Wraps the _makeValidFilename() function, loads arguments from config.
    """
    return _makeValidFilename(
        fname,
        normalize_unicode=Config['normalize_unicode_filenames'],
        windows_safe=Config['windows_safe_filenames'],
        custom_blacklist=Config['custom_filename_character_blacklist'],
        replace_with=Config['replace_invalid_characters_with'])


def formatEpisodeNames(names):
    """
    Takes a list of episode names, formats them into a string.
    If argument is not a list, it is returned as is.

    If two names are supplied, such as "Pilot (1)" and "Pilot (2)", the
    returned string will be "Pilot (1-2)". Note that the first number
    is not required, for example passing "Pilot" and "Pilot (2)" will
    also result in returning "Pilot (1-2)".

    If two different episode names are found, such as "The first", and
    "Something else" it will return "The first, Something else"
    """

    if not isinstance(names, list):
        return names
    if len(names) == 1:
        return names[0]

    join_with = Config['multiep_join_name_with']
    multiep_format = Config['multiep_format']

    found_name = ""
    numbers = []
    for cname in names:
        match = re.match("(.*) \(([0-9]+)\)$", cname)
        if found_name != "" and not match:
            # An episode didn't match
            return join_with.join(names)

        if match:
            epname, epno = match.group(1), match.group(2)
        else:   # assume that this is the first episode, without number
            epname = cname
            epno = 1
        found_name = epname
        numbers.append(int(epno))

    return multiep_format % {'epname': found_name, 'episodemin': min(numbers), 'episodemax': max(numbers)}


def formatEpisodeNumbers(episodenumbers):
    """Format episode number(s) into string, using configured values
    """
    if len(episodenumbers) == 1:
        if isinstance(episodenumbers[0], datetime.date):
            # format dated episode
            epno = str(episodenumbers[0])
        else:
            # format normal episode
            epno = Config['episode_single'] % episodenumbers[0]
    else:
        epno = Config['episode_separator'].join(
            Config['episode_single'] % x for x in episodenumbers)

    return epno
