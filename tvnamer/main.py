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

import tvdb_api
from typing import List, Union, Optional

from tvnamer import cliarg_parser, __version__
from tvnamer.config_defaults import defaults
from tvnamer.config import Config
from .files import FileFinder, FileParser, Renamer, _apply_replacements_input
from .utils import (
    warn,
    format_episode_numbers,
    make_valid_filename,
)
from tvnamer.data import (
    BaseInfo,
    EpisodeInfo,
    DatedEpisodeInfo,
    NoSeasonEpisodeInfo,
)

from tvnamer.tvnamer_exceptions import (
    ShowNotFound,
    SeasonNotFound,
    EpisodeNotFound,
    EpisodeNameNotFound,
    UserAbort,
    InvalidPath,
    NoValidFilesFoundError,
    SkipBehaviourAbort,
    InvalidFilename,
    DataRetrievalError,
)


LOG = logging.getLogger(__name__)


# Key for use in tvnamer only - other keys can easily be registered at https://thetvdb.com/api-information
TVNAMER_API_KEY = "fb51f9b848ffac9750bada89ecba0225"


def get_move_destination(episode):
    # type: (BaseInfo) -> str
    """Constructs the location to move/copy the file
    """

    # TODO: Write functional test to ensure this valid'ifying works
    def wrap_validfname(fname):
        # type: (str) -> str
        """Wrap the make_valid_filename function as it's called twice
        and this is slightly long..
        """
        if Config["move_files_lowercase_destination"]:
            fname = fname.lower()
        return make_valid_filename(
            fname,
            windows_safe=Config["windows_safe_filenames"],
            custom_blacklist=Config["custom_filename_character_blacklist"],
            replace_with=Config["replace_invalid_characters_with"],
        )

    # Calls make_valid_filename on series name, as it must valid for a filename
    if isinstance(episode, DatedEpisodeInfo):
        dest_dir = Config["move_files_destination_date"] % {
            "seriesname": make_valid_filename(episode.seriesname),
            "year": episode.episodenumbers[0].year,
            "month": episode.episodenumbers[0].month,
            "day": episode.episodenumbers[0].day,
            "originalfilename": episode.originalfilename,
        }
    elif isinstance(episode, NoSeasonEpisodeInfo):
        dest_dir = Config["move_files_destination"] % {
            "seriesname": wrap_validfname(episode.seriesname),
            "episodenumbers": wrap_validfname(
                format_episode_numbers(episode.episodenumbers)
            ),
            "originalfilename": episode.originalfilename,
        }
    elif isinstance(episode, EpisodeInfo):
        dest_dir = Config["move_files_destination"] % {
            "seriesname": wrap_validfname(episode.seriesname),
            "seasonnumber": episode.seasonnumber,
            "episodenumbers": wrap_validfname(
                format_episode_numbers(episode.episodenumbers)
            ),
            "originalfilename": episode.originalfilename,
        }
    else:
        raise RuntimeError("Unhandled episode subtype of %s" % type(episode))

    return dest_dir


def do_rename_file(cnamer, new_name):
    # type: (Renamer, str) -> None
    """Renames the file. cnamer should be Renamer instance,
    new_name should be string containing new filename.
    """
    try:
        cnamer.new_path(
            new_fullpath=new_name,
            force=Config["overwrite_destination_on_rename"],
            leave_symlink=Config["leave_symlink"],
        )
    except OSError as e:
        if Config["skip_behaviour"] == "exit":
            warn("Exiting due to error: %s" % e)
            raise SkipBehaviourAbort()
        warn("Skipping file due to error: %s" % e)


def do_move_file(cnamer, dest_dir=None, dest_filepath=None, get_path_preview=False):
    # type: (Renamer, Optional[str], Optional[str], bool) -> str
    """Moves file to dest_dir, or to dest_filepath
    """

    if (dest_dir, dest_filepath).count(None) != 1:
        raise ValueError("Specify only dest_dir or dest_filepath")

    if not Config["move_files_enable"]:
        raise ValueError("move_files feature is disabled but do_move_file was called")

    if Config["move_files_destination"] is None:
        raise ValueError(
            "Config value for move_files_destination cannot be None if move_files_enabled is True"
        )

    try:
        return cnamer.new_path(
            new_path=dest_dir,
            new_fullpath=dest_filepath,
            always_move=Config["always_move"],
            leave_symlink=Config["leave_symlink"],
            get_path_preview=get_path_preview,
            force=Config["overwrite_destination_on_move"],
        )

    except OSError as e:
        if Config["skip_behaviour"] == "exit":
            warn("Exiting due to error: %s" % e)
            raise SkipBehaviourAbort()
        warn("Skipping file due to error: %s" % e)


def confirm(question, options, default="y"):
    """Takes a question (string), list of options and a default value (used
    when user simply hits enter).
    Asks until valid option is entered.
    """
    # Highlight default option with [ ]
    options_str = []
    for x in options:
        if x == default:
            x = "[%s]" % x
        if x != "":
            options_str.append(x)
    options_str = "/".join(options_str)

    while True:
        print(question)
        print("(%s) " % (options_str), end="")
        try:
            ans = input().strip()
        except KeyboardInterrupt as errormsg:
            print("\n", errormsg)
            raise UserAbort(errormsg)

        if ans in options:
            return ans
        elif ans == "":
            return default


