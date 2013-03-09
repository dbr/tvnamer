#!/usr/bin/env python

""" Test unicode support in tvnamer
"""

from functional_runner import run_tvnamer, verify_out_data
from nose.plugins.attrib import attr

import unicodedata


@attr("functional")
def test_unicode_in_inputname():
    """Tests parsing a file with unicode in the input filename
    """
    input_files = [
        unicodedata.normalize('NFC', u'The Big Bang Theory - S02E07 - The Panty Pin\u0303ata Polarization.avi')]

    expected_files = [
        unicodedata.normalize('NFC', u'The Big Bang Theory - [02x07] - The Panty Pin\u0303ata Polarization.avi')]

    out_data = run_tvnamer(
        with_files = input_files,
        with_flags = ["--batch"])

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_unicode_in_search_results():
    """Show with unicode in search results
    """
    input_files = [
        'psych.s04e11.avi']

    expected_files = [
        'Psych - [04x11] - Thrill Seekers & Hell Raisers.avi']

    out_data = run_tvnamer(
        with_files = input_files,
        with_input = '1\ny\n')

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_not_overwritting_unicode_filename():
    """Test no error occurs when warning about a unicode filename being overwritten
    """
    input_files = [
        u'The Big Bang Theory - S02E07.avi',
        unicodedata.normalize('NFC', u'The Big Bang Theory - [02x07] - The Panty Pin\u0303ata Polarization.avi')]

    expected_files = [
        u'The Big Bang Theory - S02E07.avi',
        unicodedata.normalize('NFC', u'The Big Bang Theory - [02x07] - The Panty Pin\u0303ata Polarization.avi')]

    out_data = run_tvnamer(
        with_files = input_files,
        with_flags = ['--batch'])

    verify_out_data(out_data, expected_files)

