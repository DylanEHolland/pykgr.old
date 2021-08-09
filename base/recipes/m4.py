import pykgr


class M4(pykgr.Package):
    file_url = "https://github.com/tar-mirror/gnu-m4/archive/refs/tags/v1.4.18.tar.gz"
    file_name = "v1.4.18.tar.gz"
    name = "gnu-m4"
    version = "1.4.18"

    def alt_install(self):
        self.shell.command(
            "make DESTDIR=%s install -j%s" % (
                pykgr.config.packages_directory,
                pykgr.config.make_opts
            )
        )
