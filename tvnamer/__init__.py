#!/usr/bin/env python

"""tvnamer - Automagical TV episode renamer

Uses data from www.thetvdb.com (via tvdb_api) to rename TV episode files from
"some.show.name.s01e01.blah.avi" to "Some Show Name - [01x01] - The First.avi"
"""

__version__ = "3.0.3"
__author__ = "dbr/Ben"

import os

if 'TVNAMER_COVERAGE_SUBPROCESS' in os.environ and 'COVERAGE_PROCESS_START' in os.environ:
    # Hackery for coverage testing in functional tests, based on
    # https://coverage.readthedocs.io/en/coverage-5.1/subprocess.html#configuring-python-for-sub-process-coverage
    import coverage
    coverage.process_startup()
