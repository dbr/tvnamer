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
]

files['misc'] = [
    {'input': 'Six.Feet.Under.S0201.test_testing-yay',
    'parsedseriesname': 'Six Feet Under',
    'correctedseriesname': 'Six Feet Under',
    'seasonnumber': 2, 'episodenumber': 1,
    'episodenames': ['In The Game']},
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

# files['unicode'] = [
#     {'input': u'DARKER THAN BLACK -\xe9\xbb\x92\xe3\x81\xae\xe5\xa5\x91\xe7\xb4\x84\xe8\x80\x85- - S01E01 (21st copy)',
#     'parsedseriesname': u'darker than black -\xe9\xbb\x92\xe3\x81\xae\xe5\xa5\x91\xe7\xb4\x84\xe8\x80\x85-',
#     'correctedseriesname': u'darker than black -\xe9\xbb\x92\xe3\x81\xae\xe5\xa5\x91\xe7\xb4\x84\xe8\x80\x85-',
#     'seasonnumber': 1, 'episodenumber': 1,
#     'episodenames': ['The Star of Contract Flowed... (1st Part)']},
# 
#     {'input': u'Carniv\xc3\xa0le 1x11 - The Day of the Dead',
#     'parsedseriesname': u'Carniv\xc3\xa0le',
#     'correctedseriesname': u'Carniv\xc3\xa0le',
#     'seasonnumber': 1, 'episodenumber': 11,
#     'episodenames': ['The Day of the Dead']},
# 
#     {'input': 't\xc3\xacnh ng\xc6\xb0\xe1\xbb\x9di hi\xe1\xbb\x87n \xc4\x91\xe1\xba\xa1i - [01x01]',
#     'parsedseriesname': 't\xc3\xacnh ng\xc6\xb0\xe1\xbb\x9di hi\xe1\xbb\x87n \xc4\x91\xe1\xba\xa1i',
#     'correctedseriesname': u't\xc3\xacnh ng\xc6\xb0\xe1\xbb\x9di hi\xe1\xbb\x87n \xc4\x91\xe1\xba\xa1i',
#     'seasonnumber': 1, 'episodenumber': 1,
#     'episodenames': [u'T\xc3\xacNh Ng\xc6\xb0\xe1\xbb\x9dI Hi\xe1\xbb\x87N \xc4\x91\xe1\xba\xa1I - Virtues Of Harmony II']
#     },
# ]

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
    'correctedseriesname': 'Beet the Vandel Buster',
    'seasonnumber': None, 'episodenumber': 19,
    'episodenames': ['Threat of the Planet Earth']},

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

    {'input': '[BSS]_Tokyo_Magnitude_8.0_-_02_[0E5C4A40].mkv',
    'parsedseriesname': 'tokyo magnitude 8 0',
    'seasonnumber': None, 'episodenumber': 2,
    'episodenames': ['Broken World']},
]
