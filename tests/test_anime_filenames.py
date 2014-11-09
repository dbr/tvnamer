#!/usr/bin/env python

"""Tests anime filename output
"""

from functional_runner import run_tvnamer, verify_out_data
from helpers import attr


@attr("functional")
def test_group():
    """Anime filename [#100]
    """
    out_data = run_tvnamer(
        with_files = ['[Some Group] Scrubs - 01 [A1B2C3].avi'],
        with_config = """
{
    "always_rename": true,
    "select_first": true,

    "filename_anime_with_episode": "[%(group)s] %(seriesname)s - %(episodenumber)s - %(episodename)s [%(crc)s]%(ext)s"
}
""")

    expected_files = ['[Some Group] Scrubs - 01 - My First Day [A1B2C3].avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_group_no_epname():
    """Anime filename, on episode with no name [#100]
    """
    out_data = run_tvnamer(
        with_files = ['[Some Group] Somefakeseries - 01 [A1B2C3].avi'],
        with_config = """
{
    "always_rename": true,
    "select_first": true,

    "filename_anime_without_episode": "[%(group)s] %(seriesname)s - %(episodenumber)s [%(crc)s]%(ext)s"
}
""")

    expected_files = ['[Some Group] Somefakeseries - 01 [A1B2C3].avi']

    verify_out_data(out_data, expected_files)
