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
from utils import FileParser

from test_files import files


class test_name_parser(unittest.TestCase):

    def setUp(self):
        """Define name formats to test.
        %(seriesname)s becomes the seriesname,
        %(seasno)s becomes the season number,
        %(epno)s becomes the episode number.
        """

        #scene naming standards: http://tvunderground.org.ru/forum/index.php?showtopic=8488
        self.name_formats = [
            '%(seriesname)s.s%(seasno)de%(epno)d.dsr.nf.avi',                 #seriesname.s01e02.dsr.nf.avi
            '%(seriesname)s.S%(seasno)dE%(epno)d.PROPER.dsr.nf.avi',          #seriesname.S01E02.PROPER.dsr.nf.avi
            '%(seriesname)s.s%(seasno)d.e%(epno)d.avi',                       #seriesname.s01.e02.avi
            '%(seriesname)s-s%(seasno)de%(epno)d.avi',                        #seriesname-s01e02.avi
            '%(seriesname)s-s%(seasno)de%(epno)d.the.wrong.ep.name.avi',      #seriesname-s01e02.the.wrong.ep.name.avi
            '%(seriesname)s - [%(seasno)dx%(epno)d].avi',                     #seriesname - [01x02].avi
            '%(seriesname)s - [%(seasno)dx0%(epno)d].avi',                    #seriesname - [01x002].avi
            '%(seriesname)s-[%(seasno)dx%(epno)d].avi',                       #seriesname-[01x02].avi
            '%(seriesname)s [%(seasno)dx%(epno)d].avi',                       #seriesname [01x02].avi
            '%(seriesname)s [%(seasno)dx%(epno)d] the wrong ep name.avi',     #seriesname [01x02] epname.avi
            '%(seriesname)s [%(seasno)dx%(epno)d] - the wrong ep name.avi',   #seriesname [01x02] - the wrong ep name.avi
            '%(seriesname)s - [%(seasno)dx%(epno)d] - the wrong ep name.avi', #seriesname - [01x02] - the wrong ep name.avi
            '%(seriesname)s.%(seasno)dx%(epno)d.The_Wrong_ep_name.avi',       #seriesname.01x02.epname.avi
            '%(seriesname)s.%(seasno)d%(epno)02d.The Wrong_ep.names.avi',     #seriesname.102.epname.avi
            '%(seriesname)s_s%(seasno)de%(epno)d_The_Wrong_ep_na-me.avi',     #seriesname_s1e02_epname.avi
            '%(seriesname)s - s%(seasno)de%(epno)d - dsr.nf.avi',             #seriesname - s01e02 - dsr.nf.avi
            '%(seriesname)s - s%(seasno)de%(epno)d - the wrong ep name.avi',  #seriesname - s01e02 - the wrong ep name.avi
            '%(seriesname)s - s%(seasno)de%(epno)d - the wrong ep name.avi',  #seriesname - s01e02 - the_wrong_ep_name!.avi
        ]

    def test_name_parser_basic(self):
        """Tests most basic filename (simple seriesname)
        """
        name_data = {'seriesname': 'series name'}
        self._run_test(name_data)

    def test_name_parser_showdashname(self):
        """Tests with dash in seriesname
        """
        name_data = {'seriesname': 'S-how name'}
        self._run_test(name_data)

    def test_name_parser_shownumeric(self):
        """Tests with numeric show name
        """
        name_data = {'seriesname': '123'}
        self._run_test(name_data)

    def test_name_parser_shownumericspaces(self):
        """Tests with numeric show name, with spaces
        """
        name_data = {'seriesname': '123 2008'}
        self._run_test(name_data)

    def test_name_parser_exclaim(self):
        """Tests parsing show with explaimation mark
        """
        name_data = {'seriesname': 'Show name!'}
        self._run_test(name_data)

    def test_name_parser_unicode(self):
        """Tests parsing show containing unicode characters"""
        name_data = {'seriesname': u'T\xecnh Ng\u01b0\u1eddi Hi\u1ec7n \u0110\u1ea1i'.encode('utf-8')}
        self._run_test(name_data)

    def _run_test(self, name_data):
        """Runs the tests and checks if the parsed values have
        the correct seriesname/season number/episode number.
        Runs from season 0 ep 0 to season 10, ep 10.
        """
        for seas in xrange(1, 11):
            for ep in xrange(1, 11):
                name_data['seasno'] = seas
                name_data['epno'] = ep

                names = [x % name_data for x in self.name_formats]

                for cur in names:
                    p = FileParser(cur).parse()

                    self.assertEquals(p.episodenumber, name_data['epno'])
                    self.assertEquals(p.seasonnumber, name_data['seasno'])
                    self.assertEquals(p.seriesname, name_data['seriesname'])


def check_case(curtest):
    """Runs test case, used by test_generator
    """
    parser = FileParser(curtest['input'])
    theep = parser.parse()
    assert theep.seriesname.lower() == curtest['parsedseriesname'].lower(), "%s == %s" % (
        theep.seriesname.lower(),
        curtest['parsedseriesname'].lower())

    assert theep.seasonnumber == curtest['seasonnumber'], "%s == %s" % (theep.seasonnumber, curtest['seasonnumber'])

    assert theep.episodenumber == curtest['episodenumber'], "%s == %s" % (theep.episodenumber, curtest['episodenumber'])


def test_generator():
    """Generates test for each test case in test_files.py
    """
    for category, testcases in files.items():
        for testindex, curtest in enumerate(testcases):
            cur_tester = lambda x: check_case(x)
            cur_tester.description = '%s_%d: %s' % (
                category, testindex, curtest['input'])
            yield (cur_tester, curtest)


if __name__ == '__main__':
    import nose
    nose.main()
