#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Exceptions used through-out tvnamer
"""


class BaseTvnamerException(Exception):
    """Base exception all tvnamers exceptions inherit from
    """
    pass


class InvalidPath(BaseTvnamerException):
    """Raised when an argument is a non-existent file or directory path
    """
    pass


class NoValidFilesFoundError(BaseTvnamerException):
    """Raised when no valid files are found. Effectively exits tvnamer
    """
    pass


class InvalidFilename(BaseTvnamerException):
    """Raised when a file is parsed, but no episode info can be found
    """
    pass

class BaseConfigError(BaseTvnamerException):
    """Base exception for config errors
    """
    pass


class InvalidConfigFile(BaseConfigError):
    """Raised if the config file is malformed or unreadable
    """
    pass

class WrongConfigVersion(BaseTvnamerException):
    """Config versions do not match"""
    pass
