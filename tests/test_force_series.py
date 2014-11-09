#!/usr/bin/env python

"""Test ability to set the series name by series id
"""

from functional_runner import run_tvnamer, verify_out_data
from helpers import attr


@attr("functional")
def test_series_id():
    """Test --series-id argument
    """

    conf = """
    {"always_rename": true,
    "select_first": true}
    """

    out_data = run_tvnamer(
        with_files = ['whatever.s01e01.avi'],
        with_config = conf,
        with_flags = ["--series-id", '76156'],
        with_input = "")

    expected_files = ['Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_series_id_with_nameless_series():
    """Test --series-id argument with '6x17.etc.avi' type filename
    """

    conf = """
    {"always_rename": true,
    "select_first": true}
    """

    out_data = run_tvnamer(
        with_files = ['s01e01.avi'],
        with_config = conf,
        with_flags = ["--series-id", '76156'],
        with_input = "")

    expected_files = ['Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)
