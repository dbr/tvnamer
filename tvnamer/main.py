#!/usr/bin/env python

"""Main tvnamer utility functionality
"""

import os
import sys
import logging
import warnings

try:
    import readline
except ImportError:
    pass

try:
    import json
except ImportError:
    import simplejson as json

from tvdb_api import Tvdb

import cliarg_parser
from config_defaults import defaults

from unicode_helper import p
from utils import (Config, FileFinder, FileParser, warn,
applyCustomInputReplacements, applyCustomOutputReplacements, applyCustomFullpathReplacements,
formatEpisodeNumbers, makeValidFilename, DatedEpisodeInfo, NoSeasonEpisodeInfo)

from tvnamer_exceptions import (ConfigValueError, ShowNotFound, SeasonNotFound, EpisodeNotFound,
EpisodeNameNotFound, UserAbort, InvalidPath, NoValidFilesFoundError,
InvalidFilename, DataRetrievalError)

from renamer import Renamer


def log():
    """Returns the logger for current file
    """
    return logging.getLogger(__name__)


def getMoveDestination(episode):
    """Constructs the location to move/copy the file
    """

    if isinstance(episode, DatedEpisodeInfo):
        path = Config['move_files_destination_date'] % {
            'seriesname': makeValidFilename(episode.seriesname),
            'year': episode.episodenumbers[0].year,
            'month': episode.episodenumbers[0].month,
            'day': episode.episodenumbers[0].day,
            'originalfilename': episode.originalfilename,
            }
    elif isinstance(episode, NoSeasonEpisodeInfo):
        path = Config['move_files_destination'] % {
            'seriesname': makeValidFilename(episode.seriesname),
            'episodenumbers': formatEpisodeNumbers(episode.episodenumbers),
            'originalfilename': episode.originalfilename,
            }
    else:
        path = Config['move_files_destination'] % {
            'seriesname': makeValidFilename(episode.seriesname),
            'seasonnumber': episode.seasonnumber,
            'episodenumbers': formatEpisodeNumbers(episode.episodenumbers),
            'originalfilename': episode.originalfilename,
            }
    return path


def confirm(question, options, default = "y"):
    """Takes a question (string), list of options and a default value (used
    when user simply hits enter).
    Asks until valid option is entered.
    """

    # Highlight default option with [ ]
    options_str = []
    for x in options:
        if x == default:
            x = "[%s]" % x
        if x != '':
            options_str.append(x)
    options_str = "/".join(options_str)

    while True:
        p(question)
        p("(%s) " % (options_str), end="")
        try:
            ans = raw_input().strip()
        except KeyboardInterrupt, errormsg:
            p("\n", errormsg)
            raise UserAbort(errormsg)

        if ans in options:
            return ans
        elif ans == '':
            return default


# TODO: function is too long, split interaction with user from filename generation and renaming
# TODO: p() function is really horrible, write simple logger with log levels
def processFile(tvdb_instance, episode):
    """Gets episode name, prompts user for input
    """

    p("#" * 20)
    p("# Processing file: %s" % episode.fullfilename)

    if len(Config['input_filename_replacements']) > 0:
        replaced = applyCustomInputReplacements(episode.fullfilename)
        p("# With custom replacements: %s" % (replaced))

    # Use force_name option. Done after input_filename_replacements so
    # it can be used to skip the replacements easily
    if Config['force_name'] is not None:
        episode.seriesname = Config['force_name']

    p("# Detected series: %s (%s)" % (episode.seriesname, episode.number_string()))

    try:
        episode.populateFromTvdb(tvdb_instance, force_name=Config['force_name'], series_id=Config['series_id'])
    except (DataRetrievalError, ShowNotFound, SeasonNotFound, EpisodeNotFound, EpisodeNameNotFound), errormsg:
        # Show was found, so use corrected series name
        if Config['batch'] and Config['skip_file_on_error']:
            warn("Skipping file due to error: %s" % errormsg)
            return
        warn(errormsg)

    cnamer = Renamer(episode.fullpath)

    # set defaults
    newPath, newName = os.path.split(episode.fullpath)
    overwrite = Config['overwrite_destination_on_rename']

    if not Config["move_files_only"]:
        p("#" * 20)
        p("Original filename: %s" % newName)
        newName = episode.generateFilename()

        if len(Config['output_filename_replacements']) > 0:
            p("Before custom output replacements: %s" % newName)
            newName = applyCustomOutputReplacements(newName)
            p("After custom output replacements: %s" % newName)

    if Config['move_files_enable']:
        p("Old path: %s" % newPath)
        overwrite = Config['overwrite_destination_on_move']
        newPath = getMoveDestination(episode)
        if Config['move_files_destination_is_filepath']:
            newPath, newName = os.path.split(newPath)
        p("New path: %s" % newPath)

    # make newName and newPath lowercase if specified in config
    if Config['lowercase_filename']:
        newName = newName.lower()
    if Config['move_files_lowercase_destination']:
        newName = newName.lower()   # move_files_destination can be filename, so this is _really_ necessary
        newPath = newPath.lower()

