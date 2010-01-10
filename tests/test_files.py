#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Test file names for tvnamer
"""

files = {}

files['default_format'] = [
    {'input': 'Scrubs - [04x19] - My Best Laid Plans',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 4, 'episodenumber': 19,
    'episodenames': ['My Best Laid Plans']},

    {'input': 'Scrubs - [02x11]',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 2, 'episodenumber': 11,
    'episodenames': ['My Sex Buddy']},
]

files['s01e01_format'] = [
    {'input': 'scrubs.s01e01',
    'parsedseriesname': 'scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumber': 1,
    'episodenames': ['My First Day']},

    {'input': 'my.name.is.earl.s01e01',
    'parsedseriesname': 'my name is earl',
    'correctedseriesname': 'My Name Is Earl',
    'seasonnumber': 1, 'episodenumber': 1,
    'episodenames': ['Pilot']},

    {'input': 'scrubs.s01e24.blah.fake',
    'parsedseriesname': 'scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumber': 24,
    'episodenames': ['My Last Day']},

    {'input': 'dexter.s04e05.720p.blah',
    'parsedseriesname': 'dexter',
    'correctedseriesname': 'Dexter',
    'seasonnumber': 4, 'episodenumber': 5,
    'episodenames': ['Dirty Harry']},

    {'input': 'QI.S04E01.2006-09-29.blah',
    'parsedseriesname': 'QI',
    'correctedseriesname': 'QI',
    'seasonnumber': 4, 'episodenumber': 1,
    'episodenames': ['Danger']},

    {'input': 'The Wire s05e10 30.mp4',
    'parsedseriesname': 'The Wire',
    'correctedseriesname': 'The WIre',
    'seasonnumber': 5, 'episodenumber': 10,
    'episodenames': ['-30-']},
]

files['misc'] = [
    {'input': 'Six.Feet.Under.S0201.test_testing-yay',
    'parsedseriesname': 'Six Feet Under',
    'correctedseriesname': 'Six Feet Under',
    'seasonnumber': 2, 'episodenumber': 1,
    'episodenames': ['In The Game']},

    {'input': 'Sid.The.Science.Kid.E11.The.Itchy.Tag.WS.ABC.DeF-HIJK',
    'parsedseriesname': 'Sid The Science Kid',
    'correctedseriesname': 'Sid the Science Kid',
    'seasonnumber': None, 'episodenumber': 11,
    'episodenames': ['The Itchy Tag']},

    {'input': 'Total Access - [01x01]',
    'parsedseriesname': 'total access',
    'correctedseriesname': 'Total Access 24/7',
    'seasonnumber': 1, 'episodenumber': 1,
    'episodenames': ['Episode #1']},
]

files['multiple_episodes'] = [
    {'input': 'Scrubs - [01x01-02-03]',
    'parsedseriesname': 'Scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumber': [1, 2, 3],
    'episodenames': ['My First Day', 'My Mentor', 'My Best Friend\'s Mistake']},

    {'input': 'scrubs.s01e23e24',
    'parsedseriesname': 'scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumber': [23, 24],
    'episodenames': ['My Hero', 'My Last Day']},

    {'input': 'Stargate SG-1 - [01x01-02]',
    'parsedseriesname': 'Stargate SG-1',
    'correctedseriesname': 'Stargate SG-1',
    'seasonnumber': 1, 'episodenumber': [1, 2],
    'episodenames': ['Children of the Gods (1)', 'Children of the Gods (2)']},

    {'input': '[Lunar] Bleach - 11-12 [B937F496]',
    'parsedseriesname': 'Bleach',
    'correctedseriesname': 'Bleach',
    'seasonnumber': None, 'episodenumber': [11, 12],
    'episodenames': ['The Legendary Quincy', 'A Gentle Right Arm']},

    {'input': 'scrubs.s01e01e02e03',
    'parsedseriesname': 'scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 1, 'episodenumber': [1, 2, 3],
    'episodenames': ['My First Day', 'My Mentor', 'My Best Friend\'s Mistake']},

    {'input': 'Scrubs - [02x01-03]',
    'parsedseriesname': 'scrubs',
    'correctedseriesname': 'Scrubs',
    'seasonnumber': 2, 'episodenumber': [1, 2, 3],
    'episodenames': ['My Overkill', 'My Nightingale', 'My Case Study']},

    {'input': 'Flight.of.the.Conchords.S01E01-02.An.Ep.name.avi',
    'parsedseriesname': 'Flight of the Conchords',
    'correctedseriesname': 'Flight of the Conchords',
    'seasonnumber': 1, 'episodenumber': [1, 2],
    'episodenames': ['Sally', 'Bret Gives Up The Dream']},
]

files['unicode'] = [
    {'input': u'DARKER THAN BLACK -\u9ed2\u306e\u5951\u7d04\u8005- - S01E01 (21st copy)',
    'parsedseriesname': u'darker than black -\u9ed2\u306e\u5951\u7d04\u8005-',
    'correctedseriesname': u'Darker than Black',
    'seasonnumber': 1, 'episodenumber': 1,
    'episodenames': [u'\u5951\u7d04\u306e\u661f\u306f\u6d41\u308c\u305f\u2026\u524d\u7de8']},

    {'input': u'Carniv\xe0le 1x11 - The Day of the Dead',
    'parsedseriesname': u'Carniv\xe0le',
    'correctedseriesname': u'Carniv\xe0le',
    'seasonnumber': 1, 'episodenumber': 11,
    'episodenames': ['The Day of the Dead']},

    {'input': u'T\xecnh Ng\u01b0\u1eddi Hi\u1ec7n \u0110\u1ea1i - [01x01]',
    'parsedseriesname': u'T\xecnh Ng\u01b0\u1eddi Hi\u1ec7n \u0110\u1ea1i',
    'correctedseriesname': u'Virtues Of Harmony II',
    'seasonnumber': 1, 'episodenumber': 1,
    'episodenames': [u'T\xecnh Ng\u01b0\u1eddi Hi\u1ec7n \u0110\u1ea1i - Virtues Of Harmony II']},
]

files['anime'] = [
    {'input': '[Eclipse] Fullmetal Alchemist Brotherhood - 02 (1280x720 h264) [8452C4BF]',
    'parsedseriesname': 'Fullmetal Alchemist Brotherhood',
    'correctedseriesname': 'Fullmetal Alchemist: Brotherhood',
    'seasonnumber': None, 'episodenumber': 2,
    'episodenames': ['The Day of the Beginning']},

    {'input': '[Shinsen-Subs] Armored Trooper Votoms - Pailsen Files - 01 [9E3F1D1C]',
    'parsedseriesname': 'armored trooper votoms - pailsen files',
    'correctedseriesname': 'Armored Trooper Votoms: Pailsen Files',
    'seasonnumber': None, 'episodenumber': 1,
    'episodenames': ['River Crossing Strategy']},

    {'input': '[Shinsen-Subs] Beet - 19 [24DAB497]',
    'parsedseriesname': 'beet',
    'correctedseriesname': 'Beet the Vandel Buster Excellion',
    'seasonnumber': None, 'episodenumber': 19,
    'episodenames': ['Windfang Flash! The Soul of a Wind Mage!']},

    {'input': '[AG-SHS]Victory_Gundam-03_DVD[FC6E3A6F]',
    'parsedseriesname': 'victory gundam',
    'correctedseriesname': 'Mobile Suit Victory Gundam',
    'seasonnumber': None, 'episodenumber': 3,
    'episodenames': ['Uso\'s Fight']},

    {'input': '[YuS-SHS]Gintama-24(H264)_[52CA4F8B]',
    'parsedseriesname': 'gintama',
    'correctedseriesname': 'Gintama',
    'seasonnumber': None, 'episodenumber': 24,
    'episodenames': ['A Cute Face is Always Hiding Something']},

    {'input': '[Shinsen-Subs] True Mazinger - 07 [848x480 H.264 Vorbis][787D0074]',
    'parsedseriesname': 'True Mazinger',
    'correctedseriesname': 'True Mazinger: Shocking! Z Chapter',
    'seasonnumber': None, 'episodenumber': 7,
    'episodenames': ['Legend! The Mechanical Beasts of Bardos!']},

    {'input': '[BSS]_Tokyo_Magnitude_8.0_-_02_[0E5C4A40]',
    'parsedseriesname': 'tokyo magnitude 8.0',
    'correctedseriesname': 'Tokyo Magnitude 8.0',
    'seasonnumber': None, 'episodenumber': 2,
    'episodenames': ['Broken World']},
]


def test_verify_test_data_sanity():
    """Checks all test data is consistent
    """
    from helpers import assertEquals

    keys = []
    for alltests in files.values():
        for ctest in alltests:
            keys.append(ctest.keys())

    for k1 in keys:
        for k2 in keys:
            assertEquals(sorted(k1), sorted(k2))
