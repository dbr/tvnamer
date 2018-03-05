#!/usr/bin/env python

"""Test file names for tvnamer
"""

import datetime


files = {}

files['default_format'] = [
    {'input': 'Scrubs - [04x19] - My Best Laid Plans',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 4, 'episodenumbers': [19],
    'episodenames': ['My Best Laid Plans']},

    {'input': 'Scrubs - [02x11]',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 2, 'episodenumbers': [11],
    'episodenames': ['My Sex Buddy']},

    {'input': 'Scrubs - [04X19] - My Best Laid Plans',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 4, 'episodenumbers': [19],
    'episodenames': ['My Best Laid Plans']},
]

files['s01e01_format'] = [
    {'input': 'scrubs.s01e01',
    'parsedseriesname': 'scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [1],
    'episodenames': ['My First Day']},

    {'input': 'my.name.is.earl.s01e01',
    'parsedseriesname': 'my name is earl',
    'correctedseriesname': 'My Name Is Earl',
    'seasonnumber': 1, 'episodenumbers': [1],
    'episodenames': ['Pilot']},

    {'input': 'scrubs.s01e24.blah.fake',
    'parsedseriesname': 'scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [24],
    'episodenames': ['My Last Day']},

    {'input': 'dexter.s04e05.720p.blah',
    'parsedseriesname': 'dexter',
    'correctedseriesname': 'Dexter',
    'seasonnumber': 4, 'episodenumbers': [5],
    'episodenames': ['Dirty Harry']},

    {'input': 'QI.S04E01.2006-09-29.blah',
    'parsedseriesname': 'QI',
    'correctedseriesname': 'QI',
    'seasonnumber': 4, 'episodenumbers': [1],
    'episodenames': ['Danger']},

    {'input': 'The Wire s05e10 30.mp4',
    'parsedseriesname': 'The Wire',
    'correctedseriesname': 'The Wire',
    'seasonnumber': 5, 'episodenumbers': [10],
    'episodenames': ['-30-']},

    {'input': 'Arrested Development - S2 E 02 - Dummy Ep Name.blah',
    'parsedseriesname': 'Arrested Development',
    'correctedseriesname': 'Arrested Development',
    'seasonnumber': 2, 'episodenumbers': [2],
    'episodenames': ['The One Where They Build a House']},

    {'input': 'Next Stop Discovery - s2001e02 - Arkawa line.avi',
    'parsedseriesname': 'Next Stop Discovery',
    'correctedseriesname': 'Next Stop Discovery',
    'seasonnumber': 2001, 'episodenumbers': [2],
    'episodenames': ['Arakawa line']},

    {'input': 'next.stop.discovery.s2001e02.arkawa.line.avi',
    'parsedseriesname': 'next stop discovery',
    'correctedseriesname': 'Next Stop Discovery',
    'seasonnumber': 2001, 'episodenumbers': [2],
    'episodenames': ['Arakawa line']},

    {'input': 'next stop discovery - [2001x03] - Total Isolation.avi',
    'parsedseriesname': 'next stop discovery',
    'correctedseriesname': 'Next Stop Discovery',
    'seasonnumber': 2001, 'episodenumbers': [3],
    'episodenames': ['Spring winds in the Bay City']},

    {'input': 'Scrubs.0101.avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [1],
    'episodenames': ['My First Day']},

    {'input': 'Scrubs 1x01-720p.avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [1],
    'episodenames': ['My First Day']},

    {'input': 'Scrubs - [s01e01].avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [1],
    'episodenames': ['My First Day']},

    {'input': 'Scrubs - [01.01].avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [1],
    'episodenames': ['My First Day']},

    {'input': '30 Rock [2.10] Episode 210.avi',
    'parsedseriesname': '30 Rock',
    'correctedseriesname': '30 Rock',
    'seasonnumber': 2, 'episodenumbers': [10],
    'episodenames': ['Episode 210']},

    {'input': 'scrubs.s01_e01.avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [1],
    'episodenames': ['My First Day']},

    {'input': 'scrubs - s01 - e02 - something.avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [2],
    'episodenames': ['My Mentor']},
]

