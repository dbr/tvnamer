#!/usr/bin/env python

"""Tests multi-episode filename generation
"""

from functional_runner import run_tvnamer, verify_out_data
from helpers import attr


@attr("functional")
def test_multiep_different_names():
    """Default config - two different names are joined with 'multiep_join_name_with', 'multiep_format' doesn't matter
    """

    conf = """
    {
    "output_filename_replacements": [
        {"is_regex": false,
        "match": ":",
        "replacement": " -"}
    ],

    "multiep_join_name_with": ", ",
    "batch": true,
    "multiep_format": "%(foo)s"}
    """

    out_data = run_tvnamer(
        with_files = ["star.trek.enterprise.s01e03e04.avi"],
        with_config = conf,
        with_input = "")

    expected_files = ['Star Trek - Enterprise - [01x03-04] - Fight or Flight, Strange New World.avi']

    verify_out_data(out_data, expected_files)

@attr("functional")
def test_multiep_same_names():
    """Default config - same names, format according to 'multiep_format', 'multiep_join_name_with' doesn't matter
    """

    conf = """
    {
    "output_filename_replacements": [
        {"is_regex": false,
        "match": ":",
        "replacement": " -"}
    ],
    "multiep_join_name_with": ", ",
    "batch": true,
    "multiep_format": "%(epname)s (%(episodemin)s-%(episodemax)s)"}
    """

    out_data = run_tvnamer(
        with_files = ["star.trek.enterprise.s01e01e02.avi"],
        with_config = conf,
        with_input = "")

    expected_files = ['Star Trek - Enterprise - [01x01-02] - Broken Bow (1-2).avi']

    verify_out_data(out_data, expected_files)

@attr("functional")
def test_multiep_same_names_without_number():
    """Default config - same names, ensure that missing number doesn't matter
    """

    conf = """
    {
    "output_filename_replacements": [
        {"is_regex": false,
        "match": ":",
        "replacement": " -"}
    ],

    "multiep_join_name_with": ", ",
    "batch": true,
    "multiep_format": "%(epname)s (Parts %(episodemin)s-%(episodemax)s)"}
    """

    out_data = run_tvnamer(
        with_files = ["star.trek.deep.space.nine.s01e01e02.avi"],
        with_config = conf,
        with_input = "")

    expected_files = ['Star Trek - Deep Space Nine - [01x01-02] - Emissary (Parts 1-2).avi']

    verify_out_data(out_data, expected_files)
