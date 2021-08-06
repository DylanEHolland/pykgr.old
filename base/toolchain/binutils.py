import pykgr
import os
from base.packages.binutils import binutils as binutils_main


class binutils(binutils_main):
    def configure(self):
        self.shell.command(
            "%s/configure" % self.code_directory,
            "--prefix=%s" % pykgr.config.builder_directory
        ).run(display_output = True)
