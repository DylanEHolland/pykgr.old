import pykgr
import os

class gcc(pykgr.Package):
    file_url = "http://ftp.gnu.org/gnu/gcc/gcc-10.2.0/gcc-10.2.0.tar.xz"
    file_name = "gcc-10.2.0.tar.xz"
    name = "gcc"
    version = "10.2.0"

    def fetch(self):
        self.shell.cd(pykgr.config.source_tarballs_directory)

        self.shell.command(
            "wget",
            "-c",
            self.file_url
        ).run(
            display_output = True
        )

        if not os.path.exists(self.code_directory):
            self.shell.tar(
                "xvf",
                self.file_name,
                "-C",
                pykgr.config.source_directory,
                display_output = True
            )

    def install(self):
        self.shell.cd(self.build_directory)
        self.shell.make(
            "-j%s" % pykgr.config.make_opts,
            "install",
            display_output = True
        )

    def make(self):
        self.shell.cd(self.build_directory)
        self.shell.make("-j%s" % pykgr.config.make_opts, display_output = True)

    def prepare(self):
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
