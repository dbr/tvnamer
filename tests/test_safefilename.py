#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Test the function to create safe filenames
"""

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
    assertEquals(makeValidFilename("Test/File.avi"), "Test_File.avi")
    assertEquals(makeValidFilename("\\/:*?<Evil File>|\""), "______Evil File__")
    assertEquals(makeValidFilename("COM.txt"), "_COM.txt")
    assertEquals(makeValidFilename("COM"), "_COM")

def test_dotfilenames():
    """Tests makeValidFilename on filenames only consisting of .
    """
    assertEquals(makeValidFilename("."), "_.")
    assertEquals(makeValidFilename(".."), "_..")
    assertEquals(makeValidFilename("..."), "_...")
