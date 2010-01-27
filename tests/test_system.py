#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Tests the current system for things that might cause problems
"""

import os


def test_nosavedconfig():
    """A config at ~/.tvnamer.json could cause problems with some tests
    """
    assert not os.path.isfile(os.path.expanduser("~/.tvnamer.json")), "~/.tvnamer.json exists, which could cause problems with some tests"
