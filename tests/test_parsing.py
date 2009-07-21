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
import unittest

sys.path.append(os.path.join(os.path.abspath(sys.path[0]), ".."))
from utils import FileParser, warn
from tvnamer_exceptions import InvalidFilename

from test_files import files

class test_filenames(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_go(self):
        for category, testcases in files.items():
            for curtest in testcases:
                parser = FileParser(curtest['input'])
                theep = parser.parse()
                self.assertEquals(theep.seasonnumber, curtest['seasonnumber'])
                self.assertEquals(theep.episodenumber, curtest['episodenumber'])

if __name__ == '__main__':
    unittest.main()