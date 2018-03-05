#!/usr/bin/env python

"""Tests custom replacements on input/output files
"""

from functional_runner import run_tvnamer, verify_out_data
from helpers import attr


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

    expected_files = ['Law and Order - [01x01] - Prescription for Death.avi']

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


@attr("functional")
def test_restoring_dot():
    """Test replace the parsed "Tosh 0" with "Tosh.0"
    """
    out_data = run_tvnamer(
        with_files = ['tosh.0.s03.e02.avi'],
        with_config = """
{
    "input_filename_replacements": [
        {"is_regex": false,
        "match": "tosh.0",
        "replacement": "tosh0"}
    ],
    "always_rename": true,
    "select_first": true
}
""")

    expected_files = ['Tosh.0 - [03x02] - Brian Atene.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_replacement_order():
    """Ensure output replacements happen before the valid filename function is run
    """
    out_data = run_tvnamer(
        with_files = ['24.s03.e02.avi'],
        with_config = """
{
    "output_filename_replacements": [
        {"is_regex": false,
        "match": ":",
        "replacement": "-"}
    ],
    "always_rename": true,
    "select_first": true
}
""")

    expected_files = ['24 - [03x02] - Day 3- 2-00 P.M. - 3-00 P.M..avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_replacement_preserve_extension():
    """Ensure with_extension replacement option defaults to preserving extension
    """
    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_config = """
{
    "output_filename_replacements": [
        {"is_regex": false,
        "match": "avi",
        "replacement": "ohnobroken"}
    ],
    "always_rename": true,
    "select_first": true
}
""")

    expected_files = ['Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_replacement_including_extension():
    """Option to allow replacement search/replace to include file extension
    """
    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_config = """
{
    "output_filename_replacements": [
        {"is_regex": false,
        "with_extension": true,
        "match": "Day.avi",
        "replacement": "Day.nl.avi"}
    ],
    "always_rename": true,
    "select_first": true
}
""")

    expected_files = ['Scrubs - [01x01] - My First Day.nl.avi']

    verify_out_data(out_data, expected_files)
