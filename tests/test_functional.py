#!/usr/bin/env python

"""Functional tests for tvnamer tests
"""

from functional_runner import run_tvnamer, verify_out_data
from nose.plugins.attrib import attr
from helpers import expected_failure_travisci



@attr("functional")
def test_renaming_always_doesnt_overwrite():
    """If trying to rename a file that exists, should not create new file
    """
    input_files = [
        'Scrubs.s01e01.avi',
        'Scrubs - [01x01] - My First Day.avi']

    expected_files = [
        'Scrubs.s01e01.avi',
        'Scrubs - [01x01] - My First Day.avi']

    out_data = run_tvnamer(
        with_files = input_files,
        with_flags = ['--batch'])

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_not_recursive():
    """Tests the nested files aren't found when not recursive
    """
    input_files = [
        'Scrubs.s01e01.avi',
        'nested/subdir/Scrubs.s01e02.avi']

    expected_files = [
        'Scrubs - [01x01] - My First Day.avi',
        'nested/subdir/Scrubs.s01e02.avi']

    out_data = run_tvnamer(
        with_files = input_files,
        with_flags = ['--not-recursive', '--batch'],
        run_on_directory = True)

    verify_out_data(out_data, expected_files)


@attr("functional")
def test_no_seasonnumber():
    """Test episode with no series number
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.e01.avi'],
        with_flags = ['--batch'])

    expected_files = ['Scrubs - [01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


