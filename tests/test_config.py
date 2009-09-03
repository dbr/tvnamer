#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Test tvnamer's config loading and saving
"""

import os
import sys
import unittest
import tempfile

sys.path.append(os.path.join(os.path.abspath(sys.path[0]), ".."))
from config import Config

def test_saving_loading():
    """Tests saving the default config to a temp folder, and reloading it
    """
    
    # Save config
    fid, fname = tempfile.mkstemp()
    Config.useDefaultConfig()
    Config.saveConfig(fname)
    assert len(open(fname).read()) > 10, "Config file is less than 10 characters long"
    
    # Make copy of config dict
    saved_config = dict(Config)
    
    # Clear config
    Config.loadConfig(fname)
    new_config = dict(Config)
    
    # Compare
    
    assert saved_config == new_config, "Configs do not match"

if __name__ == '__main__':
    import nose
    nose.main()
