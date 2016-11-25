#!/usr/bin/env python

"""Tests various configs load correctly
"""

from functional_runner import run_tvnamer, verify_out_data
from helpers import attr
import pytest


@attr("functional")
def test_batchconfig():
    """Test configured batch mode works
    """

    conf = """
    {"always_rename": true,
    "select_first": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_skip_file_on_error():
    """Test the "skip file on error" config option works
    """

    conf = """
    {"skip_file_on_error": true,
    "always_rename": true}
    """

    out_data = run_tvnamer(
        with_files = ['a.fake.episode.s01e01.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['a.fake.episode.s01e01.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_do_not_skip_file_on_error():
    """Test setting "skip file on error" config option to False
    """

    conf = """
    {"skip_file_on_error": false,
    "always_rename": true}
    """

    out_data = run_tvnamer(
        with_files = ['a.fake.episode.s01e01.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['a fake episode - [01x01].avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_skip_behaviour_warn():
    """skip_behaivour:warn should keep renaming other files
    """

    conf = """
    {"skip_file_on_error": false,
    "batch": true,
    "skip_behaviour": "warn"}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'a.fake.episode.s01e01.avi', 'scrubs.s01e02.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['a fake episode - [01x01].avi', 'Scrubs - [01x01] - My First Day.avi', 'Scrubs - [01x02] - My Mentor.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_skip_behaviour_error():
    """With skip_behaviour:error, should end process
    """

    conf = """
    {"skip_file_on_error": false,
    "batch": true,
    "skip_behaviour": "warn"}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'a.fake.episode.s01e01.avi', 'scrubs.s01e02.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['a fake episode - [01x01].avi', 'Scrubs - [01x01] - My First Day.avi', 'Scrubs - [01x02] - My Mentor.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_lowercase_names():
    """Test setting "lowercase_filename" config option
    """

    conf = """
    {"lowercase_filename": true,
    "always_rename": true,
    "select_first": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['scrubs - [01x01] - my first day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_replace_with_underscore():
    """Test custom blacklist to replace " " with "_"
    """

    conf = """
    {"custom_filename_character_blacklist": " ",
    "replace_blacklisted_characters_with": "_",
    "always_rename": true,
    "select_first": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['Scrubs_-_[01x01]_-_My_First_Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
@pytest.mark.xfail
def test_abs_epnmber():
    """Ensure the absolute episode number is available for custom
    filenames in config
    """


    conf = """
    {"filename_with_episode": "%(seriesname)s - %(absoluteepisode)s%(ext)s",
    "always_rename": true,
    "select_first": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['Scrubs - 01.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_resolve_absoloute_episode():
    """Test resolving by absolute episode number
    """

    conf = """
    {"always_rename": true,
    "select_first": true}
    """

    out_data = run_tvnamer(
        with_files = ['[Bleachverse]_BLEACH_310.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['[Bleachverse] Bleach - 310 - Ichigo\'s Resolution.avi']

    verify_out_data(out_data, expected_files)

    print("Checking output files are re-parsable")
    out_data = run_tvnamer(
        with_files = expected_files,
        with_config = conf,
        with_input = "")

    expected_files = ['[Bleachverse] Bleach - 310 - Ichigo\'s Resolution.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_valid_extension_recursive():
    """When using valid_extensions in a custom config file, recursive search doesn't work. Github issue #36
    """

    conf = """
    {"always_rename": true,
    "select_first": true,
    "valid_extensions": ["avi","mp4","m4v","wmv","mkv","mov","srt"],
    "recursive": true}
    """

    out_data = run_tvnamer(
        with_files = ['nested/dir/scrubs.s01e01.avi'],
        with_config = conf,
        with_input = "",
        run_on_directory = True)

    expected_files = ['nested/dir/Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_replace_ands():
    """Test replace "and" "&"
    """

    conf = r"""
    {"always_rename": true,
    "select_first": true,
    "input_filename_replacements": [
        {"is_regex": true,
        "match": "(\\Wand\\W| & )",
        "replacement": " "}
    ]
    }
    """

    out_data = run_tvnamer(
        with_files = ['Brothers.and.Sisters.S05E16.HDTV.XviD-LOL.avi'],
        with_config = conf,
        with_input = "",
        run_on_directory = True)

    expected_files = ['Brothers & Sisters - [05x16] - Home Is Where The Fort Is.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_replace_ands_in_output_also():
    """Test replace "and" "&" for search, and replace & in output filename
    """

    conf = r"""
    {"always_rename": true,
    "select_first": true,
    "input_filename_replacements": [
        {"is_regex": true,
        "match": "(\\Wand\\W| & )",
        "replacement": " "}
    ],
    "output_filename_replacements": [
        {"is_regex": true,
        "match": " & ",
        "replacement": " and "}
    ]
    }
    """

    out_data = run_tvnamer(
        with_files = ['Brothers.and.Sisters.S05E16.HDTV.XviD-LOL.avi'],
        with_config = conf,
        with_input = "",
        run_on_directory = True)

    expected_files = ['Brothers and Sisters - [05x16] - Home Is Where The Fort Is.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_force_overwrite_enabled():
    """Tests forcefully overwritting existing filenames
    """

    conf = r"""
    {"always_rename": true,
    "select_first": true,
    "overwrite_destination_on_rename": true
    }
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'Scrubs - [01x01] - My First Day.avi'],
        with_config = conf,
        with_input = "",
        run_on_directory = True)

    expected_files = ['Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_force_overwrite_disabled():
    """Explicitly disabling forceful-overwrite
    """

    conf = r"""
    {"always_rename": true,
    "select_first": true,
    "overwrite_destination_on_rename": false
    }
    """

    out_data = run_tvnamer(
        with_files = ['Scrubs - [01x01] - My First Day.avi', 'scrubs - [01x01].avi'],
        with_config = conf,
        with_input = "",
        run_on_directory = True)

    expected_files = ['Scrubs - [01x01] - My First Day.avi', 'scrubs - [01x01].avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_force_overwrite_default():
    """Forceful-overwrite should be disabled by default
    """

    conf = r"""
    {"always_rename": true,
    "select_first": true
    }
    """

    out_data = run_tvnamer(
        with_files = ['Scrubs - [01x01] - My First Day.avi', 'scrubs - [01x01].avi'],
        with_config = conf,
        with_input = "",
        run_on_directory = True)

    expected_files = ['Scrubs - [01x01] - My First Day.avi', 'scrubs - [01x01].avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_titlecase():
    """Tests Title Case Option To Make Episodes Like This
    """

    conf = r"""
    {"always_rename": true,
    "select_first": true,
    "skip_file_on_error": false,
    "titlecase_filename": true
    }
    """

    out_data = run_tvnamer(
        with_files = ['this.is.a.fake.episode.s01e01.avi'],
        with_config = conf,
        with_input = "",
        run_on_directory = True)

    expected_files = ['This Is a Fake Episode - [01x01].avi']

    verify_out_data(out_data, expected_files)
