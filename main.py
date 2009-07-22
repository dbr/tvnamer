#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""tvnamer - Automagical TV episode renamer

Uses data from www.thetvdb.com (via tvdb_api) to rename TV episode files from
"some.show.name.s01e01.blah.avi" to "Some Show Name - [01x01] - The First.avi"
"""

import os
import sys
from optparse import OptionParser

from utils import Config, FileFinder, FileParser, EpisodeInfo, Renamer, warn
from tvnamer_exceptions import (InvalidPath, NoValidFilesFoundError,
InvalidFilename, InvalidConfig)


def tvnamer(paths):
    """Main tvnamer function, takes a config and array of paths, does stuff.
    """
    valid_files = []

    for cfile in paths:
        cur = FileFinder(cfile, recursive = Config['recursive'])
        try:
            cur.checkPath()
        except InvalidPath:
            warn("Invalid path: %s" % cfile)
        else:
            valid_files.extend(cur.findFiles())

    if len(valid_files) == 0:
        raise NoValidFilesFoundError()

    # Remove duplicate files (all paths from FileFinder are absolute)
    valid_files = list(set(valid_files))

    episodes_found = []

    for cfile in valid_files:
        parser = FileParser(cfile)
        try:
            episode = parser.parse()
        except InvalidFilename:
            warn("Invalid filename %s" % cfile)
        else:
            episodes_found.append(episode)

    print episodes_found


def main():
    """Parses command line arguments, displays errors from tvnamer in terminal
    """
    opter = OptionParser()
    opter.add_option(
        "-c", "--config",
        dest="config", help = "Override the config file path")
    opter.add_option(
        "-v", "--verbose",
        default=False, dest="verbose", action="store_true",
        help="show debugging information")
    opter.add_option(
        "-r", "--recursive",
        default = False, dest="recursive", action="store_true",
        help="Descend more than one level directories supplied as arguments")

    opts, args = opter.parse_args()

    if len(args) == 0:
        opter.error("No filenames or directories supplied")

    if opts.config is not None:
        try:
            Config.loadFile(opts.config)
        except InvalidConfig:
            warn("Invalid config file %s - using default configuration")
            Config.useDefaultConfig()

    if opts.verbose:
        Config['verbose'] = True
    if opts.recursive:
        Config['recursive'] = True

    try:
        tvnamer(paths = args)
    except NoValidFilesFoundError:
        opter.error("No valid files were supplied")

if __name__ == '__main__':
    main()
