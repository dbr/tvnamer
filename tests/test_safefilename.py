#!/usr/bin/env python

"""Test the function to create safe filenames
"""

import platform

from helpers import assertEquals

from tvnamer.utils import makeValidFilename


def test_basic():
    """Test makeValidFilename does not mess up simple filenames
    """
    assertEquals(makeValidFilename("test.avi"), "test.avi")
    assertEquals(makeValidFilename("Test File.avi"), "Test File.avi")
    assertEquals(makeValidFilename("Test"), "Test")


def test_dirseperators():
    """Tests makeValidFilename removes directory separators
    """
    assertEquals(makeValidFilename("Test/File.avi"), "Test_File.avi")
    assertEquals(makeValidFilename("Test/File"), "Test_File")


def test_windowsfilenames():
    """Tests makeValidFilename windows_safe flag makes Windows-safe filenames
    """
    assertEquals(makeValidFilename("Test/File.avi", windows_safe = True), "Test_File.avi")
    assertEquals(makeValidFilename("\\/:*?<Evil>|\"", windows_safe = True), "______Evil___")
    assertEquals(makeValidFilename("COM2.txt", windows_safe = True), "_COM2.txt")
    assertEquals(makeValidFilename("COM2", windows_safe = True), "_COM2")


def test_dotfilenames():
    """Tests makeValidFilename on filenames only consisting of .
    """
    assertEquals(makeValidFilename("."), "_.")
    assertEquals(makeValidFilename(".."), "_..")
    assertEquals(makeValidFilename("..."), "_...")
    assertEquals(makeValidFilename(".test.rc"), "_.test.rc")


def test_customblacklist():
    """Test makeValidFilename custom_blacklist feature
    """
    assertEquals(makeValidFilename("Test.avi", custom_blacklist="e"), "T_st.avi")


def test_replacewith():
    """Tests replacing blacklisted character with custom characters
    """
    assertEquals(makeValidFilename("My Test File.avi", custom_blacklist=" ", replace_with="."), "My.Test.File.avi")


def _test_truncation(max_len, windows_safe):
    """Tests truncation works correctly.
    Called with different parameters for both Windows and Darwin/Linux.
    """
    assertEquals(makeValidFilename("a" * 300, windows_safe = windows_safe), "a" * max_len)
    assertEquals(makeValidFilename("a" * 255 + ".avi", windows_safe = windows_safe), "a" * (max_len-4) + ".avi")
    assertEquals(makeValidFilename("a" * 251 + "b" * 10 + ".avi", windows_safe = windows_safe), "a" * (max_len-4) + ".avi")
    assertEquals(makeValidFilename("test." + "a" * 255, windows_safe = windows_safe), "test." + "a" * (max_len-5))


def test_truncation_darwinlinux():
    """Tests makeValidFilename truncates filenames to valid length
    """

    if platform.system() not in ['Darwin', 'Linux']:
        import nose
        raise nose.SkipTest("Test only valid on Darwin and Linux platform")

    _test_truncation(254, windows_safe = False)


def test_truncation_windows():
    """Tests truncate works on Windows (using windows_safe=True)
    """
    _test_truncation(max_len = 254, windows_safe = True)
