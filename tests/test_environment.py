TEST_DIR="/tmp/pykgr_test"

import os
# os.environ["root_directory"] = TEST_DIR # No choice
import pykgr
pykgr.config.setup(TEST_DIR)
from pykgr.environment import initialize


def test_setup():
    initialize()

    assert os.path.exists(TEST_DIR) == True


if __name__ == "__main__":
    test_setup()