files['misc'] = [
    {'input': 'Six.Feet.Under.S0201.test_testing-yay',
    'parsedseriesname': 'Six Feet Under',
    'correctedseriesname': 'Six Feet Under',
    'seasonnumber': 2, 'episodenumbers': [1],
    'episodenames': ['In the Game']},

    {'input': 'Sid.The.Science.Kid.E11.The.Itchy.Tag.WS.ABC.DeF-HIJK',
    'parsedseriesname': 'Sid The Science Kid',
    'correctedseriesname': 'Sid the Science Kid',
    'seasonnumber': None, 'episodenumbers': [11],
    'episodenames': ['The Itchy Tag']},

    {'input': 'Total Access - [01x01]',
    'parsedseriesname': 'total access',
    'correctedseriesname': 'Total Access 24/7',
    'seasonnumber': 1, 'episodenumbers': [1],
    'episodenames': ['Episode #1']},

    {'input': 'Scrubs - Episode 2 [S 1 - Ep 002] - Fri 24 Jan 2001 [KCRT].avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [2],
    'episodenames': ['My Mentor']},

    {'input': 'Scrubs Season 01 Episode 01 - The Series Title.avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [1],
    'episodenames': ['My First Day']},
]

files['multiple_episodes'] = [
    {'input': 'Scrubs - [01x01-02-03]',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [1, 2, 3],
    'episodenames': ['My First Day', 'My Mentor', 'My Best Friend\'s Mistake']},

    {'input': 'scrubs.s01e23e24',
    'parsedseriesname': 'scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [23, 24],
    'episodenames': ['My Hero', 'My Last Day']},

    {'input': 'scrubs.01x23x24',
    'parsedseriesname': 'scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [23, 24],
    'episodenames': ['My Hero', 'My Last Day']},

    {'input': 'scrubs.01x23-24',
    'parsedseriesname': 'scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [23, 24],
    'episodenames': ['My Hero', 'My Last Day']},

    {'input': 'Stargate SG-1 - [01x01-02]',
    'parsedseriesname': 'Stargate SG-1',
    'correctedseriesname': 'Stargate SG-1',
    'seasonnumber': 1, 'episodenumbers': [1, 2],
    'episodenames': ['Children of the Gods (1)', 'Children of the Gods (2)']},

    {'input': '[Lunar] Bleach - 11-12 [B937F496]',
    'parsedseriesname': 'Bleach',
    'correctedseriesname': 'Bleach',
    'seasonnumber': None, 'episodenumbers': [11, 12],
    'episodenames': ['The Legendary Quincy', 'A Gentle Right Arm']},

    {'input': 'scrubs.s01e01e02e03',
    'parsedseriesname': 'scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [1, 2, 3],
    'episodenames': ['My First Day', 'My Mentor', 'My Best Friend\'s Mistake']},

    {'input': 'Scrubs - [02x01-03]',
    'parsedseriesname': 'scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 2, 'episodenumbers': [1, 2, 3],
    'episodenames': ['My Overkill', 'My Nightingale', 'My Case Study']},

    {'input': 'Scrubs - [02x01+02]',
    'parsedseriesname': 'scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 2, 'episodenumbers': [1, 2],
    'episodenames': ['My Overkill', 'My Nightingale']},

    {'input': 'Scrubs 2x01+02',
    'parsedseriesname': 'scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 2, 'episodenumbers': [1, 2],
    'episodenames': ['My Overkill', 'My Nightingale']},

    {'input': 'Flight.of.the.Conchords.S01E01-02.An.Ep.name.avi',
    'parsedseriesname': 'Flight of the Conchords',
    'correctedseriesname': 'Flight of the Conchords',
    'seasonnumber': 1, 'episodenumbers': [1, 2],
    'episodenames': ['Sally', 'Bret Gives Up the Dream']},

    {'input': 'Flight.of.the.Conchords.S01E02e01.An.Ep.name.avi',
    'parsedseriesname': 'Flight of the Conchords',
    'correctedseriesname': 'Flight of the Conchords',
    'seasonnumber': 1, 'episodenumbers': [1, 2],
    'episodenames': ['Sally', 'Bret Gives Up the Dream']},

    {'input': 'Scrubs s01e22 s01e23 s01e24.avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [22, 23, 24],
    'episodenames': ['My Occurrence', 'My Hero', 'My Last Day']},

    {'input': 'Scrubs s01e22 s01e23.avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [22, 23],
    'episodenames': ['My Occurrence', 'My Hero']},

    {'input': 'Scrubs - 01x22 01x23.avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [22, 23],
    'episodenames': ['My Occurrence', 'My Hero']},

    {'input': 'Scrubs.01x22.01x23.avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [22, 23],
    'episodenames': ['My Occurrence', 'My Hero']},

    {'input': 'Scrubs 1x22 1x23.avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [22, 23],
    'episodenames': ['My Occurrence', 'My Hero']},

    {'input': 'Scrubs.S01E01-E04.avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [1, 2, 3, 4],
    'episodenames': ['My First Day', 'My Mentor', 'My Best Friend\'s Mistake', 'My Old Lady']},

]

