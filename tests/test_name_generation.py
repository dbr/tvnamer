#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Test tvnamer's EpisodeInfo file name generation
"""

import os
import sys
import unittest

sys.path.append(os.path.join(os.path.abspath(sys.path[0]), ".."))
from utils import getEpisodeName, EpisodeInfo

from tvdb_api import Tvdb

class test_name_generation(unittest.TestCase):
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
            'Scrubs - [01x02] - My Mentor.avi'
        )

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
            'Scrubs - [01x02] - My Mentor'
        )

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
            'Scrubs - [01x02].avi'
        )

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
            'Scrubs - [01x02]'
        )

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
            'Scrubs - [02] - My Mentor'
        )
