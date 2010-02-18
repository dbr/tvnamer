#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Helpers to deal with strings, unicode objects and terminal output
"""

import sys


def unicodify(object, encoding = "utf-8"):
    if isinstance(object, basestring):
        if not isinstance(object, unicode):
            object = unicode(object, encoding)
    return object


def p(*args, **kw):
    """Rough implementation of the Python 3 print function,
    http://www.python.org/dev/peps/pep-3105/

    def print(*args, sep=' ', end='\n', file=None)

    """
    kw.setdefault('encoding', 'utf-8')
    kw.setdefault('sep', ' ')
    kw.setdefault('end', '\n')
    kw.setdefault('file', sys.stdout)

    args = [repr(x) for x in args if not isinstance(x, basestring)]
    out = kw['sep'].join(x.encode(kw['encoding']) for x in args)

    kw['file'].write(out + kw['end'])
