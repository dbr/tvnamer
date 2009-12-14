#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Test the function to create safe filenames
"""

from tvnamer.utils import makeValidFilename

def test_basic():
    """Test makeValidFilename does not mess up simple filenames
    """
    assert makeValidFilename("test.avi") == "test.avi"
    assert makeValidFilename("Test File.avi") == "Test File.avi"
    assert makeValidFilename("Test") == "Test"

def test_dirseperators():
    """Tests makeValidFilename removes directory separators
    """
    assert makeValidFilename("Test/File.avi") == "Test_File.avi"
    assert makeValidFilename("Test/File") == "Test_File"

def test_windowsfilenames():
    """Tests makeValidFilename windows_safe flag makes Windows-safe filenames 
    """
    assert makeValidFilename("Test/File.avi", "Test_File.avi")
    assert makeValidFilename(r"\/:*?<Evil File>|\"", "______Evil File__")
    assert makeValidFilename("COM.txt", "_COM.txt")
    assert makeValidFilename("COM", "_COM")
