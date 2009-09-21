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

from optparse import OptionParser

from tvdb_api import Tvdb

from utils import (Config, FileFinder, FileParser, Renamer, warn,
getEpisodeName)
from tvnamer_exceptions import (InvalidPath, NoValidFilesFoundError,
InvalidFilename, InvalidConfigFile, UserAbort)


def processFile(tvdb_instance, episode):
    """Gets episode name, prompts user for input
    """
    print "# Processing %s" % (episode.filename)
    episode = getEpisodeName(tvdb_instance, episode)

    cnamer = Renamer(episode.fullpath)
    newName = episode.generateFilename()

    print "#" * 20
    print "# Old filename: %s" % episode.filename
    print "# New filename: %s" % newName

    if Config['alwaysrename']:
        cnamer.newName(newName)
        return

    ans = None
    while ans not in ['y', 'n', 'a', 'q', '']:
        print "Rename?"
        print "([y]/n/a/q)",
        try:
            ans = raw_input().strip()
        except KeyboardInterrupt, errormsg:
            print "\n", errormsg
            raise UserAbort(errormsg)

    if len(ans) == 0:
        print "Renaming (default)"
        cnamer.newName(newName)
    elif ans == "a":
        print "Always renaming"
        Config['alwaysrename'] = True
        cnamer.newName(newName)
    elif ans == "q":
        print "Quitting"
        raise UserAbort("User exited with q")
    elif ans == "y":
        print "Renaming"
        cnamer.newName(newName)
    elif ans == "n":
        print "Skipping"
    else:
        print "Invalid input, skipping"


def findFiles(paths):
    """Takes an array of paths, returns all files found
    """
    valid_files = []

    for cfile in paths:
        cur = FileFinder(cfile, recursive = Config['recursive'])
        try:
            valid_files.extend(cur.findFiles())
        except InvalidPath:
            warn("Invalid path: %s" % cfile)

    if len(valid_files) == 0:
        raise NoValidFilesFoundError()

    # Remove duplicate files (all paths from FileFinder are absolute)
    valid_files = list(set(valid_files))

    return valid_files


def tvnamer(paths):
    """Main tvnamer function, takes an array of paths, does stuff.
    """
    print "####################"
    print "# Starting tvnamer"

    episodes_found = []

    for cfile in findFiles(paths):
        parser = FileParser(cfile)
        try:
            episode = parser.parse()
        except InvalidFilename:
            warn("Invalid filename %s" % cfile)
        else:
            episodes_found.append(episode)

    if len(valid_files) == 0:
        raise NoValidFilesFoundError()

    print "# Found %d episodes" % len(valid_files)

    tvdb_instance = Tvdb(interactive=True, debug = Config['verbose'])

    for episode in episodes_found:
        processFile(tvdb_instance, episode)

    print "# Done"


def main():
    """Parses command line arguments, displays errors from tvnamer in terminal
    """
    opter = OptionParser()
    opter.add_option(
        "-c", "--config",
        dest="config", help = "Override the config file path")
    opter.add_option(
        "-s", "--save",
        dest="saveconfig", help = "Save (default) config to file")

    opter.add_option(
        "-v", "--verbose",
        default=False, dest="verbose", action="store_true",
        help="show debugging information")
    opter.add_option(
        "-r", "--recursive",
        default = False, dest="recursive", action="store_true",
        help="Descend more than one level directories supplied as arguments")
    opter.add_option(
        "-a", "--always",
        default = False, dest="always", action="store_true",
        help="always renames files (but still prompts for correct series). Can be set at runtime with the 'a' prompt-option")


    opts, args = opter.parse_args()

    if opts.config is not None:
        print "Loading config from: %s" % (opts.config)
        try:
            Config.loadConfig(opts.config)
        except InvalidConfigFile:
            warn("Invalid config file %s - using default configuration" % (
                opts.config))
            Config.useDefaultConfig()

    if opts.saveconfig is not None:
        print "Saving current config to %s" % (opts.saveconfig)
        try:
            Config.saveConfig(opts.saveconfig)
        except InvalidConfigFile:
            opter.error("Could not save config to %s" % opts.saveconfig)
        else:
            print "Done, exiting"
            opter.exit(0)

    if opts.verbose is not None:
        Config['verbose'] = opts.verbose

    if opts.recursive is not None:
        Config['recursive'] = opts.recursive

    if opts.always is not None:
        Config['alwaysrename'] = opts.always

    if len(args) == 0:
        opter.error("No filenames or directories supplied")

    try:
        tvnamer(paths = args)
    except NoValidFilesFoundError:
        opter.error("No valid files were supplied")
    except UserAbort, errormsg:
        opter.error(errormsg)

if __name__ == '__main__':
    main()
