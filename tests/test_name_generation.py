#!/usr/bin/env python

"""Test tvnamer's EpisodeInfo file name generation
"""

import os
import datetime

from helpers import assertEquals

from tvnamer.main import TVNAMER_API_KEY
from tvnamer.data import (EpisodeInfo, DatedEpisodeInfo, NoSeasonEpisodeInfo)
from test_files import files

from tvdb_api import Tvdb


def verify_name_gen(curtest, tvdb_instance):
    if "seasonnumber" in curtest:
        ep = EpisodeInfo(
            seriesname = curtest['parsedseriesname'],
            seasonnumber = curtest['seasonnumber'],
            episodenumbers = curtest['episodenumbers'])
    elif any([isinstance(x, datetime.date) for x in curtest['episodenumbers']]):
        ep = DatedEpisodeInfo(
            seriesname = curtest['parsedseriesname'],
            episodenumbers = curtest['episodenumbers'])
    else:
        ep = NoSeasonEpisodeInfo(
            seriesname = curtest['parsedseriesname'],
            episodenumbers = curtest['episodenumbers'])

    ep.populate_from_tvdb(tvdb_instance, force_name = curtest.get("force_name"))

    assert ep.seriesname is not None, "Corrected series name was none"
    assert ep.episodename is not None, "Episode name was None"

    assertEquals(ep.seriesname, curtest['correctedseriesname'])
    assertEquals(ep.episodename, curtest['episodenames'])


def test_name_generation_on_testfiles():
    # Test data stores episode names in English, language= is normally set
    # via the configuration, same with search_all_languages.

    tvdb_instance = Tvdb(search_all_languages=True, cache=True, language='en', apikey=TVNAMER_API_KEY)
    for category, testcases in files.items():
        for curtest in testcases:
            verify_name_gen(curtest, tvdb_instance)

def test_single_episode():
    """Simple episode name, with show/season/episode/name/filename
    """

    ep = EpisodeInfo(
        seriesname = 'Scrubs',
        seasonnumber = 1,
        episodenumbers = [2],
        episodename = 'My Mentor',
        filename = 'scrubs.example.file.avi')

    assertEquals(
        ep.generate_filename(),
        'Scrubs - [01x02] - My Mentor.avi')


def test_multi_episodes_continuous():
    """A two-part episode should not have the episode name repeated
    """
    ep = EpisodeInfo(
        seriesname = 'Stargate SG-1',
        seasonnumber = 1,
        episodenumbers = [1, 2],
        episodename = [
            'Children of the Gods (1)',
            'Children of the Gods (2)'],
        filename = 'stargate.example.file.avi')

    assertEquals(
        ep.generate_filename(),
        'Stargate SG-1 - [01x01-02] - Children of the Gods (1-2).avi')


def test_episode_numeric_title():
    """An episode with a name starting with a number should not be
    detected as a range
    """

    ep = EpisodeInfo(
        seriesname = 'Star Trek TNG',
        seasonnumber = 1,
        episodenumbers = [15],
        episodename = [
            '11001001'
        ],
        filename = 'STTNG-S01E15-11001001.avi')

    assertEquals(
        ep.generate_filename(),
        'Star Trek TNG - [01x15] - 11001001.avi')


def test_multi_episodes_seperate():
    """File with two episodes, but with different names
    """
    ep = EpisodeInfo(
        seriesname = 'Stargate SG-1',
        seasonnumber = 1,
        episodenumbers = [2, 3],
        episodename = [
            'Children of the Gods (2)',
            'The Enemy Within'],
        filename = 'stargate.example.file.avi')

    assertEquals(
        ep.generate_filename(),
        'Stargate SG-1 - [01x02-03] - Children of the Gods (2), The Enemy Within.avi')


def test_simple_no_ext():
    """Simple episode with out extension
    """
    ep = EpisodeInfo(
        seriesname = 'Scrubs',
        seasonnumber = 1,
        episodenumbers = [2],
        episodename = ['My Mentor'],
        filename = None)

    assertEquals(
        ep.generate_filename(),
        'Scrubs - [01x02] - My Mentor')


