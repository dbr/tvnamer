#!/usr/bin/env python

"""Tests moving renamed files
"""

from functional_runner import run_tvnamer, verify_out_data
from nose.plugins.attrib import attr


@attr("functional")
def test_simple_realtive_move():
    """Move file to simple relative static dir
    """

    conf = """
    {"move_files_destination": "test/",
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
    {"move_files_destination": "tv/%(seriesname)s/season %(seasonnumber)d/",
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
        with_flags = ['--batch', '--movedestination=season %(seasonnumber)d/'])

    expected_files = ['season 1/Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_move_interactive_allyes():
    """Tests interactive UI for moving all files
    """

    conf = """
    {"move_files_destination": "test",
    "batch": false}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'scrubs.s01e02.avi'],
        with_config = conf,
        with_input = "1\ny\n1\ny\n")

    expected_files = ['test/Scrubs - [01x01] - My First Day.avi',
        'test/Scrubs - [01x02] - My Mentor.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_move_interactive_allno():
    """Tests interactive UI allows not moving any files
    """

    conf = """
    {"move_files_destination": "test",
    "batch": false}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'scrubs.s01e02.avi'],
        with_config = conf,
        with_input = "1\nn\n1\nn\n")

    expected_files = ['scrubs.s01e01.avi', 'scrubs.s01e02.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_move_interactive_somefiles():
    """Tests interactive UI allows not renaming some files

    Rename and move first file, don't rename second file (so no move), and
    rename but do not move last file (Input is: y/y, n, y/n)
    """

    conf = """
    {"move_files_destination": "test",
    "batch": false}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'scrubs.s01e02.avi'],
        with_config = conf,
        with_input = "1\ny\n1\nn\n")

    expected_files = ['test/Scrubs - [01x01] - My First Day.avi',
        'scrubs.s01e02.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_with_invalid_seriesname():
    """Tests series name containing invalid filename characters
    """

    conf = """
    {"move_files_destination": "%(seriesname)s",
    "batch": true,
    "windows_safe_filenames": true}
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
    {"move_files_destination": "%(seriesname)s",
    "batch": true,
    "move_files_fullpath_replacements": [
         {"is_regex": true,
          "match": "CSI_ Miami",
          "replacement": "CSI"}],
    "windows_safe_filenames": true}
    """

    out_data = run_tvnamer(
        with_files = ['csi.miami.s01e01.avi'],
        with_config = conf)

    expected_files = ['CSI/CSI - [01x01] - Golden Parachute.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_titlecase_dynamic_parts():
    """Test titlecase_dynamic_parts configuration option.
    """

    conf = """
    {"move_files_destination": "Test/This/%(seriesname)s/S%(seasonnumber)02d",
    "titlecase_dynamic_parts": true,
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.This.Is.a.Test.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['Test/This/Scrubs/S01/Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_lowercase_dynamic_parts():
    """Test lowercase_dynamic_parts configuration option.
    """

    conf = """
    {"move_files_destination": "Test/This/%(seriesname)s/S%(seasonnumber)02d",
    "lowercase_dynamic_parts": true,
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.This.Is.a.Test.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['Test/This/scrubs/S01/scrubs - [01x01] - my first day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_lowercase_dynamic_parts_originalfilename():
    """Test lowercase_dynamic_parts does not change %(originalfilename)
    """

    conf = """
    {"move_files_destination": "Test/This/%(seriesname)s/S%(seasonnumber)02d/%(originalfilename)s",
    "move_files_destination_is_filepath": true,
    "lowercase_dynamic_parts": true,
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.This.Is.a.Test.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['Test/This/scrubs/S01/scrubs.s01e01.This.Is.a.Test.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_move_date_based_episode():
    """Moving a date-base episode (lighthouse ticket #56)
    """

    conf = """
    {"move_files_destination_date": "Test/%(seriesname)s/%(year)s/%(month)s/%(day)s",
    "lowercase_dynamic_parts": true,
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['The Colbert Report - 2011-09-28 Ken Burns.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['Test/the colbert report/2011/9/28/the colbert report - [2011-09-28] - ken burns.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_move_files_full_filepath_simple():
    """Moving file destination including a fixed filename
    """

    conf = """
    {"move_files_destination": "TestDir/%(seriesname)s/season %(seasonnumber)02d/%(episode)s/SpecificName.avi",
    "move_files_destination_is_filepath": true,
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e02.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['TestDir/Scrubs/season 01/02/SpecificName.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_move_files_full_filepath_with_origfilename():
    """Moving file destination including a filename
    """

    conf = """
    {"move_files_destination": "TestDir/%(seriesname)s/season %(seasonnumber)02d/%(episode)s/%(originalfilename)s",
    "move_files_destination_is_filepath": true,
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'scrubs.s01e02.avi'],
        with_config = conf,
        with_input = "")

    expected_files = [
        'TestDir/Scrubs/season 01/01/scrubs.s01e01.avi',
        'TestDir/Scrubs/season 01/02/scrubs.s01e02.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_move_with_correct_name():
    """Files with correct name should still be moved
    """

    conf = """
    {"move_files_destination": "SubDir",
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['Scrubs - [01x02] - My Mentor.avi'],
        with_config = conf,
        with_input = "y\n")

    expected_files = ['SubDir/Scrubs - [01x02] - My Mentor.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_move_no_season():
    """Files with no season number should moveable [#94]
    """

    conf = """
    {"move_files_destination": "SubDir",
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['Scrubs - [02] - My Mentor.avi'],
        with_config = conf,
        with_input = "y\n")

    expected_files = ['SubDir/Scrubs - [02] - My Mentor.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_forcefully_moving_enabled():
    """Forcefully moving files, overwriting destination
    """

    conf = """
    {"move_files_destination": "tv/%(seriesname)s/season %(seasonnumber)d/",
    "batch": true,
    "overwrite_destination": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'Scrubs - [01x01] - My First Day.avi'],
        with_config = conf)

    expected_files = ['tv/Scrubs/season 1/Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_forcefully_moving_disabled():
    """Explicitly disable forcefully moving files
    """

    conf = """
    {"move_files_destination": ".",
    "batch": true,
    "overwrite_destination": false}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'Scrubs - [01x01] - My First Day.avi'],
        with_config = conf)

    expected_files = [
        'scrubs.s01e01.avi',
        'Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_forcefully_moving_default():
    """Ensure default is not overwrite destination
    """

    conf = """
    {"move_files_destination": ".",
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'Scrubs - [01x01] - My First Day.avi'],
        with_config = conf)

    expected_files = [
        'scrubs.s01e01.avi',
        'Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)
