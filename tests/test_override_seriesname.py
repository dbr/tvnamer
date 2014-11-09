#!/usr/bin/env python

"""Test ability to override the series name
"""

from functional_runner import run_tvnamer, verify_out_data
from helpers import attr


@attr("functional")
def test_temp_override():
    """Test --name argument
    """

    conf = """
    {"always_rename": true,
    "select_first": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_config = conf,
        with_flags = ["--name", "lost"],
        with_input = "")

    expected_files = ['Lost - [01x01] - Pilot (1).avi']

    verify_out_data(out_data, expected_files)