files['unicode'] = [
    {'input': u'Carniv\xe0le 1x11 - The Day of the Dead',
    'parsedseriesname': u'Carniv\xe0le',
    'correctedseriesname': u'Carniv\xe0le',
    'seasonnumber': 1, 'episodenumbers': [11],
    'episodenames': ['The Day of the Dead']},

    {'input': u'The Big Bang Theory - S02E07 - The Panty Pi\xf1ata Polarization.avi',
    'parsedseriesname': u'The Big Bang Theory',
    'correctedseriesname': u'The Big Bang Theory',
    'seasonnumber': 2, 'episodenumbers': [7],
    'episodenames': [u'The Panty Pi\xf1ata Polarization']},

    {'input': u'NCIS - 1x16.avi',
    'parsedseriesname': u'NCIS',
    'correctedseriesname': u'NCIS',
    'seasonnumber': 1, 'episodenumbers': [16],
    'episodenames': [u'B\xeate Noire']},
]

files['anime'] = [
    {'input': '[Eclipse] Fullmetal Alchemist Brotherhood - 02 (1280x720 h264) [8452C4BF].mkv',
    'parsedseriesname': 'Fullmetal Alchemist Brotherhood',
    'correctedseriesname': 'Fullmetal Alchemist: Brotherhood',
    'seasonnumber': None, 'episodenumbers': [2],
    'episodenames': ['The First Day']},

    {'input': '[Shinsen-Subs] Armored Trooper Votoms - 01 [9E3F1D1C].mkv',
    'parsedseriesname': 'armored trooper votoms',
    'correctedseriesname': 'Armored Trooper VOTOMS',
    'seasonnumber': None, 'episodenumbers': [1],
    'episodenames': ['War\'s End']},

    {'input': '[Shinsen-Subs] Beet - 19 [24DAB497].mkv',
    'parsedseriesname': 'beet',
    'correctedseriesname': 'Beet the Vandel Buster',
    'seasonnumber': None, 'episodenumbers': [19],
    'episodenames': ['Threat of the Planet Earth']},

    {'input': '[AG-SHS]Victory_Gundam-03_DVD[FC6E3A6F].mkv',
    'parsedseriesname': 'victory gundam',
    'correctedseriesname': 'Mobile Suit Victory Gundam',
    'seasonnumber': None, 'episodenumbers': [3],
    'episodenames': ['Uso\'s Fight']},

    {'input': '[YuS-SHS]Gintama-24(H264)_[52CA4F8B].mkv',
    'parsedseriesname': 'gintama',
    'correctedseriesname': 'Gintama',
    'seasonnumber': None, 'episodenumbers': [24],
    'episodenames': ['Cute Faces Are Always Hiding Something']},

    {'input': '[Shinsen-Subs] True Mazinger - 07 [848x480 H.264 Vorbis][787D0074].mkv',
    'parsedseriesname': 'True Mazinger',
    'correctedseriesname': 'Mazinger Edition Z: The Impact!',
    'seasonnumber': None, 'episodenumbers': [7],
    'episodenames': ['Legend! The Mechanical Beasts of Bardos!']},

    {'input': '[BSS]_Tokyo_Magnitude_8.0_-_02_[0E5C4A40].mkv',
    'parsedseriesname': 'tokyo magnitude 8.0',
    'correctedseriesname': 'Tokyo Magnitude 8.0',
    'seasonnumber': None, 'episodenumbers': [2],
    'episodenames': ['Broken World']},

    {'input': 'Bleach - [310] - Ichigo\'s Resolution.avi',
    'parsedseriesname': 'Bleach',
    'correctedseriesname': 'Bleach',
    'seasonnumber': None, 'episodenumbers': [310],
    'episodenames': ['Ichigo\'s Resolution']},
]