def process_file(tvdb_instance, episode):
    # type: (tvdb_api.Tvdb, BaseInfo) -> None
    """Gets episode name, prompts user for input
    """
    print("#" * 20)
    print("# Processing file: %s" % episode.fullfilename)

    if len(Config["input_filename_replacements"]) > 0:
        replaced = _apply_replacements_input(episode.fullfilename)
        print("# With custom replacements: %s" % (replaced))

    # Use force_name option. Done after input_filename_replacements so
    # it can be used to skip the replacements easily
    if Config["force_name"] is not None:
        episode.seriesname = Config["force_name"]

    print("# Detected series: %s (%s)" % (episode.seriesname, episode.number_string()))

    try:
        episode.populate_from_tvdb(
            tvdb_instance,
            force_name=Config["force_name"],
            series_id=Config["series_id"],
        )
    except (DataRetrievalError, ShowNotFound) as errormsg:
        if Config["always_rename"] and Config["skip_file_on_error"] is True:
            if Config["skip_behaviour"] == "exit":
                warn("Exiting due to error: %s" % errormsg)
                raise SkipBehaviourAbort()
            warn("Skipping file due to error: %s" % errormsg)
            return
        else:
            warn("%s" % (errormsg))
    except (SeasonNotFound, EpisodeNotFound, EpisodeNameNotFound) as errormsg:
        # Show was found, so use corrected series name
        if Config["always_rename"] and Config["skip_file_on_error"]:
            if Config["skip_behaviour"] == "exit":
                warn("Exiting due to error: %s" % errormsg)
                raise SkipBehaviourAbort()
            warn("Skipping file due to error: %s" % errormsg)
            return

        warn("%s" % (errormsg))

    cnamer = Renamer(episode.fullpath)

    should_rename = False

    if Config["move_files_only"]:

        new_name = episode.fullfilename
        should_rename = True

    else:
        new_name = episode.generate_filename()
        if new_name == episode.fullfilename:
            print("#" * 20)
            print("Existing filename is correct: %s" % episode.fullfilename)
            print("#" * 20)

            should_rename = True

        else:
            print("#" * 20)
            print("Old filename: %s" % episode.fullfilename)

            if len(Config["output_filename_replacements"]) > 0:
                # Show filename without replacements
                print(
                    "Before custom output replacements: %s"
                    % (episode.generate_filename(preview_orig_filename=False))
                )

            print("New filename: %s" % new_name)

            if Config["dry_run"]:
                print("%s will be renamed to %s" % (episode.fullfilename, new_name))
                if Config["move_files_enable"]:
                    print(
                        "%s will be moved to %s"
                        % (new_name, get_move_destination(episode))
                    )
                return
            elif Config["always_rename"]:
                do_rename_file(cnamer, new_name)
                if Config["move_files_enable"]:
                    if Config["move_files_destination_is_filepath"]:
                        do_move_file(
                            cnamer=cnamer, dest_filepath=get_move_destination(episode)
                        )
                    else:
                        do_move_file(cnamer=cnamer, dest_dir=get_move_destination(episode))
                return

            ans = confirm("Rename?", options=["y", "n", "a", "q"], default="y")

            if ans == "a":
                print("Always renaming")
                Config["always_rename"] = True
                should_rename = True
            elif ans == "q":
                print("Quitting")
                raise UserAbort("User exited with q")
            elif ans == "y":
                print("Renaming")
                should_rename = True
            elif ans == "n":
                print("Skipping")
            else:
                print("Invalid input, skipping")

            if should_rename:
                do_rename_file(cnamer, new_name)

    if should_rename and Config["move_files_enable"]:
        new_path = get_move_destination(episode)
        if Config["dry_run"]:
            print("%s will be moved to %s" % (new_name, get_move_destination(episode)))
            return

        if Config["move_files_destination_is_filepath"]:
            do_move_file(cnamer=cnamer, dest_filepath=new_path, get_path_preview=True)
        else:
            do_move_file(cnamer=cnamer, dest_dir=new_path, get_path_preview=True)

        if not Config["batch"] and Config["move_files_confirmation"]:
            ans = confirm("Move file?", options=["y", "n", "q"], default="y")
        else:
            ans = "y"

        if ans == "y":
            print("Moving file")
            do_move_file(cnamer, new_path)
        elif ans == "q":
            print("Quitting")
            raise UserAbort("user exited with q")


def find_files(paths):
    # type: (List[str]) -> List[str]
    """Takes an array of paths, returns all files found
    """
    valid_files = []

    for cfile in paths:
        cur = FileFinder(
            cfile,
            with_extension=Config["valid_extensions"],
            filename_blacklist=Config["filename_blacklist"],
            recursive=Config["recursive"],
        )

        try:
            valid_files.extend(cur.find_files())
        except InvalidPath:
            warn("Invalid path: %s" % cfile)

    if len(valid_files) == 0:
        raise NoValidFilesFoundError()

    # Remove duplicate files (all paths from FileFinder are absolute)
    valid_files = list(set(valid_files))

    return valid_files


