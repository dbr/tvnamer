#!/usr/bin/env python

"""Constructs command line argument parser for tvnamer
"""

import sys
import optparse


class Group(object):
    """Simple helper context manager to add a group to an OptionParser
    """

    def __init__(self, parser, name):
        self.parser = parser
        self.name = name
        self.group = optparse.OptionGroup(self.parser, name)

    def __enter__(self):
        return self.group

    def __exit__(self, *k, **kw):
        self.parser.add_option_group(self.group)


def getCommandlineParser(defaults):
    parser = optparse.OptionParser(usage = "%prog [options] <files>", add_help_option = False)

    parser.set_defaults(**defaults)

    # Console output
    with Group(parser, "Console output") as g:
        g.add_option("-v", "--verbose", action="store_true", dest="verbose", help = "show debugging info")
        g.add_option("-q", "--not-verbose", action="store_false", dest="verbose", help = "no verbose output (useful to override 'verbose':true in config file)")
        g.add_option("--dry-run", action="store_true", dest="dry_run", help = "Only tell what script is going to do")

    # Batch options
    with Group(parser, "Batch options") as g:
        g.add_option("-a", "--always", action="store_true", dest="always_rename", help = "Always renames files (but prompt for correct series)")
        g.add_option("--not-always", action="store_true", dest="always_rename", help = "Overrides --always")

        g.add_option("-f", "--selectfirst", action="store_true", dest="select_first", help = "Select first series search result automatically")
        g.add_option("--not-selectfirst", action="store_false", dest="select_first", help = "Overrides --selectfirst")

        g.add_option("-b", "--batch", action="store_true", dest = "batch", help = "Rename without human intervention, same as --always and --selectfirst combined")
        g.add_option("--not-batch", action="store_false", dest = "batch", help = "Overrides --batch")

    # Config options
    with Group(parser, "Config options") as g:
        g.add_option("-c", "--config", action = "store", dest = "loadconfig", help = "Load config from this file")
        g.add_option("-s", "--save", action = "store", dest = "saveconfig", help = "Save configuration to this file and exit")
        g.add_option("-p", "--preview-config", action = "store_true", dest = "showconfig", help = "Show current config values and exit")

    # Override values
    with Group(parser, "Override values") as g:
        g.add_option("-n", "--name", action="store", dest = "force_name", help = "override the parsed series name with this (applies to all files)")
        g.add_option("--series-id", action="store", dest = "series_id", help = "explicitly set the show id for TVdb to use (applies to all files)")
        g.add_option("--order", action = "store", dest = "order", help = "set the TvDB episode order ('aired' [default] or 'dvd')")

    # Misc
    with Group(parser, "Misc") as g:
        g.add_option("-r", "--recursive", action="store_true", dest = "recursive", help = "Descend more than one level directories supplied as arguments")
        g.add_option("--not-recursive", action="store_false", dest = "recursive", help = "Only descend one level into directories")

        g.add_option("-m", "--move", action="store_true", dest="move_files_enable", help = "Move files to destination specified in config or with --movedestination argument")
        g.add_option("--not-move", action="store_false", dest="move_files_enable", help = "Files will remain in current directory")

        g.add_option("--force-move", action="store_true", dest = "overwrite_destination_on_move", help = "Force move and potentially overwrite existing files in destination folder")
        g.add_option("--force-rename", action="store_true", dest = "overwrite_destination_on_rename", help = "Force rename source file")
        
        g.add_option("-d", "--movedestination", action="store", dest = "move_files_destination", help = "Destination to move files to. Variables: %(seriesname)s %(seasonnumber)d %(episodenumbers)s")

        g.add_option("-h", "--help", action="help", help = "show this help message and exit")


    return parser
