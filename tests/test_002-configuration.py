import pykgr
import os
from pykgr.subroutines import load_config


def test_configuration_files():
    home = os.environ.get("HOME")
    initial_dir = pykgr.config.main_directory
    pykgr.config.from_file("%s/.pykgr.json" % home)

    assert initial_dir != pykgr.config.main_directory


def test_load_config():
    pass#load_config


if __name__ == "__main__":
    test_configuration_files()