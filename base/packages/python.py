import pykgr
import os


class python(pykgr.Package):
    file_url = "https://github.com/python/cpython/archive/3.9.tar.gz"
    name = "cpython"
    version = "3.9"
    file_name = "3.9.tar.gz"

    # def fetch(self):
    #     self.shell.cd(pykgr.config.source_tarballs_directory)
    #     if os.path.exists(self.code_directory):
    #         print("Already exists")
    #         return
    #
    #     self.shell.command(
    #         "wget",
    #         "-c",
    #         self.file_url
    #     ).run(
    #         display_output = True
    #     )
    #
    #     self.shell.tar(
    #         "xvf",
    #         self.file_name,
    #         "-C",
    #         pykgr.config.source_directory,
    #         display_output = True
    #     )
    #
    # def prepare(self):
    #     self.shell.cd(self.code_directory)
    #     if not os.path.exists(self.build_directory):
    #         os.mkdir(self.build_directory)
    #     self.shell.cd(self.build_directory)

        # self.shell.command(
        #     "%s/configure" % self.code_directory,
        #     "--prefix=%s" % pykgr.config.packages_directory,
        #     "--enable-optimizations"
        # ).run(display_output = True)
