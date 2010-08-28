#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Tests custom replacements on input/output files
"""

from functional_runner import run_tvnamer, verify_out_data
from nose.plugins.attrib import attr


@attr("functional")
def test_simple_input_replacements():
    """Tests replacing strings in input files
    """
    out_data = run_tvnamer(
        with_files = ['scruuuuuubs.s01e01.avi'],
        with_config = """
{
    "input_filename_replacements": [
        {"is_regex": false,
        "match": "uuuuuu",
        "replacement": "u"}
    ],
    "always_rename": true,
    "select_first": true
}
""")

    expected_files = ['Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_simple_output_replacements():
    """Tests replacing strings in input files
    """
    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_config = """
{
    "output_filename_replacements": [
        {"is_regex": false,
        "match": "u",
        "replacement": "v"}
    ],
    "always_rename": true,
    "select_first": true
}
""")

    expected_files = ['Scrvbs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_regex_input_replacements():
    """Tests regex replacement in input files
    """
    out_data = run_tvnamer(
        with_files = ['scruuuuuubs.s01e01.avi'],
        with_config = """
{
    "input_filename_replacements": [
        {"is_regex": true,
        "match": "[u]+",
        "replacement": "u"}
    ],
    "always_rename": true,
    "select_first": true
}
""")

    expected_files = ['Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_regex_output_replacements():
    """Tests regex replacement in output files
    """
    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_config = """
{
    "output_filename_replacements": [
        {"is_regex": true,
        "match": "[ua]+",
        "replacement": "v"}
    ],
    "always_rename": true,
    "select_first": true
}
""")

    expected_files = ['Scrvbs - [01x01] - My First Dvy.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_replacing_spaces():
    """Tests more practical use of replacements, removing spaces
    """
    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_config = """
{
    "output_filename_replacements": [
        {"is_regex": true,
        "match": "[ ]",
        "replacement": "."}
    ],
    "always_rename": true,
    "select_first": true
}
""")

    expected_files = ['Scrubs.-.[01x01].-.My.First.Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_replacing_ands():
    """Tests removind "and" and "&" from input files
    """
    out_data = run_tvnamer(
        with_files = ['Law & Order s01e01.avi'],
        with_config = """
{
    "input_filename_replacements": [
        {"is_regex": true,
        "match": "( and | & )",
        "replacement": " "}
    ],
    "output_filename_replacements": [
        {"is_regex": false,
        "match": " & ",
        "replacement": " and "}
    ],
    "always_rename": true,
    "select_first": true
}
""")

    expected_files = ['Law and Order - [01x01] - Prescription For Death.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_multiple_replacements():
    """Tests multiple replacements on one file
    """
    out_data = run_tvnamer(
    with_files = ['scrubs.s01e01.avi'],
    with_config = """
{
    "output_filename_replacements": [
        {"is_regex": true,
        "match": "[ua]+",
        "replacement": "v"},
        {"is_regex": false,
        "match": "v",
        "replacement": "_"}
    ],
    "always_rename": true,
    "select_first": true
}
""")

    expected_files = ['Scr_bs - [01x01] - My First D_y.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_fullpath_replacements():
    """Tests replacing strings in output path
    """
    out_data = run_tvnamer(
    with_files = ['scrubs.s01e01.avi'],
    with_config = """
{
    "move_files_enable": true,
    "move_files_destination": "%(seriesname)s",
    "move_files_fullpath_replacements": [
        {"is_regex": true,
        "match": "Scr.*?s",
        "replacement": "A Test"}
    ],
    "always_rename": true,
    "select_first": true
}
""")

    expected_files = ['A Test/A Test - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)
