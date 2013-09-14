#!/usr/bin/env python

"""Tests the FileParser API
"""

from tvnamer.utils import FileParser
from helpers import assertType, assertEquals


def test_episodeinfo():
    """Parsing a s01e01 episode should return EpisodeInfo class
    """
    p = FileParser("scrubs.s01e01.avi").parse()
    assertEquals(p.eptype, 'default')


def test_datedepisodeinfo():
    """Parsing a 2009.06.05 episode should return DatedEpisodeInfo class
    """
    p = FileParser("scrubs.2009.06.05.avi").parse()
    assertEquals(p.eptype, 'dated')


def test_noseasonepisodeinfo():
    """Parsing a e23 episode should return NoSeasonEpisodeInfo class
    """
    p = FileParser("scrubs - e23.avi").parse()
    assertEquals(p.eptype, 'noseason')


def test_episodeinfo_naming():
    """Parsing a s01e01 episode should return EpisodeInfo class
    """
    p = FileParser("scrubs.s01e01.avi").parse()
    assertEquals(p.eptype, 'default')
    assertEquals(p.generateFilename(), "scrubs - [01x01].avi")


def test_datedepisodeinfo_naming():
    """Parsing a 2009.06.05 episode should return DatedEpisodeInfo class
    """
    p = FileParser("scrubs.2009.06.05.avi").parse()
    assertEquals(p.eptype, 'dated')
    assertEquals(p.generateFilename(), "scrubs - [2009-06-05].avi")


def test_noseasonepisodeinfo_naming():
    """Parsing a e23 episode should return NoSeasonEpisodeInfo class
    """
    p = FileParser("scrubs - e23.avi").parse()
    assertEquals(p.eptype, 'noseason')
    assertEquals(p.generateFilename(), "scrubs - [23].avi")
