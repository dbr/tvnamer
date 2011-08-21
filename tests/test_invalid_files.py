#!/usr/bin/env python


"""Ensure that invalid files (non-episodes) are not renamed
"""

from functional_runner import run_tvnamer, verify_out_data
from nose.plugins.attrib import attr


@attr("functional")
def test_simple_single_file():
    """Files without series name should be skipped
    """

    out_data = run_tvnamer(
        with_files = ['S01E02 - Some File.avi'],
        with_flags = ["--batch"])

    expected_files = ['S01E02 - Some File.avi']

    verify_out_data(out_data, expected_files, expected_returncode = 2)
