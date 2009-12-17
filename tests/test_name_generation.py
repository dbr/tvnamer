#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Test tvnamer's EpisodeInfo file name generation
"""

import unittest
from helpers import assertEquals

from tvnamer.utils import getEpisodeName, EpisodeInfo
from test_files import files

from tvdb_api import Tvdb


def verify_name_gen(curtest, tvdb_instance):
    ep = EpisodeInfo(
        seriesname = curtest['parsedseriesname'],
        seasonnumber = curtest['seasonnumber'],
        episodenumber = curtest['episodenumber'])
    correctedSeriesName, epName = getEpisodeName(tvdb_instance, ep)

    assert correctedSeriesName is not None, "Corrected series name was none"
    assert epName is not None, "Episode name was None"

    assertEquals(epName, curtest['episodenames'])
    assertEquals(correctedSeriesName, curtest['correctedseriesname'])


def test_name_generation_on_testfiles():
    # Test data stores episode names in English, language= is normally set
    # via the configuration, same with search_all_languages.
    tvdb_instance = Tvdb(search_all_languages=True, language='en')
    for category, testcases in files.items():
        for testindex, curtest in enumerate(testcases):
            cur_tester = lambda x: verify_name_gen(x, tvdb_instance)
            cur_tester.description = 'test_name_generation_%s_%d: %r' % (
                category, testindex, curtest['input'])
            yield (cur_tester, curtest)


class test_name_generation_output_formats(unittest.TestCase):
    """Tests a few different output formats, such as with/without episode
    names, with/without season numbers and so on.
    """

    def test_single_episode(self):
        """Simple episode name, with show/season/episode/name/filename
        """

        ep = EpisodeInfo(
            seriesname = 'Scrubs',
            seasonnumber = 1,
            episodenumber = 2,
            episodename = 'My Mentor',
            filename = 'scrubs.example.file.avi')

        self.assertEquals(
            ep.generateFilename(),
            'Scrubs - [01x02] - My Mentor.avi')

    def test_simple_no_ext(self):
        """Simple episode with out extension
        """
        ep = EpisodeInfo(
            seriesname = 'Scrubs',
            seasonnumber = 1,
            episodenumber = 2,
            episodename = 'My Mentor',
            filename = None)

        self.assertEquals(
            ep.generateFilename(),
            'Scrubs - [01x02] - My Mentor')

    def test_no_name(self):
        """Episode without a name
        """
        ep = EpisodeInfo(
            seriesname = 'Scrubs',
            seasonnumber = 1,
            episodenumber = 2,
            episodename = None,
            filename = 'scrubs.example.file.avi')

        self.assertEquals(
            ep.generateFilename(),
            'Scrubs - [01x02].avi')

    def test_no_name_no_ext(self):
        """Episode with no name or extension
        """
        ep = EpisodeInfo(
            seriesname = 'Scrubs',
            seasonnumber = 1,
            episodenumber = 2,
            episodename = None,
            filename = None)

        self.assertEquals(
            ep.generateFilename(),
            'Scrubs - [01x02]')

    def test_no_series_number(self):
        """Episode without series number
        """
        ep = EpisodeInfo(
            seriesname = 'Scrubs',
            seasonnumber = None,
            episodenumber = 2,
            episodename = 'My Mentor',
            filename = None)

        self.assertEquals(
            ep.generateFilename(),
            'Scrubs - [02] - My Mentor')
