import pykgr
import os


class Python(pykgr.Package):
    file_url = "https://github.com/python/cpython/archive/3.9.tar.gz"
    name = "cpython"
    version = "3.9"
    file_name = "3.9.tar.gz"
    no_build_dir = True

    def configure(self):
        self.shell.command(
            "./configure",
            "--prefix=%s" % pykgr.config.packages_directory,
            "--enable-optimizations"
        ).run()
