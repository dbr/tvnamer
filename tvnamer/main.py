#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Main tvnamer utility functionality
"""

import os

import simplejson as json
from tvdb_api import Tvdb

import cliarg_parser
from config_defaults import defaults
from utils import (Config, FileFinder, FileParser, Renamer, warn,
getEpisodeName, applyCustomInputReplacements, applyCustomOutputReplacements)

from tvnamer_exceptions import (ShowNotFound, SeasonNotFound, EpisodeNotFound,
EpisodeNameNotFound, UserAbort, InvalidPath, NoValidFilesFoundError,
InvalidFilename, DataRetrievalError)


def processFile(tvdb_instance, episode):
    """Gets episode name, prompts user for input
    """
    print "#" * 20
    print "# Processing file: %s" % episode.fullfilename

    if len(Config['input_filename_replacements']) > 0:
        replaced = applyCustomInputReplacements(episode.fullfilename)
        print "# With custom replacements: %s" % (replaced)

    print "# Detected series: %s (season: %s, episode: %s)" % (
        episode.seriesname,
        episode.seasonnumber,
        ", ".join([str(x) for x in episode.episodenumbers]))

    try:
        correctedSeriesName, epName = getEpisodeName(tvdb_instance, episode)
    except (DataRetrievalError, ShowNotFound), errormsg:
        if Config['always_rename'] and Config['skip_file_on_error'] is True:
            warn("Skipping file due to error: %s" % errormsg)
            return
        else:
            warn(errormsg)
    except (SeasonNotFound, EpisodeNotFound, EpisodeNameNotFound), errormsg:
        # Show was found, so use corrected series name
        if Config['always_rename'] and Config['skip_file_on_error'] is True:
            warn("Skipping file due to error: %s" % errormsg)
            return

        warn(errormsg)
        episode.seriesname = correctedSeriesName
    else:
        episode.seriesname = correctedSeriesName
        episode.episodename = epName

    cnamer = Renamer(episode.fullpath)
    newName = episode.generateFilename()

    print "#" * 20
    print "Old filename: %s" % episode.fullfilename

    if len(Config['output_filename_replacements']):
        print "Before custom output replacements: %s" % (newName)
        # Only apply to filename, not extension
        newName, newExt = os.path.splitext(newName)
        newName = applyCustomOutputReplacements(newName)
        newName = newName + newExt

    print "New filename: %s" % newName

    if Config['always_rename']:
        try:
            cnamer.newName(newName)
        except OSError, e:
            warn(e)
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

    shouldRename = False
    if len(ans) == 0:
        print "Renaming (default)"
        shouldRename = True
    elif ans == "a":
        print "Always renaming"
        Config['always_rename'] = True
        shouldRename = True
    elif ans == "q":
        print "Quitting"
        raise UserAbort("User exited with q")
    elif ans == "y":
        print "Renaming"
        shouldRename = True
    elif ans == "n":
        print "Skipping"
    else:
        print "Invalid input, skipping"

    if shouldRename:
        try:
            cnamer.newName(newName)
        except OSError, e:
            warn(e)


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
    print "#" * 20
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

    if len(episodes_found) == 0:
        raise NoValidFilesFoundError()

    print "# Found %d episodes" % len(episodes_found)

    tvdb_instance = Tvdb(
        interactive=not Config['select_first'],
        debug = Config['verbose'],
        search_all_languages = Config['search_all_languages'],
        language = Config['language'])

    for episode in episodes_found:
        processFile(tvdb_instance, episode)
        print

    print "#" * 20
    print "# Done"


def main():
    """Parses command line arguments, displays errors from tvnamer in terminal
    """
    opter = cliarg_parser.getCommandlineParser(defaults)

    opts, args = opter.parse_args()

    # If a config is specified, load it, update the defaults using the loaded
    # values, then reparse the options with the updated defaults.
    default_configuration = os.path.expanduser("~/.tvnamer.json")

    if opts.loadconfig is not None:
        # Command line overrides loading ~/.tvnamer.json
        configToLoad = opts.loadconfig
    elif os.path.isfile(default_configuration):
        # No --config arg, so load default config if it exists
        configToLoad = default_configuration
    else:
        # No arg, nothing at default config location, don't load anything
        configToLoad = None

    if configToLoad is not None:
        print "Loading config: %s" % (configToLoad)
        try:
            loadedConfig = json.load(open(configToLoad))
        except ValueError, e:
            print "Error loading config: %s" % e
            opter.exit(1)
        else:
            # Config loaded, update optparser's defaults and reparse
            defaults.update(loadedConfig)
            opter = cliarg_parser.getCommandlineParser(defaults)
            opts, args = opter.parse_args()

    # Save config argument
    if opts.saveconfig is not None:
        print "Saving config: %s" % (opts.saveconfig)
        json.dump(
            opts.__dict__,
            open(opts.saveconfig, "w+"),
            sort_keys=True,
            indent=4)

        opter.exit(0)

    # Show config argument
    if opts.showconfig:
        for k, v in opts.__dict__.items():
            print k, "=", str(v)[:20]
        return

    # Process values
    if opts.batch:
        opts.select_first = True
        opts.always_rename = True

    # Update global config object
    Config.update(opts.__dict__)

    if len(args) == 0:
        opter.error("No filenames or directories supplied")

    try:
        tvnamer(paths = sorted(args))
    except NoValidFilesFoundError:
        opter.error("No valid files were supplied")
    except UserAbort, errormsg:
        opter.error(errormsg)

if __name__ == '__main__':
    main()
