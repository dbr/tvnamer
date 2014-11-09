#!/usr/bin/env python

"""Ensure that invalid files (non-episodes) are not renamed
"""

from functional_runner import run_tvnamer, verify_out_data
from helpers import attr


@attr("functional")
def test_simple_single_file():
    """Files without series name should be skipped, unless --name=MySeries is specified
    """

    out_data = run_tvnamer(
        with_files = ['S01E02 - Some File.avi'],
        with_flags = ["--batch"])

    expected_files = ['S01E02 - Some File.avi']

    verify_out_data(out_data, expected_files, expected_returncode = 2)


@attr("functional")
def test_simple_single_file_with_forced_seriesnames():
    """Specifying 's01e01.avi' should parse when --name=SeriesName arg is specified
    """

    out_data = run_tvnamer(
        with_files = ['S01E02 - Some File.avi'],
        with_flags = ["--batch", '--name', 'Scrubs'])

    expected_files = ['Scrubs - [01x02] - My Mentor.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_name_arg_skips_replacements():
    """Should not apply input_filename_replacements to --name=SeriesName arg value
    """

    conf = r"""
    {"always_rename": true,
    "select_first": true,

    "force_name": "Scrubs",

    "input_filename_replacements": [
        {"is_regex": true,
        "match": "Scrubs",
        "replacement": "Blahblahblah"}
    ]
    }
    """

    out_data = run_tvnamer(
        with_files = ['S01E02 - Some File.avi'],
        with_config = conf)

    expected_files = ['Scrubs - [01x02] - My Mentor.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_replacements_applied_before_force_name():
    """input_filename_replacements apply to filename, before --name=SeriesName takes effect
    """

    conf = r"""
    {"always_rename": true,
    "select_first": true,

    "force_name": "Scrubs",

    "input_filename_replacements": [
        {"is_regex": true,
        "match": "S01E02 - ",
        "replacement": ""}
    ]
    }
    """

    out_data = run_tvnamer(
        with_files = ['S01E02 - Some File.avi'],
        with_config = conf)

    expected_files = ['S01E02 - Some File.avi']

    verify_out_data(out_data, expected_files, expected_returncode = 2)
