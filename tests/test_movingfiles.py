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
    """
    """

    conf = """
    {"move_files_enable": true,
    "move_files_desination": "test/",
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['test/Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)
