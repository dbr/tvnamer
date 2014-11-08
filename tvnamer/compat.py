import sys

PY2 = sys.version_info[0] == 2

if PY2:
    string_type = unicode
else:
    string_type = str

if PY2:
    all_string_types = (basestring,)
else:
    all_string_types = (str,)

if PY2:
    raw_input = raw_input
else:
    raw_input = input
