import pykgr
import os

class binutils(pykgr.Package):
    file_url = "http://ftp.gnu.org/gnu/binutils/binutils-2.35.tar.xz"
    file_name = "binutils-2.35.tar.xz"
    name = "binutils"
    version = "2.35"
      
    def configure(self):
        self.shell.command(
            "%s/configure" % self.code_directory,
            "--prefix=%s" % pykgr.config.builder_directory,
            "--with-lib-path=%s/lib" % pykgr.config.library_directory
        ).run(display_output = True)
