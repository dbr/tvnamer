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

from utils import Config, FileFinder, FileParser, EpisodeInfo, Renamer
from tvnamer_exceptions import InvalidPath, NoValidFilesFoundError


def warn(text):
    """Displays message to sys.stdout
    """
    sys.stderr.write("%s\n" % text)


def tvnamer(config, paths):
    """Main tvnamer function, takes a config and array of paths, does stuff.
    """
    valid_paths = []

    for cfile in paths:
        cur = FileFinder(cfile, recursive = config['recursive'])
        try:
            cur.checkPath()
        except InvalidPath:
            warn("Invalid path: %s" % cfile)
        else:
            valid_paths.append(cur)

    if len(valid_paths) == 0:
        raise NoValidFilesFoundError()

    valid_files = []

    for cfinder in valid_paths:
        if os.path.isdir(cfinder.path):
            print "Processing directory \"%s\"" % (cfinder.path)
        valid_files.extend(cfinder.findFiles())

    for cfile in valid_files:
        parser = FileParser(cfile)
        print parser.parse()


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
        default = False, dest="recursive", action="store_true",
        help="Descend more than one level directories supplied as arguments")

    opts, args = opter.parse_args()

    if len(args) == 0:
        opter.error("No filenames or directories supplied")

    if opts.verbose:
        Config['verbose'] = True
    if opts.recursive:
        Config['recursive'] = True

    try:
        tvnamer(Config, paths = args)
    except NoValidFilesFoundError:
        opter.error("No valid files were supplied")

if __name__ == '__main__':
    main()
