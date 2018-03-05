#!/usr/bin/env python

"""Functional tests for tvnamer tests
"""

import os
from functional_runner import run_tvnamer, verify_out_data
from helpers import attr
import pytest


@attr("functional")
def test_simple_single_file():
    """Test most simple usage
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_input = "1\ny\n")

    expected_files = ['Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_simple_multiple_files():
    """Tests simple interactive usage with multiple files
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
        with_input = "y\n1\ny\n1\ny\n1\ny\ny\n")

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_simple_batch_functionality():
    """Tests renaming single files at a time, in batch mode
    """

    tests = [
        {'in':'scrubs.s01e01.hdtv.fake.avi',
        'expected':'Scrubs - [01x01] - My First Day.avi'},
        {'in':'my.name.is.earl.s01e01.fake.avi',
        'expected':'My Name Is Earl - [01x01] - Pilot.avi'},
        {'in':'a.fake.show.s12e24.fake.avi',
        'expected':'a.fake.show.s12e24.fake.avi'},
        {'in': 'total.access.s01e01.avi',
        'expected': 'Total Access 24_7 - [01x01] - Episode #1.avi'},
    ]

    for curtest in tests:

        print("Expecting %r to turn into %r" % (
            curtest['in'], curtest['expected']))
        out_data = run_tvnamer(
            with_files = [curtest['in'], ],
            with_flags = ['--batch'],
        )
        verify_out_data(out_data, [curtest['expected'], ])


@attr("functional")
def test_interactive_always_option():
    """Tests the "a" always rename option in interactive UI
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
        with_flags = ["--selectfirst"],
        with_input = "a\n")

    verify_out_data(out_data, expected_files)


@attr("functional")
@pytest.mark.skipif(os.getenv("TRAVIS", "false")=="true", reason="Test fails for some reason on Travis-CI")
def test_unicode_in_inputname():
    """Tests parsing a file with unicode in the input filename
    """

    import os, sys
    if os.getenv("TRAVIS", "false") == "true" and sys.version_info[0:2] == (2.6):
        from nose.plugins.skip import SkipTest
        raise SkipTest("Ignoring test which triggers bizarre bug in nosetests, in python 2.6, only on travis.")


    input_files = [
        u'The Big Bang Theory - S02E07 - The Panty Pin\u0303ata Polarization.avi']

    expected_files = [
        u'The Big Bang Theory - [02x07] - The Panty Pin\u0303ata Polarization.avi']

    out_data = run_tvnamer(
        with_files = input_files,
        with_flags = ["--batch"])

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_unicode_in_search_results():
    """Show with unicode in search results
    """
    input_files = [
        'psych.s04e11.avi']

    expected_files = [
        'Psych - [04x11] - Thrill Seekers and Hell-Raisers.avi']

    out_data = run_tvnamer(
        with_files = input_files,
        with_input = '1\ny\n')

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_renaming_always_doesnt_overwrite():
    """If trying to rename a file that exists, should not create new file
    """
    input_files = [
        'Scrubs.s01e01.avi',
        'Scrubs - [01x01] - My First Day.avi']

    expected_files = [
        'Scrubs.s01e01.avi',
        'Scrubs - [01x01] - My First Day.avi']

    out_data = run_tvnamer(
        with_files = input_files,
        with_flags = ['--batch'])

    verify_out_data(out_data, expected_files)


@attr("functional")
@pytest.mark.skipif(os.getenv("TRAVIS", "false")=="true", reason="Test fails for some reason on Travis-CI")
def test_not_overwritting_unicode_filename():
    """Test no error occurs when warning about a unicode filename being overwritten
    """
    input_files = [
        u'The Big Bang Theory - S02E07.avi',
        u'The Big Bang Theory - [02x07] - The Panty Pin\u0303ata Polarization.avi']

    expected_files = [
        u'The Big Bang Theory - S02E07.avi',
        u'The Big Bang Theory - [02x07] - The Panty Pin\u0303ata Polarization.avi']

    out_data = run_tvnamer(
        with_files = input_files,
        with_flags = ['--batch'])

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_not_recursive():
    """Tests the nested files aren't found when not recursive
    """
    input_files = [
        'Scrubs.s01e01.avi',
        'nested/subdir/Scrubs.s01e02.avi']

    expected_files = [
        'Scrubs - [01x01] - My First Day.avi',
        'nested/subdir/Scrubs.s01e02.avi']

    out_data = run_tvnamer(
        with_files = input_files,
        with_flags = ['--not-recursive', '--batch'],
        run_on_directory = True)

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_correct_filename():
    """If the filename is already correct, don't prompt
    """

    out_data = run_tvnamer(
        with_files = ['Scrubs - [01x01] - My First Day.avi'],
        with_input = "1\ny\n")

    expected_files = ['Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_filename_already_exists():
    """Don't overwrite
    """

    out_data = run_tvnamer(
        with_files = ['Scrubs - [01x01] - My First Day.avi', 'scrubs.s01e01.avi'],
        with_input = "1\ny\n")

    expected_files = ['Scrubs - [01x01] - My First Day.avi', 'scrubs.s01e01.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_no_seasonnumber():
    """Test episode with no series number
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.e01.avi'],
        with_flags = ['--batch'])

    expected_files = ['Scrubs - [01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_skipping_after_replacements():
    """When custom-replacement is specified, should still skip file if name is correct
    """

    conf = """
    {"select_first": true,
    "input_filename_replacements": [
        {"is_regex": false,
        "match": "v",
        "replacement": "u"}
    ],
    "output_filename_replacements": [
        {"is_regex": false,
        "match": "u",
        "replacement": "v"}
    ]
    }
    """

    out_data = run_tvnamer(
        with_files = ['Scrvbs - [01x01] - My First Day.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['Scrvbs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)

@attr("functional")
def test_dvd_order():
    """Tests TvDB dvd order naming
    """

    input_files = [
        'batman the animated series s01e01.xvid']

    expected_files = [
        'Batman - The Animated Series - [01x01] - On Leather Wings.xvid']

    conf = r"""
    {
      "output_filename_replacements": [
        {"is_regex": true,
        "match": ": ",
        "replacement": " - "}
      ]
    }
    """

    out_data = run_tvnamer(
        with_files = input_files,
        with_flags = ["--order", 'dvd'],
        with_input = "1\ny\n",
        with_config = conf)

    verify_out_data(out_data, expected_files)