files['date_based'] = [
    {'input': 'Scrubs.2001-10-02.avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'episodenumbers': [datetime.date(2001, 10, 2)],
    'episodenames': ['My First Day']},

    {'input': 'Scrubs - 2001-10-02 - Old Episode Title.avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'episodenumbers': [datetime.date(2001, 10, 2)],
    'episodenames': ['My First Day']},

    {'input': 'Scrubs - 2001.10.02 - Old Episode Title.avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'episodenumbers': [datetime.date(2001, 10, 2)],
    'episodenames': ['My First Day']},

    {'input': 'yes.we.canberra.2010.08.18.pdtv.xvid',
    'parsedseriesname': 'yes we canberra',
    'correctedseriesname': 'Yes We Canberra',
    'episodenumbers': [datetime.date(2010, 8, 18)],
    'episodenames': ['Episode 4']},
]

files['x_of_x'] = [
    {'input': 'Scrubs.1of5.avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': None, 'episodenumbers': [1],
    'episodenames': ['My First Day']},

    {'input': 'Scrubs part 1.avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': None, 'episodenumbers': [1],
    'episodenames': ['My First Day']},

    {'input': 'Scrubs part 1 of 10.avi', # only one episode, as it's not "1 to 10"
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': None, 'episodenumbers': [1],
    'episodenames': ['My First Day']},

    {'input': 'Scrubs part 1 and part 2.avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': None, 'episodenumbers': [1, 2],
    'episodenames': ['My First Day', 'My Mentor']},

    {'input': 'Scrubs part 1 to part 3.avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': None, 'episodenumbers': [1, 2, 3],
    'episodenames': ['My First Day', 'My Mentor', 'My Best Friend\'s Mistake']},

    {'input': 'Scrubs part 1 to 4.avi',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': None, 'episodenumbers': [1, 2, 3, 4],
    'episodenames': ['My First Day', 'My Mentor', 'My Best Friend\'s Mistake', 'My Old Lady']},

]


files['no_series_name'] = [
    {'input': 's01e01.avi',
    'force_name': 'Scrubs',
    'parsedseriesname': None,
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [1],
    'episodenames': ['My First Day']},

    {'input': '[01x01].avi',
    'force_name': 'Scrubs',
    'parsedseriesname': None,
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumbers': [1],
    'episodenames': ['My First Day']},
]


def test_verify_test_data_sanity():
    """Checks all test data is consistent.

    Keys within each test category must be consistent, but keys can vary
    category to category. E.g date-based episodes do not have a season number
    """
    from helpers import assertEquals

    for test_category, testcases in files.items():
        keys = [ctest.keys() for ctest in testcases]
        for k1 in keys:
            for k2 in keys:
                assertEquals(sorted(k1), sorted(k2))
