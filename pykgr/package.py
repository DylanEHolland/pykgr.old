from pykgr.shell import Shell
import pykgr
import os
import shutil


class Package(object):
    # This class contains the methods needed to compile most
    # gnu and open source projects.
    #
    # For recipes that aren't compiled you can overload any
    # method needed to change the flow (as well as in derived classes,
    # see base/toolchain module for package derivatives.)

    build_directory = None
    code_directory = None
    compile_directory = None # e.g. if code_directory has a subdir, so "{code_directory}/src" for vim
    subdirectory_location = None
    file_name = None
    file_url = None
    name = None
    repo = False
    repo_url = None
    shell = None
    version = None

    no_build_dir = False

    def __build__(self):
        if pykgr.config.verbose:
            print("\nBuilding", self.file_url)

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

        self.working_directory = self.code_directory
        if self.compile_directory:
            self.working_directory = self.working_directory + self.compile_directory

        self.build_directory = "%s/build" % self.code_directory
        self.__initialize__()

    def __initialize__(self):
        pass

    def __str__(self):
        return "<package [%s-%s]>" % (self.name, str(self.version))

    def configure(self):
        self.shell.command(
            "%s/configure" % self.working_directory,
            "--prefix=%s" % pykgr.config.packages_directory
        ).run()

    def decompress(self):
        if os.path.exists(self.code_directory):
            if pykgr.config.verbose:
                print("Decompressed code exists, removing...")
            self.shell.command("rm", "-rfv", self.code_directory).run()

        self.untar()

    def fetch(self):
        self.shell.cd(pykgr.config.source_tarballs_directory)

        self.shell.command(
            "wget", 
            "-c",
            self.file_url.encode()
        ).run()

    def generate(self):
        self.make()
        self.install()

    def get_code(self):
        if not self.repo:
            self.fetch()
            self.decompress()

    def install(self):
        if self.no_build_dir:
            self.shell.cd(self.working_directory)
        else:
            self.shell.cd(self.build_directory)

        if 'alt_install' in self.__dict__:
            self.alt_install()
        else:
            self.shell.make(
                "-j%s" % pykgr.config.make_opts,
                "install"
            )

    def make(self):
        if self.no_build_dir:
            self.shell.cd(self.working_directory)
        else:
            self.shell.cd(self.build_directory)

        self.shell.make("-j%s" % pykgr.config.make_opts)

    def prepare(self):
        self.shell.cd(self.working_directory)

        if not self.no_build_dir:
            if os.path.exists(self.build_directory):
                shutil.rmtree(self.build_directory)

            if not os.path.exists(self.build_directory):
                os.mkdir(self.build_directory)
            self.shell.cd(self.build_directory)

        self.pre_configure_run()
        self.configure()

    def pre_configure_run(self):
        # Should be overwritten
        pass

    def untar(self):
        self.shell.tar(
            "xvf",
            pykgr.config.source_directory + "/tarballs/" + self.file_name,
            "-C",
            pykgr.config.source_directory
        )


class PackageList(object):
    pass