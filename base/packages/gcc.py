import pykgr
import os


class Gcc(pykgr.Package):
    file_url = "http://ftp.gnu.org/gnu/gcc/gcc-10.2.0/gcc-10.2.0.tar.xz"
    file_name = "gcc-10.2.0.tar.xz"
    name = "gcc"
    version = "10.2.0"

    def configure(self):
        self.shell.command(
            "%s/configure" % self.code_directory,
            "--build=x86_64-linux-gnu",
            "--prefix=%s" % pykgr.config.builder_directory,
            "--enable-checking=release",
            "--enable-languages=c,c++,fortran",
            "--disable-bootstrap",
            "--disable-multilib"            
        ).run(display_output = True)
