#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Functional-test runner for use in other tests

Useful functions are run_tvnamer and verify_out_data.

Simple example test:

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_config = None,
        with_input = "1\ny\n")

    expected_files = ['Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)

This runs tvnamer with no custom config (can be a string). It then
sends "1[return]y[return]" to the console UI, and verifies the file was
created correctly, in a way that nosetest displays useful info when an
expected file is not found.
"""

import os
import sys
import tempfile
from subprocess import Popen, PIPE


def make_temp_config(config):
    (fhandle, fname) = tempfile.mkstemp()
    f = open(fname, 'w+')
    f.write(config)
    f.close()

    return fname


def get_tvnamer_path():
    """Gets the path to tvnamer/main.py
    """
    cur_location, _ = os.path.split(os.path.abspath(sys.path[0]))
    for cdir in [".", ".."]:
        tvnamer_location = os.path.abspath(
            os.path.join(cur_location, cdir, "tvnamer", "main.py"))

        if os.path.isfile(tvnamer_location):
            return tvnamer_location
        else:
            print tvnamer_location
    else:
        raise IOError("tvnamer could not be found in . or ..")


def make_temp_dir():
    return tempfile.mkdtemp()


def make_dummy_files(files, location):
    dummies = []
    for f in files:
        floc = os.path.join(location, f)
        open(floc, "w").close()
        dummies.append(floc)

    return dummies


def clear_temp_dir(location):
    print "Clearing %s" % location
    for f in os.listdir(location):
        fullpath = os.path.join(location, f)
        os.unlink(fullpath)


def run_tvnamer(with_files, with_flags = None, with_input = "", with_config = None):
    # Create dummy files (config and episodes)
    tvnpath = get_tvnamer_path()
    episodes_location = make_temp_dir()
    dummy_files = make_dummy_files(with_files, episodes_location)

    if with_config is not None:
        configfname = make_temp_config(with_config)
        conf_args = ['-c', configfname]
    else:
        conf_args = []

    if with_flags is None:
        with_flags = []

    # Construct command
    cmd = [sys.executable, tvnpath] + conf_args + with_flags + dummy_files
    print "Running command:"
    print " ".join(cmd)

    proc = Popen(
        cmd,
        stdout = PIPE,
        stderr = PIPE,
        stdin = PIPE)

    proc.stdin.write(with_input)
    stdout, stderr = proc.communicate()

    files = os.listdir(episodes_location)

    # Clean up dummy files and config
    clear_temp_dir(episodes_location)
    if with_config is not None:
        os.unlink(configfname)

    return {
        'stdout': stdout,
        'stderr': stderr,
        'files': files}


def verify_out_data(out_data, expected_files):
    """Verifies the out_data from run_tvnamer contains the expected files.

    Prints the stdout/stderr/files, then asserts all files exist.
    If an assertion fails, nosetest will handily print the stdout/etc.
    """

    print "Expected files:", expected_files
    print "Got files:", out_data['files']

    print "\n" + "*" * 20 + "\n"
    print "stdout:\n"
    print out_data['stdout']

    print "\n" + "*" * 20 + "\n"
    print "stderr:\n"
    print out_data['stderr']

    for cur in expected_files:
        if cur not in out_data['files']:
            raise AssertionError(
                "File named %r not created" % (cur))
