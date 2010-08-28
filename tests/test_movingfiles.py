#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Tests moving renamed files
"""

from functional_runner import run_tvnamer, verify_out_data
from nose.plugins.attrib import attr


@attr("functional")
def test_simple_realtive_move():
    """Move file to simple relative static dir
    """

    conf = """
    {"move_files_enable": true,
    "move_files_destination": "test/",
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['test/Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_dynamic_destination():
    """Move file to simple relative static dir
    """

    conf = """
    {"move_files_enable": true,
    "move_files_destination": "tv/%(seriesname)s/season %(seasonnumber)d/",
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_config = conf)

    expected_files = ['tv/Scrubs/season 1/Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_cli_destination():
    """Tests specifying the destination via command line argument
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_flags = ['--batch', '--move', '--movedestination=season %(seasonnumber)d/'])

    expected_files = ['season 1/Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_move_interactive_allyes():
    """Tests interactive UI for moving all files
    """

    conf = """
    {"move_files_enable": true,
    "move_files_destination": "test",
    "select_first": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'scrubs.s01e02.avi'],
        with_config = conf,
        with_input = "y\ny\ny\ny\n")

    expected_files = ['test/Scrubs - [01x01] - My First Day.avi',
        'test/Scrubs - [01x02] - My Mentor.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_move_interactive_allno():
    """Tests interactive UI allows not moving any files
    """

    conf = """
    {"move_files_enable": true,
    "move_files_destination": "test",
    "select_first": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'scrubs.s01e02.avi'],
        with_config = conf,
        with_input = "y\nn\ny\nn\n")

    expected_files = ['Scrubs - [01x01] - My First Day.avi',
        'Scrubs - [01x02] - My Mentor.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_move_interactive_somefiles():
    """Tests interactive UI allows not renaming some files, renaming/moving others

    Rename and move first file, don't rename second file (so no move), and
    rename but do not move last file (Input is: y/y, n, y/n)
    """

    conf = """
    {"move_files_enable": true,
    "move_files_destination": "test",
    "select_first": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'scrubs.s01e02.avi', 'scrubs.s01e03.avi'],
        with_config = conf,
        with_input = "y\ny\nn\ny\nn\n")

    expected_files = ['test/Scrubs - [01x01] - My First Day.avi',
        'scrubs.s01e02.avi',
        'Scrubs - [01x03] - My Best Friend\'s Mistake.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_with_invalid_seriesname():
    """Tests series name containing invalid filename characters
    """

    conf = """
    {"move_files_enable": true,
    "move_files_destination": "%(seriesname)s",
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['csi.miami.s01e01.avi'],
        with_config = conf)

    expected_files = ['CSI_ Miami/CSI_ Miami - [01x01] - Golden Parachute.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_with_invalid_seriesname_test2():
    """Another test for series name containing invalid filename characters
    """

    conf = """
    {"move_files_enable": true,
    "move_files_destination": "%(seriesname)s",
    "batch": true,
    "move_files_fullpath_replacements": [
         {"is_regex": true,
          "match": "CSI_ Miami",
          "replacement": "CSI"}]
    }
    """

    out_data = run_tvnamer(
        with_files = ['csi.miami.s01e01.avi'],
        with_config = conf)

    expected_files = ['CSI/CSI - [01x01] - Golden Parachute.avi']

    verify_out_data(out_data, expected_files)
