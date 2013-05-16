#!/usr/bin/env python

import os
import sys
import shutil
import logging

from unicode_helper import p
from config import Config


__all__ = ["Renamer"]


def log():
    """Returns the logger for current file
    """
    return logging.getLogger(__name__)


def same_partition(f1, f2):
    """Returns True if both files or directories are on the same partition
    """
    return os.stat(f1).st_dev == os.stat(f2).st_dev


def delete_file(fpath):
    """On OS X: Trashes a path using the Finder, via OS X's Scripting Bridge.
    On other platforms: unlinks file.
    """

    try:
        from AppKit import NSURL
        from ScriptingBridge import SBApplication
    except ImportError:
        p("Deleting %s" % fpath)
        log().debug("Deleting %r" % fpath)
        os.unlink(fpath)
    else:
        p("Trashing %s" % fpath)
        log().debug("Trashing %r" % fpath)
        targetfile = NSURL.fileURLWithPath_(fpath)
        finder = SBApplication.applicationWithBundleIdentifier_("com.apple.Finder")
        items = finder.items().objectAtLocation_(targetfile)
        items.delete()


def rename_file(old, new):
    """Rename 'old' file to 'new'. Both files must be on the same partition.
    Preserves access and modification time.
    """
    p("Renaming %s to %s" % (old, new))
    log().debug("Renaming %r to %r" % (old, new))
    stat = os.stat(old)
    os.rename(old, new)
    os.utime(new, (stat.st_atime, stat.st_mtime))


def copy_file(old, new):
    """Copy 'old' file to 'new'.
    """
    p("Copying %s to %s" % (old, new))
    log().debug("Copying %r to %r" % (old, new))
    shutil.copyfile(old, new)
    shutil.copystat(old, new)


def symlink_file(target, name):
    """Create symbolic link named 'name' pointing to 'target'.
    """
    p("Creating symlink %s to %s" % (name, target))
    log().debug("Creating symlink %r to %r" % (name, target))
    os.symlink(target, name)


class Renamer(object):
    """Deals with renaming of files
    """

    def __init__(self, filename):
        self.filename = os.path.abspath(filename)

    def rename(self, new_fullpath=None, force=False, always_copy=False, always_move=False, leave_symlink=False, create_dirs=True):
        """Moves the file to a new path.

        If it is on the same partition, it will be moved (unless always_copy is True)
        If it is on a different partition, it will be copied, and the original
        only deleted if always_move is True.
        If the target file already exists, it will raise OSError unless force is True.
        If it was moved, a symlink will be left behind with the original name
        pointing to the file's new destination if leave_symlink is True.
        """

        new_dir = os.path.dirname(new_fullpath)

        if create_dirs:
            p("Creating directory %s" % new_dir)
            try:
                os.makedirs(new_dir)
            except OSError, e:
                if e.errno != 17:
                    raise

        if os.path.exists(new_fullpath):
            # If the destination exists, raise exception unless force is True
            if not force:
                raise OSError("File %s already exists, not forcefully moving %s" % (
                    new_fullpath, self.filename))

        if same_partition(self.filename, new_dir):
            if always_copy:
                # Same partition, but forced to copy
                copy_file(self.filename, new_fullpath)
            else:
                # Same partition, just rename the file to move it
                rename_file(self.filename, new_fullpath)

                # Leave a symlink behind if configured to do so
                if leave_symlink:
                    symlink_file(new_fullpath, self.filename)
        else:
            # File is on different partition (different disc), copy it
            copy_file(self.filename, new_fullpath)
            if always_move:
                # Forced to move file, we just trash old file
                delete_file(self.filename)

                # Leave a symlink behind if configured to do so
                if leave_symlink:
                    symlink_file(new_fullpath, self.filename)

        self.filename = new_fullpath
