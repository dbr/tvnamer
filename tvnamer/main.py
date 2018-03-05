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

import json

from tvdb_api import Tvdb

from tvnamer import cliarg_parser
from tvnamer.compat import PY2, raw_input
from tvnamer.config_defaults import defaults

from tvnamer.unicode_helper import p
from tvnamer.utils import (Config, FileFinder, FileParser, Renamer, warn,
applyCustomInputReplacements, formatEpisodeNumbers, makeValidFilename,
DatedEpisodeInfo, NoSeasonEpisodeInfo)

from tvnamer.tvnamer_exceptions import (ShowNotFound, SeasonNotFound, EpisodeNotFound,
EpisodeNameNotFound, UserAbort, InvalidPath, NoValidFilesFoundError, SkipBehaviourAbort,
InvalidFilename, DataRetrievalError)


def getMoveDestination(episode):
    """Constructs the location to move/copy the file
    """

    #TODO: Write functional test to ensure this valid'ifying works
    def wrap_validfname(fname):
        """Wrap the makeValidFilename function as it's called twice
        and this is slightly long..
        """
        if Config['move_files_lowercase_destination']:
            fname = fname.lower()
        return makeValidFilename(
            fname,
            normalize_unicode = Config['normalize_unicode_filenames'],
            windows_safe = Config['windows_safe_filenames'],
            custom_blacklist = Config['custom_filename_character_blacklist'],
            replace_with = Config['replace_invalid_characters_with'])


    # Calls makeValidFilename on series name, as it must valid for a filename
    if isinstance(episode, DatedEpisodeInfo):
        destdir = Config['move_files_destination_date'] % {
            'seriesname': makeValidFilename(episode.seriesname),
            'year': episode.episodenumbers[0].year,
            'month': episode.episodenumbers[0].month,
            'day': episode.episodenumbers[0].day,
            'originalfilename': episode.originalfilename,
            }
    elif isinstance(episode, NoSeasonEpisodeInfo):
        destdir = Config['move_files_destination'] % {
            'seriesname': wrap_validfname(episode.seriesname),
            'episodenumbers': wrap_validfname(formatEpisodeNumbers(episode.episodenumbers)),
            'originalfilename': episode.originalfilename,
            }
    else:
        destdir = Config['move_files_destination'] % {
            'seriesname': wrap_validfname(episode.seriesname),
            'seasonnumber': episode.seasonnumber,
            'episodenumbers': wrap_validfname(formatEpisodeNumbers(episode.episodenumbers)),
            'originalfilename': episode.originalfilename,
            }
    return destdir


def doRenameFile(cnamer, newName):
    """Renames the file. cnamer should be Renamer instance,
    newName should be string containing new filename.
    """
    try:
        cnamer.newPath(new_fullpath = newName, force = Config['overwrite_destination_on_rename'], leave_symlink = Config['leave_symlink'])
    except OSError as e:
        if Config['skip_behaviour'] == 'exit':
            warn("Exiting due to error: %s" % e)
            raise SkipBehaviourAbort()
        warn("Skipping file due to error: %s" % e)