# TODO: run makeValidFilename also on newPath, but make _absolutely_ sure it doesn't conflict with
#       existing paths and paths specified in move_files_destination
    # make sure the filename is valid
    newName = makeValidFilename(newName)

    # join final filename
    newFullPath = os.path.join(newPath, newName)

    # Join new filepath to old one (to handle realtive dirs)
    old_dir = os.path.dirname(episode.fullpath)
    newFullPath = os.path.abspath(os.path.join(old_dir, newFullPath))

    # apply full-path replacements
    if len(Config['move_files_fullpath_replacements']) > 0:
        p("Before custom full path replacements: %s" % (newFullPath))
        newFullPath = applyCustomFullpathReplacements(newFullPath)

    # don't do anything if filename was not changed
    if newFullPath == episode.fullpath:
        p("#" * 20)
        p("Existing filename is correct: %s" % episode.fullfilename)
        p("#" * 20)
        return

    p("Final filename: %s" % newFullPath)

    if not Config['batch'] and Config['move_files_confirmation']:
        ans = confirm("Move file?", options = ['y', 'n', 'a', 'q'], default = 'y')
        if ans == "a":
            p("Always moving files")
            Config['move_files_confirmation'] = False
        elif ans == "q":
            p("Quitting")
            raise UserAbort("User exited with q")
        elif ans == "y":
            p("Renaming")
        elif ans == "n":
            p("Skipping")
            return
        else:
            p("Invalid input, skipping")
            return

    # finally move file
    try:
        cnamer.rename(
            new_fullpath = newFullPath,
            always_move = Config['always_move'],
            always_copy = Config['always_copy'],
            leave_symlink = Config['leave_symlink'],
            force = overwrite)
    except OSError, e:
        warn(e)


def findFiles(paths):
    """Takes an array of paths, returns all files found
    """

    valid_files = []

    for cfile in paths:
        cur = FileFinder(
            cfile,
            with_extension = Config['valid_extensions'],
            filename_blacklist = Config["filename_blacklist"],
            recursive = Config['recursive'])

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

    p("#" * 20)
    p("# Starting tvnamer")

    episodes_found = []

    for cfile in findFiles(paths):
        parser = FileParser(cfile)
        try:
            episode = parser.parse()
        except InvalidFilename, e:
            warn("Invalid filename: %s" % e)
        else:
            if episode.seriesname is None and Config['force_name'] is None and Config['series_id'] is None:
                warn("Parsed filename did not contain series name (and --name or --series-id not specified), skipping: %s" % cfile)

            else:
                episodes_found.append(episode)

    if len(episodes_found) == 0:
        raise NoValidFilesFoundError()

    p("# Found %d episode" % len(episodes_found) + ("s" * (len(episodes_found) > 1)))

    # Sort episodes by series name, season and episode number
    episodes_found.sort(key = lambda x: x.sortable_info())

    tvdb_instance = Tvdb(
        interactive = not Config['batch'],
        search_all_languages = Config['search_all_languages'],
        language = Config['language'])

    for episode in episodes_found:
        processFile(tvdb_instance, episode)
        p('')

    p("#" * 20)
    p("# Done")


def main():
    """Parses command line arguments, displays errors from tvnamer in terminal
    """

    opter = cliarg_parser.getCommandlineParser(defaults)

    opts, args = opter.parse_args()

    if opts.verbose:
        logging.basicConfig(
            level = logging.DEBUG,
            format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    else:
        logging.basicConfig()

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
        p("Loading config: %s" % (configToLoad))
        try:
            loadedConfig = json.load(open(os.path.expanduser(configToLoad)))
        except ValueError, e:
            p("Error loading config: %s" % e)
            opter.exit(1)
        else:
            # Config loaded, update optparser's defaults and reparse
            defaults.update(loadedConfig)
            opter = cliarg_parser.getCommandlineParser(defaults)
            opts, args = opter.parse_args()

    # Decode args using filesystem encoding (done after config loading
    # as the args are reparsed when the config is loaded)
    args = [x.decode(sys.getfilesystemencoding()) for x in args]

    # dump config into file or stdout
    if opts.saveconfig or opts.showconfig:
        configToSave = dict(opts.__dict__)
        del configToSave['saveconfig']
        del configToSave['loadconfig']
        del configToSave['showconfig']

        # Save config argument
        if opts.saveconfig:
            p("Saving config: %s" % (opts.saveconfig))
            json.dump(
                configToSave,
                open(os.path.expanduser(opts.saveconfig), "w+"),
                sort_keys=True,
                indent=4)

        # Show config argument
        elif opts.showconfig:
            print json.dumps(opts.__dict__, sort_keys=True, indent=2)

        return

    # Update global config object
    Config.update(opts.__dict__)

    # TODO: write function to check all exclusive options
    try:
        if Config["move_files_only"] and not Config["move_files_enable"]:
            raise ConfigValueError("Parameter move_files_enable cannot be set to false while parameter move_only is set to true.")

        if Config['always_copy'] and Config['always_move']:
            raise ConfigValueError("Both always_copy and always_move cannot be specified.")
    except ConfigValueError, e:
        p("#" * 20)
        p("Error in config:")
        p(e.message)
        p("#" * 20)
        opter.exit(0)

    if Config['titlecase_filename'] and Config['lowercase_filename']:
        warnings.warn("Setting 'lowercase_filename' clobbers 'titlecase_filename' option")



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
