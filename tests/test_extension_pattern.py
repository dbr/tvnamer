#!/usr/bin/env python

"""Tests multi-episode filename generation
"""

from functional_runner import run_tvnamer, verify_out_data
from helpers import attr


@attr("functional")
def test_extension_pattern_default():
    """Test default extension handling, no language codes
    """

    conf = r"""
    {"extension_pattern": "(\\.[a-zA-Z0-9]+)$",
    "batch": true,
    "valid_extensions": ["avi", "srt"]}
    """

    input_files = [
        "scrubs.s01e01.hdtv.fake.avi",
        "scrubs.s01e01.hdtv.fake.srt",
        "my.name.is.earl.s01e01.fake.avi",
        "my.name.is.earl.s01e01.some.other.fake.eng.srt",
    ]
    expected_files = [
        "Scrubs - [01x01] - My First Day.avi",
        "Scrubs - [01x01] - My First Day.srt",
        "My Name Is Earl - [01x01] - Pilot.avi",
        "My Name Is Earl - [01x01] - Pilot.srt",
    ]

    out_data = run_tvnamer(
        with_files = input_files,
        with_config = conf,
        with_input = "")

    verify_out_data(out_data, expected_files)

@attr("functional")
def test_extension_pattern_custom():
    """Test custom extension pattern, multiple language codes
    """

    conf = r"""
    {"extension_pattern": "((\\.|-)(eng|cze|EN|CZ)(?=\\.(sub|srt)))?(\\.[a-zA-Z0-9]+)$",
    "batch": true,
    "valid_extensions": ["avi", "srt"]}
    """

    input_files = [
        "scrubs.s01e01.hdtv.fake.avi",
        "scrubs.s01e01.hdtv.fake.srt",
        "scrubs.s01e01.hdtv.fake-CZ.srt",
        "scrubs.s01e01.hdtv.fake-EN.srt",
        "my.name.is.earl.s01e01.fake.avi",
        "my.name.is.earl.s01e01.some.other.fake.eng.srt",
        "my.name.is.earl.s01e01.fake.cze.srt",
    ]
    expected_files = [
        "Scrubs - [01x01] - My First Day.avi",
        "Scrubs - [01x01] - My First Day.srt",
        "Scrubs - [01x01] - My First Day-CZ.srt",
        "Scrubs - [01x01] - My First Day-EN.srt",
        "My Name Is Earl - [01x01] - Pilot.avi",
        "My Name Is Earl - [01x01] - Pilot.eng.srt",
        "My Name Is Earl - [01x01] - Pilot.cze.srt",
    ]

    out_data = run_tvnamer(
        with_files = input_files,
        with_config = conf,
        with_input = "")

    verify_out_data(out_data, expected_files)
