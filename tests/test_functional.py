#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Functional tests for tvnamer tests
"""

from functional_runner import run_tvnamer, verify_out_data


def test_simple_functionality():
    """Tests renaming single files at a time
    """
    tests = [
        {'in':'scrubs.s01e01.hdtv.fake.avi',
        'expected':'Scrubs - [01x01] - My First Day.avi'},
        {'in':'my.name.is.earl.s01e01.fake.avi',
        'expected':'My Name Is Earl - [01x01] - Pilot.avi'},
        {'in':'a.fake.show.s12e24.fake.avi',
        'expected':'a fake show - [12x24].avi'},
        {'in': 'total.access.s01e01.avi',
        'expected': 'Total Access 24_7 - [01x01] - Episode #1.avi'},
    ]

    for curtest in tests:
        out_data = run_tvnamer(
            with_files = [curtest['in'], ],
            with_flags = ['--batch'],
        )
        verify_out_data(out_data, [curtest['expected'], ])