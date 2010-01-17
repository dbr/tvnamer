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


def test_simple_multiple_files():
    """Tests simple usage with multiple files
    """
    input_files = [
        'scrubs.s01e01.hdtv.fake.avi',
        'my.name.is.earl.s01e01.fake.avi',
        'a.fake.show.s12e24.fake.avi',
        'total.access.s01e01.avi']

    expected_files = [
        'Scrubs - [01x01] - My First Day.avi',
        'My Name Is Earl - [01x01] - Pilot.avi',
        'a fake show - [12x24].avi',
         'Total Access 24_7 - [01x01] - Episode #1.avi']

    out_data = run_tvnamer(
        with_files = input_files,
        with_input = "y\n1\ny\n1\ny\n1\ny\n"
    )

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
