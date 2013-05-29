#!/usr/bin/env python

""" Main tvnamer utility functionality
"""

import os
import sys
import logging

try:
    import json
except ImportError:
    import simplejson as json

from __init__ import __version__
from tvdb_api import Tvdb

import cliarg_parser
from config import Config

from unicode_helper import p
from utils import FileFinder, FileParser, applyCustomInputReplacements

from tvnamer_exceptions import (ConfigValueError, ShowNotFound, SeasonNotFound, EpisodeNotFound,
EpisodeNameNotFound, UserAbort, InvalidPath, NoValidFilesFoundError,
InvalidFilename, DataRetrievalError)

from renamer import Renamer


def log():
    """ Returns the logger for current file
    """
    return logging.getLogger(__name__)


def confirm(question, options, default = "y"):
    """ Takes a question (string), list of options and a default value (used
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


def processFile(tvdb_instance, episode):
    """ Gets episode name, prompts user for input
    """

    p("#" * 20)
    p("# Processing file: %s" % episode.fullfilename)

    if len(Config['input_filename_replacements']) > 0:
        p("# With custom replacements: %s" % applyCustomInputReplacements(episode.fullfilename))

    p("# Detected series: %s (%s)" % (episode.seriesname, episode.number_string()))

    try:
        episode.populateFromTvdb(tvdb_instance, force_name=Config['force_name'], series_id=Config['series_id'])
    except (DataRetrievalError, ShowNotFound, SeasonNotFound, EpisodeNotFound, EpisodeNameNotFound), errormsg:
        log().warn(errormsg)
        if Config['batch'] and Config['exit_on_error']:
            sys.exit(1)
        if Config['batch'] and Config['skip_file_on_error']:
            log().warn("Skipping file due to previous error.")
            return

    newFullPath = episode.getNewFullPath()

    # don't do anything if filename was not changed
    if newFullPath == episode.fullpath:
        p("Existing filename is correct: %s" % episode.fullpath)
        return

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
    cnamer = Renamer(episode.fullpath)
    try:
        cnamer.rename(
            new_fullpath = newFullPath,
            always_move = Config['always_move'],
            always_copy = Config['always_copy'],
            leave_symlink = Config['leave_symlink'],
            force = Config['overwrite_destination'])
    except OSError, e:
        log().warn(e)


def findFiles(paths):
    """ Takes an array of paths, returns all files found
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
            log().warn("Invalid path: %s" % cfile)

    if len(valid_files) == 0:
        raise NoValidFilesFoundError()

    # Remove duplicate files (all paths from FileFinder are absolute)
    valid_files = list(set(valid_files))

    return valid_files


def tvnamer(paths):
    """ Main tvnamer function, takes an array of paths, does stuff.
    """

    episodes_found = []

    for cfile in findFiles(paths):
        parser = FileParser(cfile)
        try:
            episode = parser.parse()
        except InvalidFilename, e:
            log().warn("Invalid filename: %s" % e)
        else:
            if episode.seriesname is None and Config['force_name'] is None and Config['series_id'] is None:
                log().warn("Parsed filename did not contain series name (and --name or --series-id not specified), skipping: %s" % cfile)
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


class Logger:
    """ Helper class holding logging handlers, formatters etc. so that
        they can be added or removed at runtime.
    """

    def __init__(self):
        self.consoleFormatter = logging.Formatter('%(levelname)s - %(message)s')
        self.fileFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.rootLogger = logging.getLogger()
        self.rootLogger.setLevel(logging.DEBUG)
        self.consoleHandler = None
        self.fileHandler = None

    def initLogging(self, verbose_console=False, filename=""):
        """ Init logging to console and file specified by 'filename' argument.
            Maximum log level of console can be configured by 'consoleLogLevel' argument,
            log level of file is always DEBUG.
        """

        self.rootLogger.removeHandler(self.consoleHandler)
        self.rootLogger.removeHandler(self.fileHandler)

        # create console handler with INFO log level
        self.consoleHandler = logging.StreamHandler()
        if verbose_console:
            self.consoleHandler.setLevel(logging.DEBUG)
        else:
            self.consoleHandler.setLevel(logging.INFO)
        self.consoleHandler.setFormatter(self.consoleFormatter)
        self.rootLogger.addHandler(self.consoleHandler)

        if filename:
            # create file handler with DEBUG log level
            self.fileHandler = logging.FileHandler(filename)
            self.fileHandler.setLevel(logging.DEBUG)
            self.fileHandler.setFormatter(self.fileFormatter)
            self.rootLogger.addHandler(self.fileHandler)

    def __del__(self):
        log().debug("tvnamer exited")
        logging.shutdown()


def main():
    """ Parses command line arguments, displays errors from tvnamer in terminal
    """

    logger = Logger()
    logger.initLogging()

    opter = cliarg_parser.getCommandlineParser(Config)
    opts, args = opter.parse_args()

    logger.initLogging(verbose_console=opts.verbose, filename=opts.log_file)
    log().debug("tvnamer started")

    # If a config is specified, load it, update the Config using the loaded
    # values, then reparse the options with the updated Config.
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
            config_version = loadedConfig.get("__version__") or "0"
            if cmp(__version__, config_version):
                msg = "Old config file detected, please see "
                msg += "https://github.com/dbr/tvnamer/blob/master/tvnamer/config_defaults.py"
                msg += " and/or "
                msg += "https://github.com/dbr/tvnamer/blob/master/Changelog"
                msg += " and merge updates.\nProgram version: %s\nConfig version: %s" % (__version__, config_version)
                raise ConfigValueError(msg)
        except ValueError, e:
            p("Error loading config: %s" % e)
            opter.exit(1)
        except ConfigValueError, e:
            log().error("Error in config: " + e.message)
            opter.exit(1)
        else:
            # Config loaded, update optparser's Config and reparse
            Config.update(loadedConfig)
            opter = cliarg_parser.getCommandlineParser(Config)
            opts, args = opter.parse_args()
            # log file path may be specified in config
            logger.initLogging(verbose_console=opts.verbose, filename=opts.log_file)

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
            p(json.dumps(opts.__dict__, sort_keys=True, indent=2))

        return

    # Update global config object
    Config.update(opts.__dict__)

    # TODO: write function to check all exclusive options
    try:
        if Config['always_copy'] and Config['always_move']:
            raise ConfigValueError("Both always_copy and always_move cannot be specified.")
        if Config['titlecase_dynamic_parts'] and Config['lowercase_dynamic_parts']:
            raise ConfigValueError("Both 'lowercase_filename' and 'titlecase_filename' cannot be specified.")
    except ConfigValueError, e:
        log().error("Error in config: " + e.message)
        opter.exit(1)


    if len(args) == 0:
        opter.error("No filenames or directories supplied")

    try:
        args.sort()
        tvnamer(paths = args)
    except NoValidFilesFoundError:
        opter.error("No valid files were supplied")
    except UserAbort, errormsg:
        opter.error(errormsg)

if __name__ == '__main__':
    main()