def doMoveFile(cnamer, destDir = None, destFilepath = None, getPathPreview = False):
    """Moves file to destDir, or to destFilepath
    """

    if (destDir is None and destFilepath is None) or (destDir is not None and destFilepath is not None):
        raise ValueError("Specify only destDir or destFilepath")

    if not Config['move_files_enable']:
        raise ValueError("move_files feature is disabled but doMoveFile was called")

    if Config['move_files_destination'] is None:
        raise ValueError("Config value for move_files_destination cannot be None if move_files_enabled is True")

    try:
        return cnamer.newPath(
            new_path = destDir,
            new_fullpath = destFilepath,
            always_move = Config['always_move'],
            leave_symlink = Config['leave_symlink'],
            getPathPreview = getPathPreview,
            force = Config['overwrite_destination_on_move'])

    except OSError as e:
        if Config['skip_behaviour'] == 'exit':
            warn("Exiting due to error: %s" % e)
            raise SkipBehaviourAbort()
        warn("Skipping file due to error: %s" % e)


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
        except KeyboardInterrupt as errormsg:
            p("\n", errormsg)
            raise UserAbort(errormsg)

        if ans in options:
            return ans
        elif ans == '':
            return default


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
    except (DataRetrievalError, ShowNotFound) as errormsg:
        if Config['always_rename'] and Config['skip_file_on_error'] is True:
            if Config['skip_behaviour'] == 'exit':
                warn("Exiting due to error: %s" % errormsg)
                raise SkipBehaviourAbort()
            warn("Skipping file due to error: %s" % errormsg)
            return
        else:
            warn(errormsg)
    except (SeasonNotFound, EpisodeNotFound, EpisodeNameNotFound) as errormsg:
        # Show was found, so use corrected series name
        if Config['always_rename'] and Config['skip_file_on_error']:
            if Config['skip_behaviour'] == 'exit':
                warn("Exiting due to error: %s" % errormsg)
                raise SkipBehaviourAbort()
            warn("Skipping file due to error: %s" % errormsg)
            return

        warn(errormsg)

    cnamer = Renamer(episode.fullpath)


    shouldRename = False

    if Config["move_files_only"]:

        newName = episode.fullfilename
        shouldRename = True

    else:
        newName = episode.generateFilename()
        if newName == episode.fullfilename:
            p("#" * 20)
            p("Existing filename is correct: %s" % episode.fullfilename)
            p("#" * 20)

            shouldRename = True

        else:
            p("#" * 20)
            p("Old filename: %s" % episode.fullfilename)

            if len(Config['output_filename_replacements']) > 0:
                # Show filename without replacements
                p("Before custom output replacements: %s" % (episode.generateFilename(preview_orig_filename = False)))

            p("New filename: %s" % newName)

            if Config['always_rename']:
                doRenameFile(cnamer, newName)
                if Config['move_files_enable']:
                    if Config['move_files_destination_is_filepath']:
                        doMoveFile(cnamer = cnamer, destFilepath = getMoveDestination(episode))
                    else:
                        doMoveFile(cnamer = cnamer, destDir = getMoveDestination(episode))
                return

            elif Config['dry_run']:
                p("%s will be renamed to %s" % (episode.fullfilename, newName))
                if Config['move_files_enable']:
                    p("%s will be moved to %s" % (newName, getMoveDestination(episode)))
                return

            ans = confirm("Rename?", options = ['y', 'n', 'a', 'q'], default = 'y')

            if ans == "a":
                p("Always renaming")
                Config['always_rename'] = True
                shouldRename = True
            elif ans == "q":
                p("Quitting")
                raise UserAbort("User exited with q")
            elif ans == "y":
                p("Renaming")
                shouldRename = True
            elif ans == "n":
                p("Skipping")
            else:
                p("Invalid input, skipping")

            if shouldRename:
                doRenameFile(cnamer, newName)

    if shouldRename and Config['move_files_enable']:
        newPath = getMoveDestination(episode)
        if Config['dry_run']:
            p("%s will be moved to %s" % (newName, getMoveDestination(episode)))
            return

        if Config['move_files_destination_is_filepath']:
            doMoveFile(cnamer = cnamer, destFilepath = newPath, getPathPreview = True)
        else:
            doMoveFile(cnamer = cnamer, destDir = newPath, getPathPreview = True)

        if not Config['batch'] and Config['move_files_confirmation']:
            ans = confirm("Move file?", options = ['y', 'n', 'q'], default = 'y')
        else:
            ans = 'y'

        if ans == 'y':
            p("Moving file")
            doMoveFile(cnamer, newPath)
        elif ans == 'q':
            p("Quitting")
            raise UserAbort("user exited with q")


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
        except InvalidFilename as e:
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

    # episode sort order
    if Config['order'] == 'dvd':
        dvdorder = True
    else:
        dvdorder = False

    if not PY2 and os.getenv("TRAVIS", "false") == "true":
        # Disable caching on Travis-CI because in Python 3 it errors with:
        #
        # Can't pickle <class 'http.cookiejar.DefaultCookiePolicy'>: it's not the same object as http.cookiejar.DefaultCookiePolicy
        cache = False
    else:
        cache = True

    tvdb_instance = Tvdb(
        interactive = not Config['select_first'],
        search_all_languages = Config['search_all_languages'],
        language = Config['language'],
        dvdorder = dvdorder,
        cache=cache,
    )

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
        except ValueError as e:
            p("Error loading config: %s" % e)
            opter.exit(1)
        else:
            # Config loaded, update optparser's defaults and reparse
            defaults.update(loadedConfig)
            opter = cliarg_parser.getCommandlineParser(defaults)
            opts, args = opter.parse_args()

    # Decode args using filesystem encoding (done after config loading
    # as the args are reparsed when the config is loaded)
    if PY2:
        args = [x.decode(sys.getfilesystemencoding()) for x in args]

    # Save config argument
    if opts.saveconfig is not None:
        p("Saving config: %s" % (opts.saveconfig))
        configToSave = dict(opts.__dict__)
        del configToSave['saveconfig']
        del configToSave['loadconfig']
        del configToSave['showconfig']
        json.dump(
            configToSave,
            open(os.path.expanduser(opts.saveconfig), "w+"),
            sort_keys=True,
            indent=4)

        opter.exit(0)

    # Show config argument
    if opts.showconfig:
        print(json.dumps(opts.__dict__, sort_keys=True, indent=2))
        return

    # Process values
    if opts.batch:
        opts.select_first = True
        opts.always_rename = True

    # Update global config object
    Config.update(opts.__dict__)

    if Config["move_files_only"] and not Config["move_files_enable"]:
        p("#" * 20)
        p("Parameter move_files_enable cannot be set to false while parameter move_only is set to true.")
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
    except UserAbort as errormsg:
        opter.error(errormsg)
    except SkipBehaviourAbort as errormsg:
        opter.error(errormsg)

if __name__ == '__main__':
    main()
