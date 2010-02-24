#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Tests moving renamed files
"""

from functional_runner import run_tvnamer, verify_out_data


def test_simple_realtive_move():
    """Move file to simple relative static dir
    """

    conf = """
    {"move_files_enable": true,
    "move_files_destination": "test/",
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['test/Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


def test_dynamic_destination():
    """Move file to simple relative static dir
    """

    conf = """
    {"move_files_enable": true,
    "move_files_destination": "tv/%(seriesname)s/season %(seasonnumber)d/",
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_config = conf)

    expected_files = ['tv/Scrubs/season 1/Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


def test_cli_destination():
    """Tests specifying the destination via command line argument
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_flags = ['--batch', '--move', '--movedestination=season %(seasonnumber)d/'])

    expected_files = ['season 1/Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)
