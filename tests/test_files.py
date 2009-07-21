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
    'seasonnumber': 4, 'episodenumber': 19
    },
    {'input': 'Scrus - [02x11]',
    'seasonnumber': 2, 'episodenumber': 11
    },
]

files['s01e01_format'] = [
    {'input': 'scrubs.s01e01',
    'seasonnumber': 1, 'episodenumber': 1
    },
    {'input': 'my.name.is.earl.s01e01',
    'seasonnumber': 1, 'episodenumber': 1
    },
    {'input': 'scrubs.s0e24.blah.fake',
    'seasonnumber': 1, 'episodenumber': 1
    },
]

files['multiple_episodes'] = [
    {'input': 'scrubs.s01e23e24',
    'seasonnumber': 1, 'episodenumber': [23, 24]
    },
    {'input': 'Stargate SG-1 - [01x01-02]',
    'seasonnumber': 1, 'episodenumber': [1, 2]
    },
    {'input': '[Lunar] Bleach - 52-53 [B937F496]',
    'seasonnumber': None, 'episodenumber': [52, 53]
    },
    {'input': 'scrubs.s01e01e02e03',
    'seasonnumber': 1, 'episodenumber': [1, 2, 3]
    },
    {'input': 'Scrubs - [02x01-03]',
    'seasonnumber': 2, 'episodenumber': [1, 2, 3]
    },
]

files['unicode'] = [
    {'input': 'DARKER THAN BLACK -\xe9\xbb\x92\xe3\x81\xae\xe5\xa5\x91\xe7\xb4\x84\xe8\x80\x85- - S01E01 (21st copy)',
    'seasonnumber': 1, 'episodenumber': 1
    },
    {'input': 'Carniv\xc3\xa0le 1x11 - The Day of the Dead',
    'seasonnumber': 1, 'episodenumber': 11
    },
    {'input': 't\xc3\xacnh ng\xc6\xb0\xe1\xbb\x9di hi\xe1\xbb\x87n \xc4\x91\xe1\xba\xa1i - [01x01]',
    'seasonnumber': 1, 'episodenumber': 1
    },
]

files['anime'] = [
    {'input': '[Eclipse] Fullmetal Alchemist Brotherhood - 02 (1280x720 h264) [8452C4BF]',
    'seasonnumber': None, 'episodenumber': 2
    },
    {'input': '[Shinsen-Subs] Armored Trooper Votoms - Pailsen Files - 01 [9E3F1D1C]',
    'seasonnumber': None, 'episodenumber': 1
    },
    {'input': '[Shinsen-Subs] Beet - 19 [24DAB497]',
    'seasonnumber': None, 'episodenumber': 19
    },
    {'input': '[AG-SHS]Victory_Gundam-03_DVD[FC6E3A6F]',
    'seasonnumber': None, 'episodenumber': 3
    },
    {'input': '[YuS-SHS]Gintama-88(H264)_[52CA4F8B]',
    'seasonnumber': None, 'episodenumber': 88
    },
    {'input': '[Shinsen-Subs] True Mazinger - 07 [848x480 H.264 Vorbis][787D0074]',
    'seasonnumber': None, 'episodenumber': 7
    }
]
