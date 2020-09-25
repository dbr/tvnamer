#!/usr/bin/env python

"""Holds Config singleton
"""

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .config_defaults import TypedDefaults

from tvnamer.config_defaults import defaults

Config = dict(defaults) # type: TypedDefaults
