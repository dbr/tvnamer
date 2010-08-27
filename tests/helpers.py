#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Helper functions for use in tests
"""


def assertEquals(a, b):
    assert a == b, "Error, %r not equal to %r" % (a, b)


def assertType(obj, type):
    assert isinstance(obj, type), "Expecting %s, got %r" % (
        type(obj),
        type)
