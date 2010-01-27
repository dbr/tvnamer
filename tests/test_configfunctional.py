#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Tests various configs load correctly
"""

from functional_runner import run_tvnamer, verify_out_data


def test_simple_single_file():
    """Test most simple usage
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_input = "1\ny\n")

    expected_files = ['Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


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


def test_skip_file_on_error():
    """Test the "skip file on error" config option works
    """

    conf = """
    {"skip_file_on_error": true,
    "always_rename":true}
    """

    out_data = run_tvnamer(
        with_files = ['a.fake.episode.s01e01.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['a.fake.episode.s01e01.avi']

    verify_out_data(out_data, expected_files)


def test_do_not_skip_file_on_error():
    """Test setting "skip file on error" config option to False
    """

    conf = """
    {"skip_file_on_error": false,
    "always_rename":true}
    """

    out_data = run_tvnamer(
        with_files = ['a.fake.episode.s01e01.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['a fake episode - [01x01].avi']

    verify_out_data(out_data, expected_files)
