import pykgr
import os
TEST_DIR="/tmp/pykgr_test"
pykgr.config.setup(TEST_DIR)
from pykgr.environment import initialize


def test_setup():
    initialize()

    assert os.path.exists(TEST_DIR) == True


def test_destroy():
    env = pykgr.environment.Environment()

    if os.path.exists(TEST_DIR):
        assert env.destroy() is True
        assert not os.path.exists(TEST_DIR)


if __name__ == "__main__":
    test_setup()
    test_destroy()
