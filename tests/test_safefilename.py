#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Test the function to create safe filenames
"""

from tvnamer.utils import makeFilenameSafe

def test_basic():
    """Test makeFilenameSafe does not mess up simple filenames
    """
    assert makeFilenameSafe("test.avi") == "test.avi"
    assert makeFilenameSafe("Test File.avi") == "Test File.avi"
    assert makeFilenameSafe("Test") == "Test"

def test_dirseperators():
    """Tests makeFilenameSafe removes directory separators
    """
    assert makeFilenameSafe("Test/File.avi") == "Test_File.avi"
    assert makeFilenameSafe("Test/File") == "Test_File"

def test_windowsfilenames():
    """Tests makeFilenameSafe windows_safe flag makes Windows-safe filenames 
    """
    assert makeFilenameSafe("Test/File.avi", "Test_File.avi")
    assert makeFilenameSafe(r"\/:*?<Evil File>|\"", "______Evil File__")
    assert makeFilenameSafe("COM.txt", "_COM.txt")
    assert makeFilenameSafe("COM", "_COM")