def test_no_name():
    """Episode without a name
    """
    ep = EpisodeInfo(
        seriesname = 'Scrubs',
        seasonnumber = 1,
        episodenumbers = [2],
        episodename = None,
        filename = 'scrubs.example.file.avi')

    assertEquals(
        ep.generate_filename(),
        'Scrubs - [01x02].avi')


def test_episode_no_name_no_ext():
    """EpisodeInfo with no name or extension
    """
    ep = EpisodeInfo(
        seriesname = 'Scrubs',
        seasonnumber = 1,
        episodenumbers = [2],
        episodename = None,
        filename = None)

    assertEquals(
        ep.generate_filename(),
        'Scrubs - [01x02]')


def test_noseason_no_name_no_ext():
    """NoSeasonEpisodeInfo with no name or extension
    """
    ep = NoSeasonEpisodeInfo(
        seriesname = 'Scrubs',
        episodenumbers = [2],
        episodename = None,
        filename = None)

    assertEquals(
        ep.generate_filename(),
        'Scrubs - [02]')


def test_datedepisode_no_name_no_ext():
    """DatedEpisodeInfo with no name or extension
    """
    ep = DatedEpisodeInfo(
        seriesname = 'Scrubs',
        episodenumbers = [datetime.date(2010, 11, 23)],
        episodename = None,
        filename = None)

    assertEquals(
        ep.generate_filename(),
        'Scrubs - [2010-11-23]')


def test_no_series_number():
    """Episode without season number
    """
    ep = NoSeasonEpisodeInfo(
        seriesname = 'Scrubs',
        episodenumbers = [2],
        episodename = 'My Mentor',
        filename = None)

    assertEquals(
        ep.generate_filename(),
        'Scrubs - [02] - My Mentor')


def test_downcase():
    """Simple episode name, converted to lowercase
    """

    ep = EpisodeInfo(
        seriesname = 'Scrubs',
        seasonnumber = 1,
        episodenumbers = [2],
        episodename = 'My Mentor',
        filename = 'scrubs.example.file.avi')

    assertEquals(
        ep.generate_filename(lowercase = True),
        'scrubs - [01x02] - my mentor.avi')


def test_episode_number_formatting():
    from tvnamer.utils import format_episode_name
    fmt = "%(epname)s (%(episodemin)s-%(episodemax)s)"
    joiner = ", "

    # Simple cases
    assert format_episode_name(['A test'], joiner, fmt) == 'A test'
    assert format_episode_name(['A test (1)'], joiner, fmt) == 'A test (1)'
    assert format_episode_name(['A test (1)', 'A test (2)'], joiner, fmt) == 'A test (1-2)'
    assert format_episode_name(['A test (1)', 'A test (2)', 'A test (3)'], joiner, fmt) == 'A test (1-3)'

    # Inconsistent episode names
    assert format_episode_name(['A test (1)', "Weirdness (2)"], joiner, fmt) == 'A test (1), Weirdness (2)'

    # Skip incomplete sequences
    assert format_episode_name(['A test (1)', 'A test (8)'], joiner, fmt) == 'A test (1), A test (8)'

    # Skip if numbers are duplicated
    assert format_episode_name(['A test (1)', 'A test (1)'], joiner, fmt) == 'A test (1), A test (1)'

    # First episode can miss name
    assert format_episode_name(['A test', 'A test (2)', 'A test (3)'], joiner, fmt) == 'A test (1-3)'

    # Different format options
    assert format_episode_name(['Yep', 'Thing'], "!", fmt) == 'Yep!Thing'
    assert format_episode_name(['A test (1)', 'A test (2)', 'A test (3)'], ",", "%(epname)s (%(episodemin)s to %(episodemax)s)") == 'A test (1 to 3)'
