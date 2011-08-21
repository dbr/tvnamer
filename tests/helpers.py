#!/usr/bin/env python


"""Helper functions for use in tests
"""


def assertEquals(a, b):
    assert a == b, "Error, %r not equal to %r" % (a, b)


def assertType(obj, type):
    assert isinstance(obj, type), "Expecting %s, got %r" % (
        type(obj),
        type)
