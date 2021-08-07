import pykgr
import os
from base.packages.gcc import gcc as gcc_old


class Gcc(gcc_old):
    def prepare(self):
        # Overloads prepare instead of configure to download prequisites
        
        self.shell.cd(self.code_directory)
        self.shell.command(
            "%s/contrib/download_prerequisites" % self.code_directory
        ).run(display_output=True)
        
        if not os.path.exists(self.build_directory):
            os.mkdir(self.build_directory)
        self.shell.cd(self.build_directory)

        self.shell.command(
            "%s/configure" % self.code_directory,
            "--build=x86_64-linux-gnu",
            "--prefix=%s" % pykgr.config.builder_directory,
            "--enable-checking=release",
            "--enable-languages=c,c++,fortran",
            "--disable-bootstrap",
            "--disable-multilib"
        ).run(display_output = True)