def tvnamer(paths):
    # type: (List[str]) -> None
    """Main tvnamer function, takes an array of paths, does stuff.
    """

    print("#" * 20)
    print("# Starting tvnamer")

    episodes_found = []

    for cfile in find_files(paths):
        parser = FileParser(cfile)
        try:
            episode = parser.parse()
        except InvalidFilename as e:
            warn("Invalid filename: %s" % e)
        else:
            if (
                episode.seriesname is None
                and Config["force_name"] is None
                and Config["series_id"] is None
            ):
                warn(
                    "Parsed filename did not contain series name (and --name or --series-id not specified), skipping: %s"
                    % cfile
                )

            else:
                episodes_found.append(episode)

    if len(episodes_found) == 0:
        raise NoValidFilesFoundError()

    print(
        "# Found %d episode" % len(episodes_found) + ("s" * (len(episodes_found) > 1))
    )

    # Sort episodes by series name, season and episode number
    episodes_found.sort(key=lambda x: x.sortable_info())

    # episode sort order
    if Config["order"] == "dvd":
        dvdorder = True
    else:
        dvdorder = False

    if Config["tvdb_api_key"] is not None:
        LOG.debug("Using custom API key from config")
        api_key = Config["tvdb_api_key"]
    else:
        LOG.debug("Using tvnamer default API key")
        api_key = TVNAMER_API_KEY

    tvdb_instance = tvdb_api.Tvdb(
        interactive=not Config["select_first"],
        search_all_languages=Config["search_all_languages"],
        language=Config["language"],
        dvdorder=dvdorder,
        cache=True,
        apikey=api_key,
    )

    for episode in episodes_found:
        process_file(tvdb_instance, episode)
        print("")

    print("#" * 20)
    print("# Done")


def main():
    # type: () -> None
    """Parses command line arguments, displays errors from tvnamer in terminal
    """
    opter = cliarg_parser.get_cli_parser(defaults)

    opts, args = opter.parse_args()

    if opts.show_version:
        print("tvnamer version: %s" % (__version__,))
        print("tvdb_api version: %s" % (tvdb_api.__version__,))
        sys.exit(0)

    if opts.verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
    else:
        logging.basicConfig()

    # If a config is specified, load it, update the defaults using the loaded
    # values, then reparse the options with the updated defaults.
    default_configuration = os.path.expanduser("~/.config/tvnamer/tvnamer.json")
    old_default_configuration = os.path.expanduser("~/.tvnamer.json")

    if opts.loadconfig is not None:
        # Command line overrides loading ~/.config/tvnamer/tvnamer.json
        config_to_load = opts.loadconfig
    elif os.path.isfile(default_configuration):
        # No --config arg, so load default config if it exists
        config_to_load = default_configuration
    elif os.path.isfile(old_default_configuration):
        # No --config arg and neow defualt config so load old version if it exist
        config_to_load = old_default_configuration
    else:
        # No arg, nothing at default config location, don't load anything
        config_to_load = None

    if config_to_load is not None:
        LOG.info("Loading config: %s" % (config_to_load))
        if os.path.isfile(old_default_configuration):
            LOG.warning("WARNING: you have a config at deprecated ~/.tvnamer.json location.")
            LOG.warning("Config must be moved to new location: ~/.config/tvnamer/tvnamer.json")

        try:
            loaded_config = json.load(open(os.path.expanduser(config_to_load)))
        except ValueError as e:
            LOG.error("Error loading config: %s" % e)
            opter.exit(1)
        else:
            # Config loaded, update optparser's defaults and reparse
            defaults.update(loaded_config)
            opter = cliarg_parser.get_cli_parser(defaults)
            opts, args = opter.parse_args()

    # Save config argument
    if opts.saveconfig is not None:
        LOG.info("Saving config: %s" % (opts.saveconfig))
        config_to_save = dict(opts.__dict__)
        del config_to_save["saveconfig"]
        del config_to_save["loadconfig"]
        del config_to_save["showconfig"]
        json.dump(
            config_to_save,
            open(os.path.expanduser(opts.saveconfig), "w+"),
            sort_keys=True,
            indent=4,
        )

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
        opter.error(
            "Parameter move_files_enable cannot be set to false while parameter move_only is set to true."
        )

    if Config["titlecase_filename"] and Config["lowercase_filename"]:
        warnings.warn(
            "Setting 'lowercase_filename' clobbers 'titlecase_filename' option"
        )

    if len(args) == 0:
        opter.error("No filenames or directories supplied")

    try:
        tvnamer(paths=sorted(args))
    except NoValidFilesFoundError:
        opter.error("No valid files were supplied")
    except UserAbort as errormsg:
        opter.error(errormsg)
    except SkipBehaviourAbort as errormsg:
        opter.error(errormsg)


if __name__ == "__main__":
    main()
