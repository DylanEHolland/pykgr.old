from pykgr import config

import os

def build_directories():
    for d in [config.main_directory, config.source_directory, config.source_tarballs_directory]:
        if not os.path.exists(d):
            os.mkdir(d)

def initialize():
    build_directories()