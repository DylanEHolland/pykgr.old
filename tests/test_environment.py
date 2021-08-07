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


class Vim(pykgr.Package):
    file_url = "https://github.com/vim/vim/archive/refs/tags/v8.2.3301.tar.gz"
    file_name = "v8.2.3301.tar.gz"
    name = "vim"
    version = "8.2.3301"
    sub_directory_location = "/src"

    def __initialize__(self):
        self.code_directory = self.code_directory + "/src"#self.sub_directory_location
        self.build_directory = self.code_directory

    def configure(self):
        # Vim doesn't use autoconf
        self.shell.cd(self.code_directory)
        self.shell.make("distclean", display_output=True)
        self.shell.configure("--prefix="+pykgr.config.packages_directory)

    def install(self):
        self.shell.make(
            "-j%s" % pykgr.config.make_opts,
            "DESTDIR="+pykgr.config.packages_directory,
            "install",
            display_output=True
        )

    def prepare(self):
        pass


def test_setup():
    initialize()

    assert os.path.exists(TEST_DIR) == True


def test_build():
    env = pykgr.Environment()

    env.build_package(Hello)
    assert os.path.exists(pykgr.config.packages_directory+"/bin/hello") is True

    env.build_package(Vim)
    assert os.path.exists(pykgr.config.packages_directory+"/bin/vi") is True


if __name__ == "__main__":
    test_setup()
    test_build()
