import pykgr
import os


class test_package(pykgr.Package):
    file_url = "http://ftp.gnu.org/gnu/binutils/binutils-2.35.tar.xz"
    file_name = "binutils-2.35.tar.xz"
    name = "binutils"
    version = "2.35"

    def configure(self):
        self.shell.command(
            "%s/configure" % self.code_directory,
            "--prefix=%s" % "/tmp/binutils",
            #"--with-lib-path=%s/lib" % pykgr.config.library_directory
        ).run(display_output=True)


def test_build():
    env = pykgr.Environment()
    env.build_package(test_package)


if __name__ == "__main__":
    test_build()