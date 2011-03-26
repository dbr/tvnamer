#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Tests ignoreing files by regexp (e.g. all files with "sample" in the name)
"""

from functional_runner import run_tvnamer, verify_out_data
from nose.plugins.attrib import attr


@attr("functional")
def test_no_blacklist():
    """Tests empty list of filename regexps is parsed as expected
    """

    conf = """
    {"always_rename": true,
    "select_first": true,
    "filename_blacklist": []}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'scrubs.s01e02.avi'],
        with_config = conf)

    expected_files = [
        'Scrubs - [01x01] - My First Day.avi',
        'Scrubs - [01x02] - My Mentor.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_partial_blacklist_using_simple_match():
    """Tests single match of filename blacklist using a simple match
    """

    conf = """
    {"always_rename": true,
    "select_first": true,
    "filename_blacklist": [
        {"is_regex": false,
         "match": "s02e01"}
        ]
    }
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'scrubs.s02e01.avi', 'scrubs.s02e02.avi'],
        with_config = conf)

    expected_files = [
        'Scrubs - [01x01] - My First Day.avi',
        'scrubs.s02e01.avi',
        'Scrubs - [02x02] - My Nightingale.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_partial_blacklist_using_regex():
    """Tests single match of filename blacklist using a regex match
    """

    conf = """
    {"always_rename": true,
    "select_first": true,
    "filename_blacklist": [
        {"is_regex": true,
         "match": ".*s02e01.*"}
        ]
    }
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'scrubs.s02e01.avi', 'scrubs.s02e02.avi'],
        with_config = conf)

    expected_files = [
        'Scrubs - [01x01] - My First Day.avi',
        'scrubs.s02e01.avi',
        'Scrubs - [02x02] - My Nightingale.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_partial_blacklist_using_mix():
    """Tests single match of filename blacklist using a mix of regex and simple match
    """

    conf = """
    {"always_rename": true,
    "select_first": true,
    "filename_blacklist": [
        {"is_regex": true,
         "match": ".*s02e01.*"},
        {"is_regex": false,
         "match": "s02e02"}
        ]
    }
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'scrubs.s02e01.avi', 'scrubs.s02e02.avi'],
        with_config = conf)

    expected_files = [
        'Scrubs - [01x01] - My First Day.avi',
        'scrubs.s02e01.avi',
        'scrubs.s02e02.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_full_blacklist():
    """Tests complete blacklist of all filenames with a regex
    """

    conf = """
    {"always_rename": true,
    "select_first": true,
    "filename_blacklist": [
        {"is_regex": true,
         "match": ".*"}
        ]
    }
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'scrubs.s02e01.avi', 'scrubs.s02e02.avi'],
        with_config = conf)

    expected_files = ['scrubs.s01e01.avi', 'scrubs.s02e01.avi', 'scrubs.s02e02.avi']

    verify_out_data(out_data, expected_files, expected_returncode = 2)
