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
    'seriesname': 'scrubs',
    'seasonnumber': 4, 'episodenumber': 19},
    {'input': 'Scrubs - [02x11]',
    'seriesname': 'scrubs',
    'seasonnumber': 2, 'episodenumber': 11},
]

files['s01e01_format'] = [
    {'input': 'scrubs.s01e01',
    'seriesname': 'scrubs',
    'seasonnumber': 1, 'episodenumber': 1},
    {'input': 'my.name.is.earl.s01e01',
    'seriesname': 'my name is earl',
    'seasonnumber': 1, 'episodenumber': 1},
    {'input': 'scrubs.s01e24.blah.fake',
    'seriesname': 'scrubs',
    'seasonnumber': 1, 'episodenumber': 24},
]

files['misc'] = [
    {'input': 'Six.Feet.Under.S0201.test_testing-yay',
    'seriesname': 'six feet under',
    'seasonnumber': 2, 'episodenumber': 1},
]

files['multiple_episodes'] = [
    {'input': 'Scrubs - [01x01-02-03]',
    'seriesname': 'scrubs',
    'seasonnumber': 1, 'episodenumber': [1, 2, 3],
    },
    {'input': 'scrubs.s01e23e24',
    'seriesname': 'scrubs',
    'seasonnumber': 1, 'episodenumber': [23, 24]},
    {'input': 'Stargate SG-1 - [01x01-02]',
    'seriesname': 'stargate sg-1',
    'seasonnumber': 1, 'episodenumber': [1, 2]},
    {'input': '[Lunar] Bleach - 52-53 [B937F496]',
    'seriesname': 'bleach',
    'seasonnumber': None, 'episodenumber': [52, 53]},
    {'input': 'scrubs.s01e01e02e03',
    'seriesname': 'scrubs',
    'seasonnumber': 1, 'episodenumber': [1, 2, 3]},
    {'input': 'Scrubs - [02x01-03]',
    'seriesname': 'scrubs',
    'seasonnumber': 2, 'episodenumber': [1, 2, 3]},
    {'input': 'Flight.of.the.Conchords.S01E01-02.An.Ep.name.avi',
    'seriesname': 'Flight of the Conchords',
    'seasonnumber': 1, 'episodenumber': [1, 2]},
]

files['unicode'] = [
    {'input': 'DARKER THAN BLACK -\xe9\xbb\x92\xe3\x81\xae\xe5\xa5\x91\xe7\xb4\x84\xe8\x80\x85- - S01E01 (21st copy)',
    'seriesname': 'darker than black -\xe9\xbb\x92\xe3\x81\xae\xe5\xa5\x91\xe7\xb4\x84\xe8\x80\x85-',
    'seasonnumber': 1, 'episodenumber': 1},
    {'input': 'Carniv\xc3\xa0le 1x11 - The Day of the Dead',
    'seriesname': 'Carniv\xc3\xa0le',
    'seasonnumber': 1, 'episodenumber': 11},
    {'input': 't\xc3\xacnh ng\xc6\xb0\xe1\xbb\x9di hi\xe1\xbb\x87n \xc4\x91\xe1\xba\xa1i - [01x01]',
    'seriesname': 't\xc3\xacnh ng\xc6\xb0\xe1\xbb\x9di hi\xe1\xbb\x87n \xc4\x91\xe1\xba\xa1i',
    'seasonnumber': 1, 'episodenumber': 1},
]

files['anime'] = [
    {'input': '[Eclipse] Fullmetal Alchemist Brotherhood - 02 (1280x720 h264) [8452C4BF]',
    'seriesname': 'fullmetal alchemist brotherhood',
    'seasonnumber': None, 'episodenumber': 2},
    {'input': '[Shinsen-Subs] Armored Trooper Votoms - Pailsen Files - 01 [9E3F1D1C]',
    'seriesname': 'armored trooper votoms - pailsen files',
    'seasonnumber': None, 'episodenumber': 1},
    {'input': '[Shinsen-Subs] Beet - 19 [24DAB497]',
    'seriesname': 'beet',
    'seasonnumber': None, 'episodenumber': 19},
    {'input': '[AG-SHS]Victory_Gundam-03_DVD[FC6E3A6F]',
    'seriesname': 'victory gundam',
    'seasonnumber': None, 'episodenumber': 3},
    {'input': '[YuS-SHS]Gintama-88(H264)_[52CA4F8B]',
    'seriesname': 'gintama',
    'seasonnumber': None, 'episodenumber': 88},
    {'input': '[Shinsen-Subs] True Mazinger - 07 [848x480 H.264 Vorbis][787D0074]',
    'seriesname': 'true mazinger',
    'seasonnumber': None, 'episodenumber': 7},
]
