#!/usr/bin/env python

"""Tests moving renamed files
"""

from functional_runner import run_tvnamer, verify_out_data
from helpers import attr


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
    {"move_files_enable": true,
    "move_files_destination": "%(seriesname)s",
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
def test_move_files_lowercase_destination():
    """Test move_files_lowercase_destination configuration option.
    """

    conf = """
    {"move_files_enable": true,
    "move_files_destination": "Test/This/%(seriesname)s/S%(seasonnumber)02d",
    "move_files_lowercase_destination": true,
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.This.Is.a.Test.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['Test/This/scrubs/S01/Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_move_date_based_episode():
    """Moving a date-base episode (lighthouse ticket #56)
    """

    conf = """
    {"move_files_enable": true,
    "move_files_destination_date": "Test/%(seriesname)s/%(year)s/%(month)s/%(day)s",
    "move_files_lowercase_destination": true,
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['The Colbert Report - 2011-09-28 Ken Burns.avi'],
        with_config = conf,
        with_input = "")

    expected_files = ['Test/The Colbert Report/2011/9/28/The Colbert Report - [2011-09-28] - Ken Burns.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_move_files_full_filepath_simple():
    """Moving file destination including a fixed filename
    """

    conf = """
    {"move_files_enable": true,
    "move_files_destination": "TestDir/%(seriesname)s/season %(seasonnumber)02d/%(episodenumbers)s/SpecificName.avi",
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
    {"move_files_enable": true,
    "move_files_destination": "TestDir/%(seriesname)s/season %(seasonnumber)02d/%(episodenumbers)s/%(originalfilename)s",
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
    {"move_files_enable": true,
    "move_files_destination": "SubDir",
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
    {"move_files_enable": true,
    "move_files_destination": "SubDir",
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['Scrubs - [02] - My Mentor.avi'],
        with_config = conf,
        with_input = "y\n")

    expected_files = ['SubDir/Scrubs - [02] - My Mentor.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_move_files_only():
    """With parameter move_files_only set to true files should be moved and not renamed
    """

    conf = """
    {"move_files_only": true,
    "move_files_enable": true,
    "move_files_destination": "tv/%(seriesname)s/season %(seasonnumber)d/",
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_config = conf)

    expected_files = ['tv/Scrubs/season 1/scrubs.s01e01.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_forcefully_moving_enabled():
    """Forcefully moving files, overwriting destination
    """

    conf = """
    {"move_files_enable": true,
    "move_files_destination": "tv/%(seriesname)s/season %(seasonnumber)d/",
    "batch": true,
    "overwrite_destination_on_move": true}
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
    {"move_files_enable": true,
    "move_files_destination": "tv/%(seriesname)s/season %(seasonnumber)d/",
    "batch": true,
    "overwrite_destination_on_move": false}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'scrubs - [01x01].avi'],
        with_config = conf)

    expected_files = [
        'Scrubs - [01x01] - My First Day.avi',
        'tv/Scrubs/season 1/Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_forcefully_moving_default():
    """Ensure default is not overwrite destination
    """

    conf = """
    {"move_files_enable": true,
    "move_files_destination": "tv/%(seriesname)s/season %(seasonnumber)d/",
    "batch": true}
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi', 'scrubs - [01x01].avi'],
        with_config = conf)

    expected_files = [
        'Scrubs - [01x01] - My First Day.avi',
        'tv/Scrubs/season 1/Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)
