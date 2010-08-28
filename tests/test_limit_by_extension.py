#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Tests the valid_extensions config option
"""

from functional_runner import run_tvnamer, verify_out_data
from nose.plugins.attrib import attr


@attr("functional")
def test_no_extensions():
    """Tests empty list of extensions is parsed as expected
    """

    conf = """
    {"always_rename": true,
    "select_first": true,
    "valid_extensions": []}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'scrubs.s01e02.mkv'],
        with_config = conf)

    expected_files = [
        'Scrubs - [01x01] - My First Day.avi',
        'Scrubs - [01x02] - My Mentor.mkv']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_single_extensions():
    """Tests one valid extension with multiple files
    """

    conf = """
    {"always_rename": true,
    "select_first": true,
    "valid_extensions": ["mkv"]}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'scrubs.s01e02.mkv'],
        with_config = conf)

    expected_files = [
        'scrubs.s01e01.avi',
        'Scrubs - [01x02] - My Mentor.mkv']

    verify_out_data(out_data, expected_files)
