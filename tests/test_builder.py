import pykgr
from pykgr.subroutines import add_module, import_from_string, setup_paths
import os
import sys
from common import get_current_path
pykgr.config.setup("/tmp/pykgr_test")


def test_loading_module():
    path = get_current_path()
    base_module = path+"base"
    add_module(base_module)

    assert base_module in sys.path


def test_builder_setup():
    builder = pykgr.Builder(directory=pykgr.config.builder_directory)
    builder.build_toolchain()


if __name__ == "__main__":
    test_loading_module()
    test_builder_setup()