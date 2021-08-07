import pykgr
import os


class test_package(pykgr.Package):
    file_url = "https://ftp.gnu.org/gnu/hello/hello-2.9.tar.gz"
    file_name = "hello-2.9.tar.gz"
    name = "hello"
    version = "2.9"


def test_build():
    env = pykgr.Environment()
    env.build_package(test_package)


if __name__ == "__main__":
    test_build()