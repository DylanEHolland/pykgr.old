import pykgr


class Coreutils(pykgr.Package):
    file_url = "http://ftp.gnu.org/gnu/coreutils/coreutils-8.32.tar.xz"
    file_name = "coreutils-8.32.tar.xz"
    name = "coreutils"
    version = "8.32"
    no_build_dir = True

    # def pre_configure_run(self):
    #     self.shell.command(
    #         "./bootstrap"
    #     ).run()
