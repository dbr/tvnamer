#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Test tvnamer's filename parser
"""

import os
import sys
from copy import copy
import unittest

sys.path.append(os.path.join(os.path.abspath(sys.path[0]), ".."))
from utils import FileParser

from test_files import files

def check_test(curtest):
    """Runs test case, used by test_generator
    """
    parser = FileParser(curtest['input'])
    theep = parser.parse()
    assert theep.seriesname.lower() == curtest['seriesname'].lower()
    assert theep.seasonnumber == curtest['seasonnumber']
    assert theep.episodenumber == curtest['episodenumber']

def test_generator():
    """Generates test for each test case in test_files.py
    """
    for category, testcases in files.items():
        for testindex, curtest in enumerate(testcases):
            cur_tester = lambda x: check_test(x)
            cur_tester.description = '%s_%d' % (category, testindex)
            yield (cur_tester, curtest)

if __name__ == '__main__':
    import nose
    nose.main()
