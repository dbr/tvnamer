#!/usr/bin/env python

""" Tests interactive mode of tvnamer
"""

from functional_runner import run_tvnamer, verify_out_data
from nose.plugins.attrib import attr


@attr("functional")
def test_simple_single_file():
    """Test simple interactive usage with single file
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
        'total.access.247.s01e01.avi']

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
    """Tests simple batch mode, interactive mode explicitly disabled
    """

    tests = [
        {'in':'scrubs.s01e01.hdtv.fake.avi',
        'expected':'Scrubs - [01x01] - My First Day.avi'},
        {'in':'my.name.is.earl.s01e01.fake.avi',
        'expected':'My Name Is Earl - [01x01] - Pilot.avi'},
        {'in':'a.fake.show.s12e24.fake.avi',
        'expected':'a.fake.show.s12e24.fake.avi'},
        {'in': 'total.access.247.s01e01.avi',
        'expected': 'Total Access 24_7 - [01x01] - Episode #1.avi'},
    ]

    for curtest in tests:

        def _the_test():
            out_data = run_tvnamer(
                with_files = [curtest['in'], ],
                with_flags = ['--batch'],
            )
            verify_out_data(out_data, [curtest['expected'], ])

        _the_test.description = "test_simple_functionality_%s" % curtest['in']
        yield _the_test


@attr("functional")
def test_interactive_always_option():
    """Tests the "a" always rename option in interactive UI
    """

    input_files = [
        'scrubs.s01e01.hdtv.fake.avi',
        'my.name.is.earl.s01e01.fake.avi',
        'a.fake.show.s12e24.fake.avi',
        'total.access.247.s01e01.avi']

    expected_files = [
        'Scrubs - [01x01] - My First Day.avi',
        'My Name Is Earl - [01x01] - Pilot.avi',
        'a fake show - [12x24].avi',
         'Total Access 24_7 - [01x01] - Episode #1.avi']

    out_data = run_tvnamer(
        with_files = input_files,
        with_input = "1\na\n1\n1\n1\n")

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
    """If the filename is already correct, don't prompt
    """

    out_data = run_tvnamer(
        with_files = ['Scrubs - [01x01] - My First Day.avi', 'scrubs.s01e01.avi'],
        with_input = "1\ny\n")

    expected_files = ['Scrubs - [01x01] - My First Day.avi', 'scrubs.s01e01.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_skipping_after_replacements():
    """When custom-replacement is specified, should still skip file if name is correct
    """

    conf = """
    {"batch": true,
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
