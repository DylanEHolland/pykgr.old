from pykgr.shell import Shell
import pykgr
import os


class Package(object):
    # This class contains the methods needed to compile most
    # gnu and open source projects.
    #
    # For packages that aren't compiled you can overload any
    # method needed to change the flow (as well as in derived classes,
    # see base/toolchain module for package derivatives.)

    build_directory = None
    code_directory = None
    file_name = None
    file_url = None
    name = None
    repo = False
    repo_url = None
    shell = None
    version = None

    def __build__(self):
        print("Building", self)
        self.get_code()
        self.prepare()
        self.generate()

    def __init__(self, **kwargs):
        self.shell = Shell(PWD=pykgr.config.source_directory)
        self.code_directory = "%s/%s" % (
            pykgr.config.source_directory,
            "%s-%s" % (
                self.name,
                self.version
            )
        )
        self.build_directory = "%s/build" % self.code_directory
        self.__initialize__()

    def __initialize__(self):
        pass

    def __str__(self):
        return "<package [%s-%s]>" % (self.name, str(self.version))

    def configure(self):
        self.shell.command(
            "%s/configure" % self.code_directory,
            "--prefix=%s" % self.base_directory
        ).run(display_output = True)

    def decompress(self):
        print(self.code_directory)
        if os.path.exists(self.code_directory):
            print("Decompressed code exists, removing...")
            self.shell.command("rm", "-rfv", self.code_directory).run(display_output = True)

        self.untar()

    def fetch(self):
        self.shell.cd(pykgr.config.source_tarballs_directory)

        self.shell.command(
            "wget", 
            "-c",
            self.file_url
        ).run(
            display_output = True
        )

    def generate(self):
        self.make()
        self.install()

    def get_code(self):
        if not self.repo:
            self.fetch()
            self.decompress()

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
        if os.path.exists(self.build_directory):
            os.rmdir(self.build_directory)
        
        os.mkdir(self.build_directory)
        self.shell.cd(self.build_directory)

        self.configure()

    def untar(self):
        self.shell.tar(
            "xvf",
            self.file_name,
            "-C",
            pykgr.config.source_directory,
            display_output = True
        )

class PackageList(object):
    pass