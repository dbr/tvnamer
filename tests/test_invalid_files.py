#!/usr/bin/env python

"""Ensure that invalid files (non-episodes) are not renamed
"""

from functional_runner import run_tvnamer, verify_out_data
from helpers import attr


@attr("functional")
def test_simple_single_file():
    """Boring example
    """

    out_data = run_tvnamer(
        with_files = ['Some File.avi'],
        with_flags = ["--batch"])

    expected_files = ['Some File.avi']

    verify_out_data(out_data, expected_files, expected_returncode = 2)


@attr("functional")
def test_no_series_name():
    """File without series name should be skipped (unless '--name=MySeries' arg is supplied)
    """

    out_data = run_tvnamer(
        with_files = ['s01e01 Some File.avi'],
        with_flags = ["--batch"])

    expected_files = ['s01e01 Some File.avi']

    verify_out_data(out_data, expected_files, expected_returncode = 2)


@attr("functional")
def test_ambigious():
    invalid_files = [
        'show.123.avi', # Maybe s01e23 but too ambigious. #140
        'Scrubs.0101.avi', # Ambigious. #140
    ]

    for f in invalid_files:
        out_data = run_tvnamer(
            with_files = [f],
            with_flags = ["--batch"])

        expected_files = [f]

        verify_out_data(out_data, expected_files, expected_returncode = 2)
