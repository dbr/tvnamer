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

import sys
from optparse import OptionParser
import tvdb_api
from utils import ConfigManager, FileFinder, FileParser, EpisodeInfo, Renamer


class InvalidPath(Exception):
    """Raised when an argument is a non-existent file or directory path
    """
    pass


class NoValidFilesFoundError(Exception):
    """Raised when no valid files are found. Effectively exits tvnamer
    """


def warn(text):
    sys.stderr.write("%s\n" % text)


def tvnamer(config, paths):
    """Main tvnamer function, takes a config and array of paths, does stuff.
    """
    valid_paths = []

    for cfile in paths:
        cur = FileFinder(cfile, recursive = config.recursive)
        try:
            cur.findFiles()
        except InvalidPath:
            warn("Invalid path: %s" % cfile)
        else:
            valid_paths.append(cur)

    if len(valid_paths) == 0:
        raise NoValidFilesFoundError()


def main():
    """Parsers command line arguments, displays errors from tvnamer in terminal
    """
    opter = OptionParser()
    opter.add_option(
        "-v", "--verbose",
        default=False, dest="verbose", action="store_true",
        help="show debugging information")
    opter.add_option(
        "-r", "--recursive",
        default = False, dest="recursive", action="store_true"
        help="Descend more than one level directories supplied as arguments")

    opts, args = opter.parse_args()

    if len(args) == 0:
        opter.error("No filenames or directories supplied")

    config = ConfigManager()
    if opts.verbose:
        config['verbose'] = True

    tvnamer(config, paths = args)

if __name__ == '__main__':
    main()
