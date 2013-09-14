#!/usr/bin/env python

"""Tests custom replacements on input/output files
"""

from functional_runner import run_tvnamer, verify_out_data
from nose.plugins.attrib import attr


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
    "batch": true
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
    "batch": true
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
    "batch": true
}
""")

    expected_files = ['Replacement Series Name - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)
