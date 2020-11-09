#!/usr/bin/env python

"""Tests custom replacements on input/output files
"""

from functional_runner import run_tvnamer, verify_out_data
from helpers import attr


@attr("functional")
def test_replace_input():
    """Tests replacing strings in input files
    """
    out_data = run_tvnamer(
        with_files = ['scruuuuuubs.s01e01.avi'],
        with_config = """
{
    "input_series_replacements": {
        "scru*bs": "scrubs"},
    "always_rename": true,
    "select_first": true
}
""")

    expected_files = ['Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_replace_input_with_id():
    """Map from a series name to a numberic TVDB ID
    """

    out_data = run_tvnamer(
        with_files = ['seriesnamegoeshere.s01e01.avi'],
        with_config = """
{
    "input_series_replacements": {
        "seriesnamegoeshere": 76156},
    "always_rename": true,
    "select_first": true
}
""")

    expected_files = ['Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_replace_output():
    """Tests replacing strings in input files
    """
    out_data = run_tvnamer(
        with_files = ['Scrubs.s01e01.avi'],
        with_config = """
{
    "output_series_replacements": {
        "Scrubs": "Replacement Series Name"},
    "always_rename": true,
    "select_first": true
}
""")

    expected_files = ['Replacement Series Name - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_replacements_mulitple_Files():
    """Test for https://github.com/dbr/tvnamer/issues/150 - need to test replacement with multiple files specified
    """

    conf = r"""
    {"always_rename": true,
    "select_first": true,
    "skip_file_on_error": false,
    "input_series_replacements": {
        "Example": 153021
    }
    }
    """

    out_data = run_tvnamer(
        with_files = ['Example.s01e01.avi', 'Scrubs.s01e01.avi'],
        with_config = conf,
        with_input = "",
        run_on_directory = True)

    expected_files = ['The Walking Dead - [01x01] - Days Gone Bye.avi', 'Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)
