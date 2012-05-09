#!/usr/bin/env python

"""Tests the current system for things that might cause problems
"""

import os


def test_nosavedconfig():
    """A config at ~/.tvnamer.json could cause problems with some tests
    """
    assert not os.path.isfile(os.path.expanduser("~/.tvnamer.json")), "~/.tvnamer.json exists, which could cause problems with some tests"
