#!/usr/bin/env python

"""Test the function to create safe filenames
"""

import platform

from helpers import assertEquals

from tvnamer.utils import make_valid_filename


def test_basic():
    """Test make_valid_filename does not mess up simple filenames
    """
    assertEquals(make_valid_filename("test.avi"), "test.avi")
    assertEquals(make_valid_filename("Test File.avi"), "Test File.avi")
    assertEquals(make_valid_filename("Test"), "Test")


def test_dirseperators():
    """Tests make_valid_filename removes directory separators
    """
    assertEquals(make_valid_filename("Test/File.avi"), "Test_File.avi")
    assertEquals(make_valid_filename("Test/File"), "Test_File")


def test_windowsfilenames():
    """Tests make_valid_filename windows_safe flag makes Windows-safe filenames
    """
    assertEquals(make_valid_filename("Test/File.avi", windows_safe = True), "Test_File.avi")
    assertEquals(make_valid_filename("\\/:*?<Evil>|\"", windows_safe = True), "______Evil___")
    assertEquals(make_valid_filename("COM2.txt", windows_safe = True), "_COM2.txt")
    assertEquals(make_valid_filename("COM2", windows_safe = True), "_COM2")


def test_dotfilenames():
    """Tests make_valid_filename on filenames only consisting of .
    """
    assertEquals(make_valid_filename("."), "_.")
    assertEquals(make_valid_filename(".."), "_..")
    assertEquals(make_valid_filename("..."), "_...")
    assertEquals(make_valid_filename(".test.rc"), "_.test.rc")


def test_customblacklist():
    """Test make_valid_filename custom_blacklist feature
    """
    assertEquals(make_valid_filename("Test.avi", custom_blacklist="e"), "T_st.avi")


def test_replacewith():
    """Tests replacing blacklisted character with custom characters
    """
    assertEquals(make_valid_filename("My Test File.avi", custom_blacklist=" ", replace_with="."), "My.Test.File.avi")


def _test_truncation(max_len, windows_safe):
    """Tests truncation works correctly.
    Called with different parameters for both Windows and Darwin/Linux.
    """
    assertEquals(make_valid_filename("a" * 300, windows_safe = windows_safe), "a" * max_len)
    assertEquals(make_valid_filename("a" * 255 + ".avi", windows_safe = windows_safe), "a" * (max_len-4) + ".avi")
    assertEquals(make_valid_filename("a" * 251 + "b" * 10 + ".avi", windows_safe = windows_safe), "a" * (max_len-4) + ".avi")
    assertEquals(make_valid_filename("test." + "a" * 255, windows_safe = windows_safe), "test." + "a" * (max_len-5))


def test_truncation_darwinlinux():
    """Tests make_valid_filename truncates filenames to valid length
    """

    if platform.system() not in ['Darwin', 'Linux']:
        import nose
        raise nose.SkipTest("Test only valid on Darwin and Linux platform")

    _test_truncation(254, windows_safe = False)


def test_truncation_windows():
    """Tests truncate works on Windows (using windows_safe=True)
    """
    _test_truncation(max_len = 254, windows_safe = True)
