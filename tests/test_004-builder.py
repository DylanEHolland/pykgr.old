import pykgr
from pykgr.subroutines import add_module, import_from_string, setup_paths
import sys
from common import get_current_path
from pykgr.environment import initialize

pykgr.config.setup("/tmp/pykgr_test")


def test_loading_module():
    path = get_current_path()
    base_module = path+"base"
    add_module(base_module)

    assert base_module in sys.path


def test_builder_setup():
    initialize()
    builder = pykgr.Builder(directory=pykgr.config.builder_directory)
    builder.build_toolchain()


def test_build_world():
    initialize()
    builder = pykgr.Builder(directory=pykgr.config.builder_directory)
    builder.build_world()


if __name__ == "__main__":
    test_loading_module()
    test_builder_setup()
    test_build_world()
