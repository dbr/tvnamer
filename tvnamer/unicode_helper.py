#!/usr/bin/env python

"""Helpers to deal with strings, unicode objects and terminal output
"""

import sys
from tvnamer.compat import PY2, string_type


def p(*args, **kw):
    """Rough implementation of the Python 3 print function,
    http://www.python.org/dev/peps/pep-3105/

    def print(*args, sep=' ', end='\n', file=None)
    """

    kw.setdefault('encoding', 'utf-8')
    kw.setdefault('sep', ' ')
    kw.setdefault('end', '\n')
    kw.setdefault('file', sys.stdout)

    if not PY2:
        print(kw['sep'].join(string_type(x) for x in args))
        return

    new_args = []
    for x in args:
        if not isinstance(x, basestring):
            new_args.append(repr(x))
        else:
            if kw['encoding'] is not None:
                new_args.append(x.encode(kw['encoding']))
            else:
                new_args.append(x)

    out = kw['sep'].join(new_args)

    kw['file'].write(out + kw['end'])
