#!/usr/bin/env python

"""Test tvnamer's filename parser
"""

from helpers import assertEquals

from tvnamer.utils import (FileParser, DatedEpisodeInfo, NoSeasonEpisodeInfo)

from test_files import files


def test_autogen_names():
    """Tests set of standard filename formats with various data
    """

    """Mostly based on scene naming standards:
    http://tvunderground.org.ru/forum/index.php?showtopic=8488

    %(seriesname)s becomes the seriesname,
    %(seasno)s becomes the season number,
    %(epno)s becomes the episode number.

    Each is string-formatted with seasons from 0 to 10, and ep 0 to 10
    """

    name_formats = [
        '%(seriesname)s.s%(seasno)de%(epno)d.dsr.nf.avi',                 # seriesname.s01e02.dsr.nf.avi
        '%(seriesname)s.S%(seasno)dE%(epno)d.PROPER.dsr.nf.avi',          # seriesname.S01E02.PROPER.dsr.nf.avi
        '%(seriesname)s.s%(seasno)d.e%(epno)d.avi',                       # seriesname.s01.e02.avi
        '%(seriesname)s-s%(seasno)de%(epno)d.avi',                        # seriesname-s01e02.avi
        '%(seriesname)s-s%(seasno)de%(epno)d.the.wrong.ep.name.avi',      # seriesname-s01e02.the.wrong.ep.name.avi
        '%(seriesname)s - [%(seasno)dx%(epno)d].avi',                     # seriesname - [01x02].avi
        '%(seriesname)s - [%(seasno)dx0%(epno)d].avi',                    # seriesname - [01x002].avi
        '%(seriesname)s-[%(seasno)dx%(epno)d].avi',                       # seriesname-[01x02].avi
        '%(seriesname)s [%(seasno)dx%(epno)d].avi',                       # seriesname [01x02].avi
        '%(seriesname)s [%(seasno)dx%(epno)d] the wrong ep name.avi',     # seriesname [01x02] epname.avi
        '%(seriesname)s [%(seasno)dx%(epno)d] - the wrong ep name.avi',   # seriesname [01x02] - the wrong ep name.avi
        '%(seriesname)s - [%(seasno)dx%(epno)d] - the wrong ep name.avi', # seriesname - [01x02] - the wrong ep name.avi
        '%(seriesname)s.%(seasno)dx%(epno)d.The_Wrong_ep_name.avi',       # seriesname.01x02.epname.avi
        '%(seriesname)s.%(seasno)d%(epno)02d.The Wrong_ep.names.avi',     # seriesname.102.epname.avi
        '%(seriesname)s_s%(seasno)de%(epno)d_The_Wrong_ep_na-me.avi',     # seriesname_s1e02_epname.avi
        '%(seriesname)s - s%(seasno)de%(epno)d - dsr.nf.avi',             # seriesname - s01e02 - dsr.nf.avi
        '%(seriesname)s - s%(seasno)de%(epno)d - the wrong ep name.avi',  # seriesname - s01e02 - the wrong ep name.avi
        '%(seriesname)s - s%(seasno)de%(epno)d - the wrong ep name.avi',  # seriesname - s01e02 - the_wrong_ep_name!.avi
    ]

    test_data = [
    {'name': 'test_name_parser_unicode',
    'description': 'Tests parsing show containing unicode characters',
    'name_data': {'seriesname': 'T\xc3\xacnh Ng\xc6\xb0\xe1\xbb\x9di Hi\xe1\xbb\x87n \xc4\x90\xe1\xba\xa1i'}},

    {'name': 'test_name_parser_basic',
    'description': 'Tests most basic filename (simple seriesname)',
    'name_data': {'seriesname': 'series name'}},

    {'name': 'test_name_parser_showdashname',
    'description': 'Tests with dash in seriesname',
    'name_data': {'seriesname': 'S-how name'}},

    {'name': 'test_name_parser_exclaim',
    'description': 'Tests parsing show with exclamation mark',
    'name_data': {'seriesname': 'Show name!'}},

    {'name': 'test_name_parser_shownumeric',
    'description': 'Tests with numeric show name',
    'name_data': {'seriesname': '123'}},

    {'name': 'test_name_parser_shownumericspaces',
    'description': 'Tests with numeric show name, with spaces',
    'name_data': {'seriesname': '123 2008'}},
    ]

    for cdata in test_data:
        # Make new wrapped function
        def cur_test():
            for seas in range(1, 11):
                for ep in range(1, 11):

                    name_data = cdata['name_data']

                    name_data['seasno'] = seas
                    name_data['epno'] = ep

                    names = [x % name_data for x in name_formats]

                    for cur in names:
                        p = FileParser(cur).parse()

                        assertEquals(p.episodenumbers, [name_data['epno']])
                        assertEquals(p.seriesname, name_data['seriesname'])
                        # Only EpisodeInfo has seasonnumber
                        if not isinstance(p, (DatedEpisodeInfo, NoSeasonEpisodeInfo)):
                            assertEquals(p.seasonnumber, name_data['seasno'])
        #end cur_test

        print("Testing: %s" % cdata['description'])
        cur_test()


def check_case(curtest):
    """Runs test case, used by test_parsing_generator
    """
    parser = FileParser(curtest['input'])
    theep = parser.parse()

    if theep.seriesname is None and curtest['parsedseriesname'] is None:
        pass # allow for None seriesname
    else:
        assert theep.seriesname.lower() == curtest['parsedseriesname'].lower(), "%s == %s" % (
            theep.seriesname.lower(),
            curtest['parsedseriesname'].lower())

    assertEquals(theep.episodenumbers, curtest['episodenumbers'])
    if not isinstance(theep, (DatedEpisodeInfo, NoSeasonEpisodeInfo)):
        assertEquals(theep.seasonnumber, curtest['seasonnumber'])


def test_parsing_generator():
    """Generates test for each test case in test_files.py
    """
    for category, testcases in files.items():
        for curtest in testcases:
            check_case(curtest)


if __name__ == '__main__':
    import nose
    nose.main()
