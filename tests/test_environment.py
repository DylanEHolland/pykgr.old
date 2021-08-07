TEST_DIR="/tmp/pykgr_test"

import os
# os.environ["root_directory"] = TEST_DIR # No choice
import pykgr
pykgr.config.setup(TEST_DIR)
from pykgr.environment import initialize


class Hello(pykgr.Package):
    file_url = "https://ftp.gnu.org/gnu/hello/hello-2.9.tar.gz"
    file_name = "hello-2.9.tar.gz"
    name = "hello"
    version = "2.9"


class Bash(pykgr.Package):
    file_url = "http://ftp.gnu.org/gnu/bash/bash-5.0.tar.gz"
    file_name = "bash-5.0.tar.gz"
    name = "bash"
    version = "5.0"


def test_setup():
    initialize()

    assert os.path.exists(TEST_DIR) == True


def test_build():
    env = pykgr.Environment()

    env.build_package(Hello)
    assert os.path.exists(pykgr.config.packages_directory+"/bin/hello") is True

    env.build_package(Bash)
    assert os.path.exists(pykgr.config.packages_directory+"/bin/bash") is True


if __name__ == "__main__":
    test_setup()
    #test_build()