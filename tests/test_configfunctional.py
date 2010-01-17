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


def test_batchconfig():
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
<tvnamer version="1">
  <option name="alwaysrename" type="bool">True</option>
  <option name="selectfirst" type="bool">True</option>
</tvnamer>"""

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)
