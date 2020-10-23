import pykgr
import os

class glibc(pykgr.Package):
    file_url = "http://ftp.gnu.org/gnu/glibc/glibc-2.32.tar.xz"
    file_name = "glibc-2.32.tar.xz"
    name = "glibc"
    version = "2.32"
      
    def configure(self):
        self.shell.command(
            "%s/configure" % self.code_directory,
            "--prefix=%s" % pykgr.config.library_directory
        ).run(display_output = True)
